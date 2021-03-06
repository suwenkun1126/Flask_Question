from flask import Flask,render_template,url_for,request,redirect,session
import config
from exts import db
from models import User,Question,Answer
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    questions = Question.query.order_by('-created_time').all()
    return render_template('index.html',questions=questions)

@app.route('/login/',methods=['GET','POST'])
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

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register/',methods=['GET','POST'])
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

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>')
def detail(question_id):
    question = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html',question=question)

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

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run()
