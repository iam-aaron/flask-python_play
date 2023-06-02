from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/todo.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<Task {self.id}>'

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    todo_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that todo item'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo_item = request.form['todo']
        new_todo = Todo(todo_item=todo_item)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your todo item'
    else:
        todos = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', todos=todos)


if __name__ == '__main__':
    app.run(debug=True)