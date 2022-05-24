from FlaskImport import *
from home import home

@app.route('/change_password', methods = ['POST', 'GET'])
def change_password():
    if request.method == 'GET':
        return  render_template('change_password.html')
     
    if request.method == 'POST':
        newpass = request.form['newpass']

        uid = session['uid']
        if session.get('changeid') != None :
            uid = session['changeid']

        val = (uid,)
        sql = "SELECT UserPasswordID FROM users WHERE UserID = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sql, val)
        pid = cursor.fetchone()[0]

        sql = "SELECT UserName FROM users WHERE UserID = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sql, val)
        uname = cursor.fetchone()[0]

        change_passw(newpass,pid)

        sql = "INSERT INTO logs (LogPasswordDate, LogDriverName, LogPasswordTypeChange) VALUES (%s,%s,%s)"
        val = (date.today(), uname, 'Admin Changed Password')
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        session.pop('changeid', None)
        return home()