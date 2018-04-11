# 1、搭建项目结构

```
config.py : 项目配置文件,生成诸如DEBUG = True、SQLALCHEMY_DATABASE_URI、SQLALCHEMY_TRACK_MODIFICATION = True等配置信息

exts.py :此文件用于实例化db即db = SQLALCHEMY(),防止循环导入

models.py :用于生成项目的模型文件

manage.py :项目的入口文件
```

# 2、使用Bootstrap制作导航条
## （1）Bootstrap的使用
进入到 ` https://www.bootcss.com `中引用:
```
<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
```
又因为js文件要依赖jquery文件,所以进入到`http://www.bootcdn.cn/jquery/`复制`<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>`到上面的`bootstrap.min.js`前面
终上:
```
<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

<script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>

<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

```
## (2)导航条的使用
在组件中找到导航条,复制相关代码,并根据实际需要进行修改

**遇到的问题**:在`static/css/index.css`文件中更改图片的样式,在浏览器中重新启动后并没有引用修改后后的样式而是继续使用修改前的样式,这是由于浏览器缓存的缘故,可以通过*CRTL+F5*刷新浏览器,也可以再浏览器中进行设置当打开开发者模式时不进行缓存.

# 3、使用基模板和模板继承
基模板的使用:将网站中各网页中相同的部分如导航栏、侧边栏等抽离出来放在`base.html`文件中,这样可以减少代码量,可以提高代码的复用.

模板的继承:使用`{% extends 'base.html' %}`继承基模板的代码,同时可以在`{% block xxx %} {% endblock %}`中自定义代码.

# 4、登录页面的创建
登录页面`login.html`的创建主要还是参考`bootstrap`中表单的设计：

```
    <h3 class="page-title">登录</h3>
    <form action="" method="post">
        <div class="form-container">
            <div class="form-group"> #form-group的使用
                <input class="form-control" type="text" placeholder="手机号码"> #form-control的使用
            </div>
            <div class="form-group">
                <input class="form-control" type="password" placeholder="密码">
            </div>
            <div class="form-group">
                <button class="btn btn-primary btn-block">立即登录</button> #btn btn-primary btn-block的使用
            </div>
        </div>
    </form>
```

# 5、注册页面的创建
注册页面的创建和登录页面的创建是一样的：
```
<h3 class="page-title">登录</h3>
    <form action="" method="post">
        <div class="form-container">
            <div class="form-group">
                <input class="form-control" type="text" placeholder="手机号码" name="telephone">
            </div>
            <div class="form-group">
                <input class="form-control" type="password" placeholder="密码" name="password">
            </div>
            <div class="form-group">
                <button class="btn btn-primary btn-block">立即登录</button>
            </div>
        </div>
    </form>

```

# 6、创建User模型
在models.py文件中创建用户模型,用户字段包括:Id、telephone、username、password
```
class User(db.Model):
    __tablename = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
```

问题1:`ImportError: No module named 'MySQLdb'`

解决：`pip3 install pymysql` 并且在配置文件`config.py`中更改`DRIVER = 'pymysql'`

问题2:`pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on '127.0.0.1' ([WinError 10061] 由于目标计算
机积极拒绝，无法连接`

解决：记得在计算机中的管理中将MySQL服务打开

# 7、完成注册视图函数
注册视图函数:

(1)、表单中用户输入的数据的获取`request.form.get()`

(2)、数据库的数据查询`User.query.filter(User.telephone == telephone)`

(3)、数据库的数据添加`user=User(telephone=telephone,username=username,password=password1) db.sesssion.add(user) db.session.commit()`

```
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 =request.form.get('password2')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'此号码已被注册,请更换号码'
        else:
            if password1 != password2:
                return u'密码输入不一致,请重新输入'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

```

# 8、完成登录视图函数
登录视图函数:

(1)、表单中用户输入的数据的获取`request.form.get()`

(2)、数据库的数据查询`User.query.filter(User.telephone == telephone,User.password == password).first()`

(3)、由于HTTP是无状态的,为了保持用户登录状态,需要传递一个session `session['user_id'] = user.id`

```
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或密码输入错误,请确认后再重新输入！'


```










































