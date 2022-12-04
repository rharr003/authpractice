from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask import Flask, request, render_template, redirect, session
from flask_wtf import FlaskForm
from model import db, connect_app, User, Feedback
from forms import SignUp, LogIn, FeedbackForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rharr003:Dissidia1!@127.0.0.1:5432/authpractice'
app.config['SQLALCHEMY_ECHO'] = True
Bootstrap(app)
bcrypt = Bcrypt()
connect_app(app)



@app.route('/')
def home():
    session['user_id'] = ''
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        current_user = User.query.filter_by(username=session.get('user_id')).first()
        return redirect(f'/user/{current_user.id}')
    form = SignUp()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user = User.register(username=form.username.data, password=form.password.data, email=form.email.data,
                                 first_name=form.first_name.data, last_name=form.last_name.data)
            db.session.add(current_user)
            db.session.commit()
            session['user_id'] = current_user.username
            return redirect(f'/users/{current_user.id}')
    return render_template('index.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogIn()
    if request.method == 'POST':
        if form.validate_on_submit():
            current_user = User.authenticate(form.username.data, form.password.data)
            if current_user:
                session['user_id'] = current_user.username
                return redirect(f'/users/{current_user.id}')
            else:
                return redirect('/login')
    return render_template('index.html', form=form)

@app.route('/users/<int:user_id>', methods=['GET', 'DELETE'])
def user_detail(user_id):
    if session.get('user_id'):
        current_user = User.query.get(user_id)
        feedback = Feedback.query.filter_by(username=current_user.username)
        return render_template('details.html', user=current_user, feedback=feedback)
    else:
        return redirect('/login')

@app.route('/users/<int:user_id>/feedback', methods=['GET', 'POST'])
def add_feedback(user_id):
    if session.get('user_id'):
        form = FeedbackForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                feedback = Feedback(title=form.title.data, content=form.content.data, username=session.get('user_id'))
                db.session.add(feedback)
                db.session.commit()
                return redirect(f'/users/{user_id}')
        return render_template('index.html', form=form)

@app.route('/logout')
def logout():
    session['user_id'] = ''
    return redirect('/login')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    current_user = User.query.get(user_id)
    if session.get('user_id') == current_user.username:
        user_to_delete = db.session.query(User).filter(User.id == current_user.id).first()
        db.session.delete(user_to_delete)
        db.session.commit()
        session['user_id'] = ''
        return redirect('/login')

@app.route('/feedback/<int:feedback_id>/delete')
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if session.get('user_id') == feedback.user.username:
        feedback_to_delete = db.session.query(Feedback).filter(Feedback.id == feedback.id).first()
        db.session.delete(feedback_to_delete)
        db.session.commit()
        return redirect(f'/users/{User.query.filter_by(username=session["user_id"]).first().id}')
    else:
        return redirect('/login')
app.run(debug=True)

