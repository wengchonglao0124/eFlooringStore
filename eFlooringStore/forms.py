from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField
from wtforms.validators import InputRequired, email


class CheckoutForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), email()])
    address = StringField('Shipping Address', validators=[InputRequired()])
    phone = StringField("Phone Number", validators=[InputRequired()])
    submit = SubmitField('Place Order')
