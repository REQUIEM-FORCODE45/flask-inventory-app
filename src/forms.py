from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired

class InventoryItemForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    code = IntegerField('Code', validators=[DataRequired()])
    product = StringField('Product', validators=[DataRequired()])
    shelves = IntegerField('Shelves', validators=[DataRequired()])
    floors = IntegerField('Floors', validators=[DataRequired()])
    packs = IntegerField('Packs', validators=[DataRequired()])
    submit = SubmitField('Add Inventory Item')

class TransactionForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    product = StringField('Product', validators=[DataRequired()])
    total = FloatField('Total', validators=[DataRequired()])
    codigo = IntegerField('codigo', validators=[DataRequired()])
    submit = SubmitField('Record Transaction')