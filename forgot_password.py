from FlaskImport import *

@app.route('/forgot_password', methods = ['POST', 'GET'])
def forgot_password():
    if request.method == 'GET':
        return  render_template('forgot_password.html')
     
    if request.method == 'POST':

        uname = request.form['username']
        email = request.form['email']
        newpass = request.form['newpass']
        val = (uname, email)
        sql = "SELECT UserPasswordID FROM users WHERE UserName = %s AND UserEmail = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sql, val)
        pid = cursor.fetchone()[0]

        change_passw(newpass,pid)

        sql = "INSERT INTO logs (LogPasswordDate, LogDriverName, LogPasswordTypeChange) VALUES (%s,%s,%s)"
        val = (date.today(), uname, 'User Forgot Password')
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return render_template('login.html')