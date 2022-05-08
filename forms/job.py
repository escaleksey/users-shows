from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, \
    EmailField, IntegerField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader_id = IntegerField("ID лидера работы", validators=[DataRequired()])
    job = StringField("Описание работы", validators=[DataRequired()])
    work_size = IntegerField("Объем работы", validators=[DataRequired()])
    collaborators = StringField("Соработники", validators=[DataRequired()])
    is_finished = BooleanField("Работа завершена?")
    submit = SubmitField('Отправить')