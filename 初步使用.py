from flask import Flask , current_app,g,request,make_response,render_template,redirect,abort#导入库
app=Flask(__name__)#创建实例


@app.route('/current')
def index():
    print(app)
    print(current_app)#当前实例
    return  'index'
"""路由配置一"""
@app.route('/') #装饰器，route的用途：抓取识别/后的内容，如果匹配上就运行下面函数。如：www.baidu。com/indenx就会运行hello_world2
def hello_world():
    #视图函数
    return "hello world"
def hello_world2():
    #视图函数
    return "hello world222"
"""路由配置二"""
app.add_url_rule('/home','home',hello_world2)


"可以从装饰器传参到函数中"
@app.route('/user/<page>')
def list_user(page):
    return '您好，你是第{}位用户'.format(int(page)*10)


"""请求报文"""
@app.route('/test/req')
def test_req():
    "获取get请求参数"
    get_args=request.args
    print(get_args)
    page=request.args.get('page')#获取请求时带的参数，括号写参数名
    print(page)
    "获得请求其他信息:ip等"
    hard=request.headers
    print(hard)
    ip=request.remote_addr
    print('ip:',ip)

    return "test "

"请求钩子，拦截请求，还有after_request/trardown_request"
@app.before_first_request#"服务器启动第一个请求到达"
def first_request():
    print('first_request')
@app.before_request
def first_request():
    print('everone_request')


"响应报文"
@app.route('/test/html')
def test_response():
    #构造一个响应对象
   # resp=make_response('这是一个响应对象',403,{'hahaha':'oooo'}) #可以定义返回的内容

    #响应html
    html="<html><h style='color:#f00'>HTML文本显示</h><body></body></html>"#直接写，不规范
    htmls = render_template('index.html')
    resp=make_response(htmls,400)
    return resp

"重定向"

@app.route('/cdx')
def redirectss():
    #根据ip拦截
    ip_list=['0227.0.0.1']
    ip=request.remote_addr
    if ip in ip_list:
        abort(403)#可以引导报错代码，配合下面的forbidden_page ：实现没权限访问的页面展示

    #redirect重定向页面，abort重定向错误
    return redirect('/test/html')# 访问/时 引导到index

print(app.url_map)#查看路由连接

@app.errorhandler(403)
def forbidden_page(err):
    return "您没有权利访问，请联系管理员开通权限"

@app.route('/kate')
def to_kate():
    htmls = render_template('kate.html')
    resp=make_response(htmls,400)
    return resp

if __name__ == '__main__':# 第一种启动方式，但不推荐
    app.run()