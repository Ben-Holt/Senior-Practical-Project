from FlaskImport import *

@app.route('/create_account', methods = ['POST', 'GET'])
def create_account():
    if request.method == 'GET':
        return(render_template('create_account.html'))

    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
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

        sql = "INSERT INTO users (UserName, UserFirstName, UserMiddleName, UserLastName, UserAddress, UserEmail, UserPhone, UserPasswordID, UserTypeID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (username, fname, mname, lname, address, email, phone, passID, 1)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return(render_template('login.html', err="Account Created"))