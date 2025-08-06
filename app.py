from flask import Flask,render_template as rt, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) # Initialize Flask app
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///todo.db'
db=SQLAlchemy(app)


class Todo(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=True)
    date=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=="POST":
        title=request.form["title"]
        desc=request.form["desc"]
        todo = Todo()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()

    alltodo = Todo.query.all()
    return rt("index1.html", alltodo = alltodo) 

@app.route('/greet')
def greet():
    return f"Hello, ADITYA!"

@app.route ("/delete/<int:sno>")
def delete(sno):
    Td=Todo.query.filter_by(sno=sno).first()
    db.session.delete(Td)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    if request.method=="POST":
        title=request.form["title"]
        desc=request.form["desc"]
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return rt("update1.html", todo=todo)


@app.route('/show')
def show():
    alltodo= Todo.query.all()
    print(alltodo)
    return "this is show page"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=4105)