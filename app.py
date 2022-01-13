from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from sqlalchemy import desc
from sqlalchemy.sql.expression import asc
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/Scrapydata1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# flask swagger configs
SWAGGER_URL = '/swagger'
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


# create db schema class
class HotelModelSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'price', 'rating', 'location', 'amenities', 'image')


# instantiate schema objects for todolist and todolists
HotelModel_Schema = HotelModelSchema(many=False)
HotelModel_Schema = HotelModelSchema(many=True)


@app.route('/', methods=['POST', 'GET'])
def handle_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_car = HotelModel(title=data['title'], price=data['price'], rating=data['rating'], location=data['location'], amenities=data['amenities'], image=data['image'])
            db.session.add(new_car)
            db.session.commit()
            return {"message": f"car {new_car.title} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        cars = HotelModel.query.all()
        results = [
            {
                "title": car.title,
                "price": car.price,
                "rating": car.rating,
                "location": car.location,
                "amenities": car.amenities,
                "image": car.image
            } for car in cars]

        return {"count ": len(results), "data":results}


@app.route('/find', methods=['GET'])
def titleFilter():
    
    titlevalue = request.args.get('title')
    locationValue = request.args.get('location')
    amenitiesValue = request.args.get('amenities')
    priceValue = request.args.get('price')
    amenities = "%{}%".format(amenitiesValue)
    if None not in (titlevalue, locationValue):
        cars = HotelModel.query.filter_by(title=titlevalue, location=locationValue).all()
    elif titlevalue is not None:
        cars = HotelModel.query.filter_by(title=titlevalue).all()
    elif locationValue is not None:
        cars = HotelModel.query.filter_by(location=locationValue).all()
    elif amenitiesValue is not None:
        cars = HotelModel.query.filter(HotelModel.amenities.like(amenities)).all()
    elif priceValue == 'asc':
         cars = HotelModel.query.order_by(asc(HotelModel.price)).all()
    elif priceValue == 'desc':
        cars = HotelModel.query.order_by(desc(HotelModel.price)).all()
    else:
        cars = HotelModel.query.all()
    
    results = [
    {
        "title": car.title,
        "price": car.price,
        "rating": car.rating,
        "location": car.location,
        "amenities": car.amenities,
        "image": car.image
    } for car in cars]

    return {"count ": len(results), "data":results}


@app.route('/location', methods=['GET'])
def locationFilter():
    locationValue = request.args.get('location')
    cars = HotelModel.query.filter_by(location=locationValue).all()
    results = [
        {
            "title": car.title,
            "price": car.price,
            "rating": car.rating,
            "location": car.location,
            "amenities": car.amenities,
            "image": car.image
        } for car in cars]

    return {"count": len(results), "data":results}


if __name__ == '__main__':
    app.run(debug=True)