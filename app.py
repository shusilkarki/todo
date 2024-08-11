from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import pytz


# Define Nepal time zone
nepal_tz = pytz.timezone('Asia/Kathmandu')

# Get the current time in Nepal time zone
nepal_time = datetime.now(nepal_tz)


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize the app with the extension
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    time = db.Column(db.DateTime, default=lambda: datetime.now(nepal_tz))
    #time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def hello_world():    
    if request.method=='POST':
        todo_title = (request.form['title'])
        todo_desc = (request.form['desc'])
        data = Todo(title=todo_title, desc=todo_desc)
        db.session.add(data)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html",alltodo=alltodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        todo_title = (request.form['title'])
        todo_desc = (request.form['desc'])
        data = Todo.query.filter_by(sno=sno).first()
        data.title = todo_title
        data.desc = todo_desc
        db.session.add(data)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


if __name__ == "__main__":
    app.run(debug = True)
