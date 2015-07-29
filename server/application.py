import sys
from os import remove
from flask import Flask, Response
from flask import request, render_template, url_for, redirect, json, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import logging, uuid, random

def random_row(Table):
    query = db.session.query(Table)
    row = query.offset(int(query.count() * random.random() )).first()
    row = query.offset(0).first()
    return row

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ycombikea.sqlite'
db = SQLAlchemy(app)

class Base(object):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    desc = db.Column(db.String(255))
    ikea_name = db.Column(db.String(255))
    ycomb_name = db.Column(db.String(255))
    product = db.Column(db.Boolean)
    startup = db.Column(db.Boolean)
    cycle = db.Column(db.String(8))
    product_vote = db.Column(db.BigInteger)
    startup_vote = db.Column(db.BigInteger)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'desc': self.desc,
            'ikea_name': self.ikea_name,
            'ycomb_name': self.ycomb_name,
            'product': self.product,
            'startup': self.startup,
            'cycle': self.cycle,
            'product_vote': self.product_vote,
            'startup_vote': self.startup_vote,
        }

class Ikea(db.Model, Base):
    __tablename__ = 'products'

    def __init__(self,  name="", url="", desc=""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.url = url
        self.desc = desc
        self.ikea_name = name
        self.ycomb_name = unikeaify(name)
        self.product = True
        self.startup = False
        self.product_vote = 0
        self.startup_vote = 0

class Ycomb(db.Model, Base):
    __tablename__ = 'startups'
    desc = db.Column(db.String(512))

    def __init__(self,  name="", url="", desc="", cycle=""):
        self.id = str(uuid.uuid4())
        self.name = name
        self.url = url
        self.desc = desc
        self.cycle = cycle
        self.ikea_name = ikeaify(name)
        self.ycomb_name = name
        self.product = False
        self.startup = True
        self.product_vote = 0
        self.startup_vote = 0

@app.route("/")
def root():
    return render_template('index.html')

@app.route(u'/ycomborikea', methods=[u'GET', u'PUT'])
def ycomborikea():
    print request.json
    if request.method == u"GET":
        random_product_index = 4
        product = random_row(Ikea)
        startup = random_row(Ycomb)
        return jsonify(random.choice([product, startup]).serialize())
    elif request.method == u'PUT':
        try:
            id = request.json['id']
            if request.json['startup']:
                startuporproduct = Ycomb.query.filter(Ycomb.id == id).first()
            else:
                startuporproduct = Ikea.query.filter(Ikea.id == id).first()
            startuporproduct.startup_vote = request.json['startup_vote']
            startuporproduct.product_vote = request.json['product_vote']
            db.session.commit()
            return Response(response="200 Success", status=200)
        except:
            return Response(response="401 Bad Request", status=401)

if __name__ == "__main__":
    db.create_all()  # make our sqlalchemy tables

    app.testing = True
    app.run(port=4000)







