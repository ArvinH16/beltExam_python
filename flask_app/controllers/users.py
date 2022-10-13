from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.thought import Thought

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def register_login():
    if 'user_id' in session:
        return redirect('/thoughts')

    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if User.validate_registration(request.form) == False:
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    
    user_id = User.add_user(data)
    session['user_id'] = user_id
    
    return redirect('/thoughts')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        
        return redirect('/')

    user = User.check_email(request.form)
    if user == False:
        flash("Invalid email", "login")
        print("HEY")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')

    session['user_id'] = user.id
    print("HI")
    return redirect('/thoughts')

@app.route('/thoughts')
def thoughts():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        "id": session['user_id']
    }
    
    all_thoughts_with_creator = Thought.all_thoughts_with_creator()
    return render_template("thoughts.html", user = User.get_user(data), all_thoughts_with_creator = all_thoughts_with_creator)

@app.route("/user/<int:id>")
def get_user_thoughts(id):
    if 'user_id' not in session:
        return redirect('/')
        
    data = {
        "user_id": id
    }
    
    all_user_thoughts = User.get_user_thoughts(data)
    return render_template('user_dash.html', all_user_thoughts = all_user_thoughts)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')