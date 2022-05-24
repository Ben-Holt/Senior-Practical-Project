from FlaskImport import *
from home import home

@app.route('/name', methods = ['POST', 'GET'])
def name():
    return render_template('name.html')
 
@app.route('/nameChange', methods = ['POST', 'GET'])
def nameChange():
    if request.method == 'GET':
        return "Change Name with Form"
     
    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']

        uid = session['uid']
        if session.get('changeid') != None :
            uid = session['changeid']

        cursor = mysql.connection.cursor()
        sql = "UPDATE users SET UserFirstName = %s, UserMiddleName = %s, UserLastName = %s WHERE UserID = %s"
        val = (fname, mname, lname, uid)
        cursor.execute(sql, val)

        val = (uid,)
        sql = "SELECT UserAffiliation FROM users WHERE UserID = %s"
        cursor.execute(sql, val)
        sponCheck = cursor.fetchone()[0]

        if sponCheck == 'yes' :
            sql = "UPDATE driversponsorassociations SET DriverName = %s WHERE DriverID = %s"
            name = fname+' '+lname
            val = (name, uid)
            cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()

        session.pop('changeid', None)

        return home()