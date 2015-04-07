#!/usr/bin/env python

from flask import Flask, request, render_template, session, redirect, url_for, flash
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.uploads import UploadSet, IMAGES, configure_uploads
from wtforms import StringField, IntegerField, DecimalField, SubmitField, FieldList
from flask.ext.wtf.file import FileField
from wtforms.validators import Required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = """MX|142$|I7eUpITFcR0$v:3E4RHIlY1Y0wNe#3[dTYHu&~q+r}g)&>DW?VHG$*&capWkPt8v*#=U9oNCVsFf~RdT!H8_>LMO3Dg~"""
basedir = os.path.abspath(os.path.dirname(__file__)) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(basedir, 'catalog.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['UPLOADS_DEFAULT_DEST'] = '/tmp/prodimg'
app.config['UPLOADS_DEFAULT_URL'] = '/product-imgs'
images = UploadSet('prodimg', IMAGES)
configure_uploads(app, (images,))
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


# ==========================================================================
# --  MODELS  --------------------------------------------------------------

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    sku = db.Column(db.Integer)
    description = db.Column(db.Text)
    price = db.Column(db.Float(precision=2, asdecimal=True, decimal_return_scale=2))
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

# ==========================================================================
# --  UPLOAD MACHINERY  ----------------------------------------------------

# app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(basedir, 'prodimg')
# app.config['UPLOADS_DEFAULT_DEST'] = '/tmp/prodimg'
# app.config['UPLOADS_DEFAULT_URL'] = '/product-imgs'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = NewProductForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            img_no = 1
            prod_name = request.form['product_name']
            # prefix = '-'.join(prod_name.lower().split())
            prefix = ''.join(prod_name.lower().split())
            files = request.files
            for img_file in files:
                stem = '%s%03d.' % (prefix, img_no)
                images.save(files[img_file], name=stem)
                img_no += 1
            flash("Saved image set '%s'." % prefix)
            return redirect(url_for('index'))
        else:
            flash("Uh-oh. Something wrent wong.")
    return render_template('upload.html', form=form)


# ==========================================================================
# --  FORMS  ---------------------------------------------------------------

class NewProductForm(Form):
    product_name = StringField('Product name:', validators=[Required()])
    sku = IntegerField('SKU:')
    description = StringField('Description:')
    price = DecimalField('Price:')
    images = FieldList(FileField('Upload photo:'), min_entries=1, max_entries=10)
    submit = SubmitField('Submit!')

if __name__ == '__main__':
    app.debug = True
    app.run()
