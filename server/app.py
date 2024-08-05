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

# Add views here
@app.route('/earthquakes/<int:id>')
def route_id(id):
    query_first = Earthquake.query.filter_by(id=id).first()
    if query_first is None:
        return make_response({'message': 'Earthquake {} not found.'.format(id)}, 404)
    return query_first.to_dict()    
@app.route('/earthquakes/magnitude/<float:mag>')
def route_magnitude(mag):
    all_e = Earthquake.query.filter(Earthquake.magnitude >= mag).all()
    return_list = []
    count = 0
    for i in all_e:
        return_list.append(i.to_dict())
        count += 1
    return {'count': count, 'quakes': return_list}
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)
