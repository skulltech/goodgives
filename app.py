import giveaways
import uuid
from flask import Flask, session, redirect, url_for



app = Flask(__name__)


@app.route('/scrape-giveaways')
def scrape_giveaways():
	if not 'uid' in session:
		return redirect(url_for('login'))

	



@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['password'] = request.form['password']
		session['uid'] = uuid.uuid4()
		return redirect(url_for('index'))

    return 'Hello, World!'


@app.route('/', methods=['GET', 'POST'])
def index():
	if 




if __name__=='__main__':
    app.run()
