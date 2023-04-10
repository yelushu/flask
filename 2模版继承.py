from flask import Flask, render_template

app = Flask(__name__)

"""
    继承：{% extends 'base.html' %}
    选择变动区域 {% block content %}{% endblock %}
    替换：{% include 'sidebar.html' %} #他和继承的区别是，全变和局部变
    
"""
@app.route('/')
def index():
    """  首页 """
    return render_template('index.html')


@app.route('/course')
def course():
    """  免费课程 """
    return render_template('course.html')


@app.route('/coding')
def coding():
    """  实战课程 """
    return render_template('coding.html')


@app.route('/article')
def article():
    """  手记 """
    return render_template('article.html')


@app.route('/wenda')
def wenda():
    """  实战课程 """
    return render_template('wenda.html')

"消息闪现 "

if __name__ == '__main__':
    app.run()
