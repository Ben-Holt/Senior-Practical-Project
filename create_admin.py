from FlaskImport import *
from home import home

@app.route('/create_admin', methods = ['POST', 'GET'])
def create_admin():
    if request.method == 'GET':
        return(render_template('create_admin.html'))

    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']

        cursor = mysql.connection.cursor()

        sql = "INSERT INTO passwords (PasswordDate, PasswordString) VALUES (%s, %s)"
        val = (date.today(), hashlib.sha512(password.encode('utf-8')).hexdigest())
        cursor.execute(sql, val)

        sql = "SELECT PasswordID FROM passwords WHERE PasswordString = %s"
        val = (hashlib.sha512(password.encode('utf-8')).hexdigest(), )
        cursor.execute(sql, val)

        passID = cursor.fetchone()[0]

        sql = "INSERT INTO users (UserName, UserPasswordID, UserTypeID) VALUES (%s, %s, %s)"
        val = (username, passID, 3)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()

        return home()