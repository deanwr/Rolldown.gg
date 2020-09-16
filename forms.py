from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import InputRequired, NumberRange

class InputForm(FlaskForm):
    level = IntegerField('Level', validators=[InputRequired(), NumberRange(min=1,max=9,message="Value must be between 1 and 9.")])
    unitCost = IntegerField('Unit Cost', validators=[InputRequired(), NumberRange(min=1,max=5,message="Value must be between 1 and 5.")])
    unitsSameCostGone = IntegerField('Units of Same Cost Gone', validators=[InputRequired(), NumberRange(min=0,message="Value must be greater than or equal to 0.")])
    unitsGone = IntegerField('Units Gone', validators=[InputRequired(), NumberRange(min=0,message="Value must be greater than or equal to 0.")])
    gold = IntegerField('Gold', validators=[InputRequired(), NumberRange(min=0,message="Value must be greater than or equal to 0.")])
    submit = SubmitField('Calculate')
