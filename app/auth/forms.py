from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住密码')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('该昵称已存在')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('此邮箱已注册过')

    def validate_password2(self, password2):
        print(password2.data)
        print(self.password.data)
        if password2.data == self.password.data:
            return True
        else:
            raise ValidationError('两次密码不一致')


class ResetPasswordRequestForm(FlaskForm):
    pass


class ResetPasswordForm(FlaskForm):
    pass
