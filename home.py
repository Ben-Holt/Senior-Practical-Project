from FlaskImport import *

@app.route('/home', methods = ['POST', 'GET'])
def home():
    uid = session['uid']
    if admin_check(uid) :
        return render_template('home_admin.html', type='You are an ADMIN')
    if sponsor_check(uid) :
        return render_template('home_sponsor.html', type='You are a SPONSOR')
    if driver_check(uid) :
        return render_template('home.html', type='You are a DRIVER')

    return render_template('home.html')