from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('昵称', validators=[DataRequired()])
    about_me = TextAreaField('简介', validators=[Length(min=0, max=1400)])
    submit = SubmitField('确认修改')


class PostForm(FlaskForm):
    post = TextAreaField('发布动态', validators=[DataRequired(), Length(min=1, max=1400)])
    submit = SubmitField('确认发布')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('发表')


class MessageForm(FlaskForm):
    message = TextAreaField('私信', validators=[DataRequired(), Length(min=1, max=1400)])
    submit = SubmitField('发送')
