#!/usr/bin/env python

from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SLQAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = """MX|142$|I7eUpITFcR0$v:3E4RHIlY1Y0wNe#3[dTYHu&~q+r}g)&>DW?VHG$*&capWkPt8v*#=U9oNCVsFf~RdT!H8_>LMO3Dg~"""

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    sku = db.Column(db.Integer)
    description = db.Column(db.Text)
    price = db.Column(db.Float, precision=2, asdecimal=True, decimal_return_scale=2)
    lead_image = db.Column(db.String(256))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
        backref = db.backref('products', lazy='dynamic'))

    def __init__(self, name, sku, description, category, price, lead_image):
        self.name = name
        self.sku = sku
        self.description = description
        self.category = category
        self.price = price
        self.lead_image = lead_image

    def __repr__(self):
        return '<Product %r>' % self.name

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

