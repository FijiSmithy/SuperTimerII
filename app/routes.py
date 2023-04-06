from flask import flash, render_template, session, redirect, url_for, request, make_response

from app import app, stats



def clear_session():
    #Wipes out all data in the session cookie
    for key in list(session.keys()):
        session.pop(key)
def insert_session(new_session):
    #Allows you to add new data to the session. Argument must be a dictionary
    if 'racedata' in session:
        temp_session = session['racedata']
    else:
        temp_session={}
    for key in new_session:
        temp_session[key]=new_session[key]
    session['racedata']= temp_session
def get_session():
    #returns a dictionary of the stored session data
    if 'racedata' in session:
        return session['racedata']
    else:
        insert_session({"current":{"1":"CarA"},"next":{}})
        return redirect(url_for('index'))


#================        AUTH ROUTES        ===============
#==========================================================
@app.route('/', methods=['GET' , 'POST'])
def index():
    print("RAce Data: ",app.stats)
    return render_template('index.html.j2', racedata=app.stats)

@app.route('/update_race',methods=['POST'])
def update_race():
    app.stats = request.json
    print(app.stats)
    return make_response('Success',200,{'Status':'Stats Updated'})


@app.route('/flash')
def flash_test():
    flash("This is a test","success")
    flash("This is also a test","warning")
    flash("This is the last test","danger")
    return render_template('index.html.j2')

@app.route('/healthcheck')
def health_check():
    return "<html><body>App is up!</body></html>"
