import giveaways
import pickle
import base64
import requests
from flask import Flask, session, redirect, url_for, render_template, request



app = Flask(__name__)
app.secret_key = 'super secret key'


@app.route('/giveaways', methods=['GET', 'POST'])
def scrape_giveaways():
    if not 'jar' in session:
        return redirect(url_for('login'))
    
    jar = pickle.loads(base64.b64decode(session['jar'].encode()))
    s = requests.Session()
    s.cookies = requests.utils.cookiejar_from_dict(jar)
    
    if request.method == 'POST':
        ids = []
        for identifier, check in request.form.to_dict().items():
            if check=='on':
                ids.append(int(identifier))
        for identifier in ids:
            giveaways.enter_giveaway(s, identifier)

        return 'Entered giveaway for books with IDs: {}'.format(str(ids))
    else:
        gas = giveaways.scrape_giveaways(s)
        gas = [g for g in gas if not g['Entered']]
        
        return render_template('giveaways.html', books=gas)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        s = requests.Session()
        giveaways.login(s, request.form['username'], request.form['password'])
        jar = requests.utils.dict_from_cookiejar(s.cookies)
        session['jar'] = base64.b64encode(pickle.dumps(jar)).decode()
        return redirect(url_for('scrape_giveaways'))

    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



if __name__=='__main__':
    app.run()
