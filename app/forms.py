from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, ValidationError, EqualTo


from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Авторизоваться')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя пользователя занято')


class CreateFormForm(FlaskForm):
    name = StringField('Имя формы', validators=[DataRequired()])
    submit = SubmitField('Создать')


class EditFormForm(FlaskForm):
    name = StringField('Название формы', validators=[DataRequired()])
    text = TextAreaField('Краткий текст')
    full_text = TextAreaField('Полный текст')
    picture = FileField('Картинка')
    delete_picture = BooleanField('Удалить картинку')
    send_text = BooleanField('Отправить краткий текст')
    send_full_text = BooleanField('Отправить полный текст')
    departure_date = StringField('Дата отправления')
    receive_date = StringField('Дата получения')

    submit = SubmitField('Сохранить')