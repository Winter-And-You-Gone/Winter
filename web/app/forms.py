from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, \
    Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('    登    录    ')


class EditProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    about_me = TextAreaField('个性签名', validators=[Length(min=0, max=140)])
    img_url = StringField()
    submit = SubmitField('确认')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email(message='邮箱格式错误')])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(),
                                                  EqualTo('password',
                                                          message='两次输入密码不一致')])
    submit = SubmitField('    注    册    ')
    
    # 校验用户名是否重复
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名已经被注册啦，请重新换一个噻!')
    
    # 校验邮箱是否重复
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱已经被注册啦，请重新换一个噻!')
