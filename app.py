from flask import Flask, request,jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from sqlalchemy import desc
from sqlalchemy.sql.expression import asc
from flask_swagger_ui import get_swaggerui_blueprint
import uuid 
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
import secrets
import datetime
from functools import wraps
app = Flask(__name__)

thisissecret = secrets.token_hex(16) 

app.config['KEY']='thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/Scrapydata1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# flask swagger configs
SWAGGER_URL = ''
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Database API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# create db instance
db = SQLAlchemy(app)

# instanctiate ma
ma = Marshmallow(app)

class HotelModel(db.Model):
    __tablename__ = 'newdata'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    price = db.Column(db.String())
    rating = db.Column(db.String())
    location = db.Column(db.String())
    amenities = db.Column(db.String())
    image = db.Column(db.String())

    def __init__(self, title, price, rating, location, amenities, image):
        self.title = title
        self.price = price
        self.rating = rating
        self.location = location
        self.amenities = amenities
        self.image = image

class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   public_id = db.Column(db.String())
   name = db.Column(db.String())
   password = db.Column(db.String())

   def __init__(self, public_id, name, password):
        self.public_id = public_id
        self.name = name
        self.password = password

# def token_required(f):
#    @wraps(f)
#    def decorator(*args, **kwargs):
#     #    print(request.args['token'])
#        token = None
#        if 'access-token' in request.headers:
#            token = request.headers['access-token']
 
#        if not token:
#            return jsonify({'message': 'a valid token is missing'})
#        try:
#            data = jwt.decode(token, app.config['KEY'], algorithms=["HS256"])
#            print(data)
#            current_user = Users.query.filter_by(public_id=data['public_id']).first()
#        except:
#            return jsonify({'message': 'token is invalid'})
 
#        return f(current_user, *args, **kwargs)
#    return decorator

token = ''
@app.route('/login', methods=['POST']) 
def login_user():
    auth = request.get_json()
    if not auth or not auth['name'] or not auth['password']: 
        return make_response('could not verify', 401, {'Authentication': 'login required"'})   
    user = Users.query.filter_by(name=auth['name']).first()  
    if check_password_hash(user.password, auth['password']):
        global token
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=45)}, app.config['KEY'], "HS256")
        return jsonify({'token' : token})
    return make_response('could not verify',  401, {'Authentication': '"login required"'})

@app.route('/register', methods=['POST'])
def signup_user(): 
    auth = request.get_json()
    if not auth or not auth['name'] or not auth['password']: 
        return make_response('could not verify', 401, {'Authentication': 'login required"'})   
    hashed_password = generate_password_hash(auth['password'], method='sha256')
    new_user = Users(public_id=str(uuid.uuid4()), name=auth['name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'New user created please login'})
 

# @app.route('/users', methods=['GET'])
# def get_all_users(): 
#     users = Users.query.all()
#     results = [
#         {
#         "public_id": user.public_id,
#         "name": user.name,
#         "password": user.password,
#         "admin": user.admin,
              
#     } for user in users]
#     return {"count ": len(users), "data":results}
    

# create db schema class
class HotelModelSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'price', 'rating', 'location', 'amenities', 'image')

# instantiate schema objects for todolist and todolists
HotelModel_Schema = HotelModelSchema(many=False)
HotelModel_Schema = HotelModelSchema(many=True)


@app.route('/post', methods=['POST'])

def handle_hotels():
    if request.is_json:
        data = request.get_json()
        new_hotel = HotelModel(title=data['title'], price=data['price'], rating=data['rating'], location=data['location'], amenities=data['amenities'], image=data['image'])
        db.session.add(new_hotel)
        db.session.commit()
            
        return {"message": f"hotel {new_hotel.title} has been created successfully."}
    else:
        return {"error": "The request payload is not in JSON format"}

    
@app.route('/search', methods=['GET'])
def titleFilter():
    titlevalue = request.args.get('title')
    locationValue = request.args.get('location')
    amenitiesValue = request.args.get('amenities')
    priceValue = request.args.get('price')
    priceValue1 = request.args.get('pricefilter')
    amenities = "%{}%".format(amenitiesValue)
    location = "%{}%".format(locationValue)
    title = "%{}%".format(titlevalue)
    price = "%{}%".format(priceValue)
    global token
   
    if titlevalue is None:
        title = "%"
    if locationValue is None:
        location = "%"
    if amenitiesValue is None:
        amenities = "%"
    if priceValue is None:
        price = "%"
    if priceValue1 == 'asc':
        hotels = HotelModel.query.filter(HotelModel.title.like(title),HotelModel.location.like(location),HotelModel.amenities.like(amenities)).order_by(asc(HotelModel.price)).all()
    elif priceValue1 =='desc':
        hotels = HotelModel.query.filter(HotelModel.title.like(title),HotelModel.location.like(location),HotelModel.amenities.like(amenities)).order_by(desc(HotelModel.price)).all()
    else:
        hotels = HotelModel.query.filter(HotelModel.title.like(title),HotelModel.location.like(location),HotelModel.amenities.like(amenities),HotelModel.price.like(price)).all()
    try:
        data = jwt.decode(token, app.config['KEY'], algorithms=["HS256"])
    except:
        return jsonify({'message': 'Token invalid please login'})

    results = [
        {
            "title": hotel.title,
            "price": hotel.price,
            "rating": hotel.rating,
            "location": hotel.location,
            "amenities": hotel.amenities,
            "image": hotel.image
        } for hotel in hotels]

    return {"count ": len(results), "data":results}


if __name__ == '__main__':
    app.run(debug=True)