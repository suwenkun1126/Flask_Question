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

# 9、提问页面的创建

提问页面的创建和之前的登录页面、注册页面的创建类似
```
    <div class="form-container">
        <h3 class="page-title">发布问答</h3>
        <form action="" method="post">
            <div class="form-group">
                <input type="text" class="form-control" name="title" placeholder="请输入标题">
            </div>
            <div class="form-group">
                <textarea name="content" rows="10" class="form-control" placeholder="请输入内容"></textarea>
            </div>
            <div class="form-group">
                <button class="btn btn-primary">立即发布</button>
            </div>
        </form>
    </div>
```

# 10、 context_processor钩子函数实现注销功能及装饰器实现登录限制

## （1）context_processor钩子函数

context_processor钩子函数：使用这个函数,必须返回一个字典,这个字典中的值在所有的**模板**中都可以使用.
如果在很多模板中都要使用同一个变量,那么就可以使用此钩子函数来进行返回,而不用在每一个视图函数中的`render_template`中
都要写一次，从而使代码更加简洁.

```
@app.context_processor
def my_context_processor:
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}
        
```
**注意**：最后`return {}`的写法,如果不写会出现报错

在`base.html`中

```
    <ul class="nav navbar-nav navbar-right">
        {% if user  %}
            <li><a href="#">{{ user.username }}</a></li>
            <li><a href="{{ url_for('logout') }}">注销</a></li>
        {% else %}
            <li><a href="{{ url_for('login') }}">登录</a></li>
            <li><a href="{{ url_for('register') }}">注册</a></li>
        {% endif %}
    </ul>
```
## （2）装饰器实现登录限制

装饰器：它本质上是一个特殊的函数,一方面它的参数是一个函数,另一方面它的返回值也是一个函数.

装饰器的使用:

A、通过一个@符号,放在函数的上面

B、装饰器中定义的函数要使用 `*args` 和 `**kwargs` ,并且在函数中执行原始函数也要把`*args` 和 `**kwargs`传递进去

C、使用functools.wraps在装饰器中的函数上把要传递进去的这个函数进行一个包裹,这样就不会丢掉原来函数`__name__`等属性

```
from functools import wraps

def login_required(func):
    wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        return redirect(url_for('login'))
    return wrapper
```

# 11、创建Question模型并完成提问视图函数

创建Question模型:
```
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    text = db.Column(db.Text,nullable=False)
    author_id = db.Column(db.Integer,db.Foreignkey('user.id'))
    author = db.relationship('User',backref=db.backref('questions'))
    
```

实现视图函数:

```
@app.route('/question/')
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = requstion.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))
```

# 12、首页页面的创建

首页页面的创建主要涉及到前端的知识

```
    <ul class="question-list-group">
        <li>
            <div class="avatar-group">
                <img class="avatar" src="{{ url_for('static',filename='images/brand.png') }}" alt="头像">
            </div>
            <div class="question-group">
                <p class="question-title"><a href="#">这里是标题</a></p>
                <p class="quetion-content">这里是文章内容。。。。。。。。。。。。。。。。</p>
            </div>
            <div class="question-info">
                <span class="question-author">xiaozuozuo</span>
                <span class="question-time">2018-04-10 20:12:23</span>
            </div>
        </li>
    </ul>
```

# 13、完成首页视图函数
首页视图函数

```
@app.route('/')
def index():
    questions = Question.query.order_by('-created_time').all()
    return render_template('index.html',questions=questions)
```
注意按时间顺序排列的这种写法：`questions = Question.query.order_by('-created_time').all()`

```
<ul class="question-list-group">
        {% for question in questions %}
            <li>
                <div class="avatar-group">
                    <img class="avatar" src="{{ url_for('static',filename='images/brand.png') }}" alt="头像">
                </div>
                <div class="question-group">
                    <p class="question-title"><a href="#">{{ question.title }}</a></p>
                    <p class="quetion-content">{{ question.content }}</p>
                </div>
                <div class="question-info">
                    <span class="question-author">{{ question.author.username }}</span>
                    <span class="question-time">{{ question.created_time }}</span>
                </div>
            </li>
        {% endfor %}
    </ul>
```
注意作者是如何取到：`question.author.username`

# 14、完成问答详情页的创建

## （1）详情页视图函数的创建

```
@app.route('/detail/<question_id>')
def detail(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html',question=question)

```


## （2）详情页面模板的创建

```
<h3 class="page-title">{{ question.title }}</h3>
    <p class="question-info">
        <span class="question-author">作者：{{ question.author.username }}</span>
        <span>时间：{{ question.created_time }}</span>
    </p>
    <hr>
    <p class="question-content">{{ question.content }}</p>
    <hr>
```

**注意**：在首页中实现详情页面的跳转`url_for('detail',question_id=question.id)`,记得要传入参数,否则会发生报错

# 15、评论页面的创建

创建评论页面：

```
<h4>评论：（5）</h4>
    <form action="#" method="post">
        <div class="form-group">
            <input type="text" class="form-control" name="answer_content" placeholder="请输入评论">
        </div>
        <div class="form-group" style="text-align: right">
            <button class="btn btn-primary">评论</button>
        </div>
    </form>
```

# 16、创建Answer模型并完成评论视图函数

## （1）创建Answer模型

```
class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    answer = db.Column(db.Text,nullable=False)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    question = db.relationship('Question',backref=db.backref('answers'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',backref=db.backref('answers'))
```


## （1）完成评论视图函数

```
@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    answer_content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(answer=answer_content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))
```
**注意**：为了将评论提交到数据库,必须要新建一个Answer模型,并且要有author字段,author字段可以通过`user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()`获得,并且还要有question字段,要想得到question地段就要从`question = Question.query.filter(Question.id == question_id).first()`获得,然后如何拿到`question_id`就是关键.
    
```
/detail.html
    <div class="form-group">
        <input type="text" class="form-control" name="answer_content" placeholder="请输入评论">
        <input type="hidden" name="question_id" value="{{ question.id }}">
    </div>
```
     
     从而在视图函数中通过`question_id = request.form.get('question_id')`获得`question_id`的值





































