
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField,IntegerField,FileField
from wtforms.validators import DataRequired,ValidationError
from flask_wtf.file import FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField(label='用户名')
    password=PasswordField(label='密码')
    submit=SubmitField(label='登陆')


class Register_Form(FlaskForm):
    """def __init__(self,csrf_enabled,*args,**kwargs):
        super().__init__(csrf_enabled=csrf_enabled,*args,**kwargs)"""
    username = StringField(label='用户名')
    password = PasswordField(label='密码',validators=[DataRequired('请输入密码')])
    submit = SubmitField(label='注册')
    birth_date=DateField(label='生日')
    age=IntegerField(label='年龄')
    number_id=StringField(label='身份证号')
    def validate_username(self,field):
        username=field.data
        if len(username)<3:
            raise ValidationError('请输入11位以上')
        return field

class UserAvatarForm(FlaskForm):
    """ 用户头像上传 """
    avatar = FileField(label='上传头像', validators=[
        FileRequired('请选择头像文件'),#必须要上传文件
        FileAllowed(['png'], '仅支持PNG图片上传')#文件类型验证
    ])