from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.thought import Thought

@app.route('/add_thought', methods=["POST"])
def add_thought():
    if not Thought.validate_thought(request.form):
        return redirect('/')

    data = {
        'thought': request.form['thought'],
        'user_id': session['user_id']
    }
    new_thought_id = Thought.add_thought(data)
    return redirect('/thoughts')

@app.route('/delete/<int:id>')
def delete_thought(id):
    data = {
        "thought_id": id
    }

    Thought.delete_thought(data)
    return redirect('/thoughts')

@app.route('/like/<int:id>')
def like(id):
    data = {
        "thought_id": id
    }

    Thought.like(data)
    return redirect('/thoughts')

@app.route('/unlike/<int:id>')
def unlike(id):
    data = {
        "thought_id": id
    }

    Thought.unlike(data)
    return redirect('/thoughts')

