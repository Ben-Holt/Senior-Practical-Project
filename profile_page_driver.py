# from __main__ import app
from contextlib import nullcontext
from FlaskImport import *

@app.route('/profile_driver', methods = ['POST', 'GET'])
def profile_driver():
    cursor = mysql.connection.cursor()
    uid = session['uid']
    val = (uid,)
    sql = "SELECT UserAddress FROM users WHERE UserID = %s"
    cursor.execute(sql, val)
    address = cursor.fetchone()[0]

    sql = "SELECT UserEmail FROM users WHERE UserID = %s"
    cursor.execute(sql, val)
    email = cursor.fetchone()[0]

    sql = "SELECT UserPhone FROM users WHERE UserID = %s"
    cursor.execute(sql, val)
    phone = cursor.fetchone()[0]

    sql = "SELECT UserName FROM users WHERE UserID = %s"
    cursor.execute(sql, val)
    username = cursor.fetchone()[0]

    sql = "SELECT UserFirstName FROM users WHERE UserID = %s"
    cursor.execute(sql, val)
    fname = cursor.fetchone()[0]
    sql = "SELECT UserMiddleName FROM users WHERE UserID = %s"
    cursor.execute(sql, val)
    mname = cursor.fetchone()[0]
    sql = "SELECT UserLastName FROM users WHERE UserID = %s"
    cursor.execute(sql, val)
    lname = cursor.fetchone()[0]

    sql = "SELECT UserAffiliation FROM users WHERE UserID = %s"
    cursor.execute(sql, val)
    sponCheck = cursor.fetchone()[0]

    if sponCheck == 'yes' :
        val = (uid,)
        sql = "SELECT SponsorName, DriverPoints FROM driversponsorassociations WHERE DriverID = %s"
        cursor.execute(sql, val)
        points = cursor.fetchall()
        
    else :
        return render_template('profile_driver.html', fname=fname, mname=mname, address=address,
        lname=lname, email=email, phone=phone, username=username)

    mysql.connection.commit()

    return render_template('profile_driver.html', fname=fname, mname=mname, address=address,
    lname=lname, email=email, phone=phone, username=username, points=points)