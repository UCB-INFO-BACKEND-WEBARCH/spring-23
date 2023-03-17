from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/cats_db"
db = SQLAlchemy(app)

# Define a `Cat` model, which will map to a `cats` table in the database.
class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    color = db.Column(db.String(80))
    breed = db.Column(db.String(80))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
            'breed': self.breed
        }

@app.route('/cats')
def get_cats():
    cats = Cat.query.all() # Queries all records in that model/table - SELECT *
    return jsonify([cat.to_dict() for cat in cats])


@app.route('/cats/<int:catId>')
def get_cat(catId):
    cat = Cat.query.filter_by(id=catId).first() # filter_by allows us to add filters to our Queries - SELECT * FROM cat WHERE ....
    if cat:
        return jsonify(cat.to_dict())
    else:
        return jsonify({'error': 'Cat not found'})


@app.route('/cats', methods=['POST'])
def add_cat():
    data = request.get_json()
    new_cat = Cat(name=data['name'], color=data['color'], breed=data['breed'])
    db.session.add(new_cat) # Allows us to add/post new rows to the table
    try:
        db.session.commit() # Ensures that the data is actually written to the table - ACID properties anyone?
        return jsonify(new_cat.to_dict())
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Cat already exists'})


@app.route('/cats/<int:id>', methods=['PUT'])
def update_cat(id):
    data = request.json
    cat = Cat.query.filter_by(id=id).first()
    if cat:
        cat.name = data.get('name', cat.name)
        cat.color = data.get('color', cat.color)
        cat.breed = data.get('breed', cat.breed)
        db.session.commit()
        return jsonify(cat.to_dict())
    else:
        return jsonify({'error': 'Cat not found'})


@app.route('/cats/<int:id>', methods=['DELETE'])
def delete_cat(id):
    cat = Cat.query.filter_by(id=id).first()
    if cat:
        db.session.delete(cat)
        db.session.commit()
        return jsonify({'message': 'Cat deleted'})
    else:
        return jsonify({'error': 'Cat not found'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
