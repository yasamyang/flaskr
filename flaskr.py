# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
#nltk
from nltk import word_tokenize
from nltk import pos_tag
#read & write lisp
import rwlisp
rwlisp.rlisp()    #read lisp
# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = ''
##################################################
selEnv=''
selRot=''
entries=''
wsEnv=''
wsRot=''
#read env & robot data from static folder
dataEnv={k:v for line in open('./static/envData').readlines() for (k,v) in (line.strip().split(':'),)}
#dataEnv=[d.strip() for d in dataFile]
#dataFile=open('./static/rotData').readlines()
dataRot={k:v for line in open('./static/rotData').readlines() for (k,v) in (line.strip().split(':'),)}
#print dataEnv

########################################    
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    
#for create db
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()
    
@app.route('/')
def show_entries():
    session.pop('go_to_plan', None)
    #cur = g.db.execute('select title, text from entries order by id desc')  #using sql to get data from db
    #entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    WS=wsEnv+wsRot
    return render_template('show_entries.html', entries=entries, dataRot=dataRot, dataEnv=dataEnv, selRot=selRot, selEnv=selEnv, WS=WS)

@app.route('/addRot', methods=['POST'])
def addRot_entry():
    global selRot, wsRot
    if not session.get('logged_in'):
        abort(401)
    #g.db.execute('insert into entries (title, text) values (?, ?)',[request.form['selRot'], request.form['selRot']])
    #g.db.commit()
    selRot = request.form['selRot']
    wsRot=dataRot[selRot]
    print selRot
    flash('You selected '+ selRot)
    return redirect(url_for('show_entries'))

@app.route('/addEnv', methods=['POST'])
def addEnv_entry():
    global selEnv, entries, wsEnv
    entries=''
    if not session.get('logged_in'):
        abort(401)
    #g.db.execute('insert into entries (title, text) values (?, ?)',[request.form['selEnv'], request.form['selEnv']])
    #g.db.commit()
    selEnv = request.form['selEnv']
    wsEnv=dataEnv[selEnv]
    flash('You selected '+request.form['selEnv']+' Environment')
    print selEnv
    return redirect(url_for('show_entries'))
 
@app.route('/action', methods=['POST'])
def action():
    global entries, wsEnv
    command=request.form['command']
    sentence='Robot '+command
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    print tagged
    vb_list=[tag[0] for tag in tagged if 'VB' in tag[1]]
    print 'vb_list is ',vb_list
    prp_list=[tag[0] for tag in tagged if 'PRP' in tag[1]]
    print 'vb_list is ',vb_list
    nn_list=[tag[0] for tag in tagged if 'NN' in tag[1]]
    print 'nn_list is ',nn_list
    print [nn for nn in nn_list[1:] if '(exist '+nn+')' in wsEnv]
    print 'wsEnv= ',wsEnv
    if vb_list and len(nn_list)>1:
        act='('+vb_list[0]+' '+prp_list[0]+' '+nn_list[1]+')'
    else:
        act='no such command'
    print 'act = ',act
    if command and act is not 'no such command':
        import os
        rwlisp.init.insert(2,wsEnv)   #insert state into init
        rwlisp.act.insert(2,act)
        print rwlisp.init
        print rwlisp.act
        rwlisp.wlisp()
        fileo=open('./static/action','w')
        fileo.close()
        os.system('sbcl --script myshop.lisp')
        rwlisp.init.pop(2)    #remove init
        rwlisp.act.pop(2)
        filein=open('./static/action').readlines()    #read file
        path=''
        for cmd in filein:
            cmdword=[]
            while True:
                f1=cmd.find('!')
                if f1 == -1:
                    break
                f2=cmd.find(')')
                cmdword.append(cmd[f1:f2])
                cmd=cmd[f2+1:]
            #print(cmdword)
            for p in cmdword:
                #print p
                path=path+p+' -> '
        #print path[:-4]
        entries = path[:-4]
        #print entries
        if not entries: 
            entries=act
            flash('Please try again')
    else:
        entries=''
        flash('Please try again')
    #os.system('openrave.py --example hanoi')
    return redirect(url_for('show_entries')) 
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    print session
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/add_NS')
def add_NS():
    print session
    error = None
    session['go_to_plan'] = True
    return render_template('add_NS.html', error=error)

@app.route('/revise_S')
def revise_S():
    print session
    error = None
    session['go_to_plan'] = True
    return render_template('revise_S.html', error=error)


if __name__ == '__main__':
    init_db()
    app.run()   