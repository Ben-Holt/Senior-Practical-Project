from FlaskImport import *
from home import home

@app.route('/create_sponsor', methods = ['POST', 'GET'])
def create_sponsor():
    if request.method == 'GET':
        return(render_template('create_sponsor.html'))

    if request.method == 'POST':
        sname = request.form['sname']
        username = request.form['uname']
        password = request.form['pass']
        pointrate = request.form['prate']

        cursor = mysql.connection.cursor()

        sql = "INSERT INTO passwords (PasswordDate, PasswordString) VALUES (%s, %s)"
        val = (date.today(), hashlib.sha512(password.encode('utf-8')).hexdigest())
        cursor.execute(sql, val)

        sql = "SELECT PasswordID FROM passwords WHERE PasswordString = %s"
        val = (hashlib.sha512(password.encode('utf-8')).hexdigest(), )
        cursor.execute(sql, val)

        passID = cursor.fetchone()[0]

        sql = "INSERT INTO users (UserName, UserAffiliation, UserPasswordID, UserTypeID) VALUES (%s, %s, %s, %s)"
        val = (username, sname, passID, 2)
        cursor.execute(sql, val)

        sql = "INSERT INTO organizations (OrganizationName, OrganizationNumberEmployees, OrganizationPointValue) VALUES (%s, %s, %s)"
        val = (sname, 0, pointrate)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()

        return home()