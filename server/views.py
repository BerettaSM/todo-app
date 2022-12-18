from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from . import db
from .models import Todo


views = Blueprint('views', __name__)


@views.route('/', methods=('GET',))
@login_required
def home():
    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', todos=todos)


@views.route('/create-new-todo', methods=('POST',))
@login_required
def create_todo():
    data = request.form
    new_todo_text = data.get('new-todo')
    if len(new_todo_text) == 0:
        flash('Type something before adding!', category='danger')
        return redirect(url_for('views.home'))
    new_todo = Todo(
        text=new_todo_text,
        user_id=current_user.id
    )
    db.session.add(new_todo)
    db.session.commit()
    flash('Added!', category='success')
    return redirect(url_for('views.home'))


@views.route('/delete-todo/<int:todo_id>', methods=('GET',))
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo and todo.user_id == current_user.id:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('views.home'))
