# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    quake = Earthquake.query.filter(Earthquake.id == id).first()

    if quake:
        body = quake.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found'}
        status = 404
    return make_response(body,status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_more_than_magnitude(magnitude):
    earthquake_data = Earthquake.query.filter(Earthquake.magnitude > magnitude).all()
    if len(earthquake_data) != []:
        qs = []
        for q in earthquake_data:
            q_dict = q.to_dict()
            qs.append(q_dict)
        body = {
            'count':len(qs),
            'quakes':qs
        }
        status = 200
    else:
        body = {"count":0,"quakes":[]}
        status = 404
    return make_response(body,status)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
