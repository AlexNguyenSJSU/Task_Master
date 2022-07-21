from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#Telling our app where our database is located:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#the database has been initialized with the settings from our app:
db = SQLAlchemy(app) 

#Set up the class:
class Task_to_do(db.Model): 
    #Set up the columns:
    #First One is the id column: (The Integer that references the ID of each entry)
    id = db.Column(db.Integer, primary_key=True)
    #Text Column with 200 characters and nullable=False cuz don't want this text column to be left blank
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    
    #Function that return 1 string every time we create 1 new element:
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def home():
    #if request sent to this route is POST -> grab the task and put it into the database
    if request.method == 'POST':
        #task_content is equal to the input content -> grab it
        task_content = request.form['content']
        new_task = Task_to_do(content=task_content)
        
        #Pushing it to the database:
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was something wrong when adding your task!'

    else: #Otherwise, we're just looking at the page
        tasks = Task_to_do.query.order_by(Task_to_do.date_created).all() #This will look at all contents of database in order of the date they're created, return all of them
        return render_template('index.html', tasks = tasks) #Then, passing them into template.

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task_to_do.query.get_or_404(id) #attempt to get that task by the id and if it doesn't exist -> going to 404

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was something wrong when deleting your task!'

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Task_to_do.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was something wrong when updating your task!'
    else:
        return render_template('update.html', task=task)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)