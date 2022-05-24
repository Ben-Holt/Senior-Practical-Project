# from __main__ import app
from FlaskImport import *
from home import home

@app.route('/profile_admin', methods = ['POST', 'GET'])
def profile_admin():
    if request.method == 'GET':
        return render_template('profile_admin_question.html')

@app.route('/profile_admin_to_driver', methods = ['POST', 'GET'])
def profile_admin_to_driver() :
    
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        return render_template('profile_admin_question.html')
     
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        val = (fname, lname)
        sql = "SELECT UserID FROM users WHERE UserFirstName = %s AND UserLastName = %s"

        cursor.execute(sql, val)
        uid = cursor.fetchone()[0]
        session['changeid'] = uid
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
            return render_template('profile_admin.html', fname=fname, mname=mname, address=address,
            lname=lname, email=email, phone=phone, username=username,points=points)
        else :
            return render_template('profile_admin.html', fname=fname, mname=mname, address=address,
            lname=lname, email=email, phone=phone, username=username)


@app.route('/profile_admin_to_sponsor', methods = ['POST', 'GET'])
def profile_admin_to_sponsor() :
    
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        return render_template('admin_change_ratio.html')
     
    if request.method == 'POST':
        sname = request.form['sname']
        ratio = request.form.get('ratio', type=float)
        val = (ratio,sname)
        sql = "UPDATE organizations SET OrganizationPointValue = %s WHERE OrganizationName = %s"
        cursor.execute(sql,val)
        mysql.connection.commit()
        cursor.close()
        return home()
        

