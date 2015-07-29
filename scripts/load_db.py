# -*- coding: utf-8 -*-

from os import remove
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import uuid, codecs
from unidecode import unidecode
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../ycombikea.sqlite'
db = SQLAlchemy(app)

def load(file_name):
    lines = []
    with codecs.open(file_name, 'r', 'utf8') as f:
        for line in f:
            line = line.split('\t')
            lines.append(line)
    return lines 

def ikeaify(name):
    ikea_dict = {
        "a": [u"a", u"å", u"ä"],
        "o": [u"o", u"ö"],
        "u": [u"u", u"ü"],
    }
    ikea_name = name
    aous = [ i for i,ltr in enumerate(name) if any(key for key in ikea_dict.keys() if ltr == key )]
    for aou in aous:
        ltr = name[aou]
        ikea_name = ikea_name[:aou]+random.choice(ikea_dict[ltr])+ikea_name[aou+1:]
    print name, ikea_name.upper()
    return ikea_name

def unikeaify(name):
    return unidecode(name)

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
            'email': self.email,
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
        self.product_vote = 1
        self.startup_vote = 1

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
        self.product_vote = 1
        self.startup_vote = 1


if __name__ == "__main__":
    try:
        remove("../ycombikea.sqlite")
    except OSError:
        pass

    db.create_all()  # make our sqlalchemy tables
    products = load('scrape_ikea.txt')
    for url, name, desc in products:
        product = Ikea(name, url, desc)
        db.session.add(product)
    products = Ikea.query.all()

    startups = load('scrape_ycomb.txt')
    for url, name, desc, cycle in startups:
        startup = Ycomb(name, url, desc, cycle)
        db.session.add(startup)
    startups = Ycomb.query.all()

    db.session.commit()


