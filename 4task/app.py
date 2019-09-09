from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:skywlk@localhost/zad2_db'
db = SQLAlchemy(app)

class poruke(db.Model):
	process_id = db.Column(db.String(5))
	message = db.Column(db.String(5), primary_key = True)
	
	def __init__(self, process_id, message):
		self.process_id = process_id
		self.message = message
		
	def __repr__(self):
		return '<Message %r>' % self.message

@app.route('/')
def index():
	return 'Hello world!'
	
@app.route('/messagepage')
def display_messagepage():
	message = poruke.query.all()	
	return render_template('index.html', message = message)
	

if __name__ == '__main__':
	app.run()