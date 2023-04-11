from flask import Flask ,render_template,redirect,url_for
import pymysql
import os
pymysql.install_as_MySQLdb()
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy

from forms import  LoginForm,Register_Form,UserAvatarForm
from werkzeug.utils import secure_filename



app=Flask(__name__)#创建实例


app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:yelushu7758258@localhost/test_flask'#配置数据库

#app.config['WTF_CSRF_SECRET_KEY']='abc123abc'#CSRF保护
app.config['SECRET_KEY']='abc123abc'#s设置了这个可以不用设置上面
db=SQLAlchemy(app)

app.config['SESSION_TYPE'] = 'filesystem'

app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), 'static')#自定义文件上传路径



# 创造数据库连接（需要在console中跑，代码如下）也可以 通过navicat创建
"""根据gpt提示 
from app import app, db
with app.app_context():
    db.create_all()
"""
class User(db.Model):
    __tablename__='weibo_user'
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),nullable=False)
    possword = db.Column(db.String(256), nullable=False)
    birth_date = db.Column(db.Date)
    age=db.Column(db.Integer,default=0)
    number_id=db.Column(db.Integer)

class UserAddress(db.Model):
    "用户地址"
    __tablename__ = 'weibo_user_add'
    id=db.Column(db.Integer,primary_key=True)
    addr=db.Column(db.String(64),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('weibo_user.id'),nullable=False)#外键关联
    user=db.relationship('User',backref=db.backref('address',lazy=True))#反向引用：原本是根据名称--用户id--关联用户地址表--地址。在用户地址表创建反向引用 直接可以名称--用户id--地址


"""数据插入需要在console中操作,新增修改：设置相同的主键
from orm import app,User, db
with app.app_context():
    for i in range(100):
        user = User(username='张{}'.format(i), possword='{}'.format(i * 5))
        db.session.add(user)
    db.session.commit()
    """

@app.route('/')
def mine():
    """首页"""
    return render_template('index.html')

@app.route('/user/<int:page>/')
def list_user(page):
    per_page = 10
    # 1 查询用户信息
    user_query = User.query
    # 2 准备分页数据
    user_page_data = user_query.paginate(page=page, per_page=per_page)
    return render_template('user_page.html', user_page_data=user_page_data)

@app.route('/login',methods=['GET','POST'])
def page_form():
    "form表单练习"
    form=LoginForm()

    return render_template('page_form.html',form=form)

@app.route('/register',methods=['GET','POST'])
def page_register():
    "新用户注册：表单保存数据"
    #form=Register_Form(csrf_enabled=False)#在forms中设置关闭crsf保护关闭
    form = Register_Form()
    #用户提交时，会触发
    if form.validate_on_submit():
        #验证通过的操作:
        #1)获取数据
        username=form.username.data
        possword=form.password.data
        birth_date=form.birth_date.data
        age=form.age.data
        number_id=form.number_id.data

        #2）构建用户对象
        user=User(username=username,possword=possword,age=age,birth_date=birth_date,number_id=number_id)
        #3）提交数据库
        db.session.add(user)
        db.session.commit()
        #4）跳转到登陆
        return redirect(url_for('page_form'))
    else:

        return render_template('page_register.html',form=form)


@app.route('/upload',methods=['GET','POST'])
def uploads():
    """ 头像上传 """
    form = UserAvatarForm()
    if form.validate_on_submit():
        # 获取图片对象
        img = form.avatar.data
        f_name = secure_filename(img.filename)
        file_name = os.path.join(app.config['UPLOAD_PATH'], f_name)
        img.save(file_name)
        print('保存成功')
        return redirect('/')
    else:
        print(form.errors)
    return render_template('uploads.html',form=form)
if __name__ == '__main__':
    app.run()