# from __main__ import app
from FlaskImport import *
from home import home

@app.route('/sponsor_apply', methods = ['POST', 'GET'])
def sponsor_apply():
    uid = session['uid']
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        val = (uid,)

        sql = "SELECT UserAffiliation FROM users WHERE UserID = %s AND UserTypeID = 2"
        cursor.execute(sql, val)
        sname = cursor.fetchone()[0]

        val = (sname,)
        sql = "SELECT OrganizationID FROM organizations WHERE OrganizationName = %s"
        cursor.execute(sql, val)
        orgID = cursor.fetchone()[0]
        val = (orgID,)
        
        sql = "SELECT ApplicationDriverID FROM applications WHERE EXISTS(SELECT * FROM applications WHERE ApplicationSponsorID = %s AND ApplicationStatus = 'open')"
        if (cursor.execute(sql, val)) :

            sql = "SELECT ApplicationID, ApplicationDate, ApplicationDriverID, ApplicationDriverName FROM applications WHERE ApplicationSponsorID = %s AND ApplicationStatus = 'open'"
            val = (orgID,)
            cursor.execute(sql, val)
            apps = cursor.fetchall()

            return render_template('sponsor_apply_page.html', apps=apps)

        else :
            err="No Current Open Applications"
            return(render_template("sponsor_no_applicants.html", err=err))
            

    if request.method == 'POST':
        driver = request.form['driver']
        cursor = mysql.connection.cursor()

        val = (uid,)
        sql = "SELECT UserAffiliation FROM users WHERE UserID = %s"
        cursor.execute(sql, val)
        orgName = cursor.fetchone()[0]
        
        val = (driver, orgName)
        sql = "SELECT ApplicationID FROM applications WHERE ApplicationDriverName = %s AND ApplicationSponsorName=%s"
        cursor.execute(sql, val)
        appid = cursor.fetchone()[0]

        val=(appid,)
        sql = "SELECT ApplicationSponsorID FROM applications WHERE ApplicationID = %s"
        cursor.execute(sql, val)
        orgID = cursor.fetchone()[0]

        sql = "SELECT ApplicationDriverID FROM applications WHERE ApplicationID = %s"
        cursor.execute(sql, val)
        driverID = cursor.fetchone()[0]

        val = (driverID,)
        sql = "SELECT UserFirstName FROM users WHERE UserID = %s"
        cursor.execute(sql, val)
        fname = cursor.fetchone()[0]
        sql = "SELECT UserLastName FROM users WHERE UserID = %s"
        cursor.execute(sql, val)
        lname = cursor.fetchone()[0]
        driverName = fname + ' ' + lname

        val = (uid,)
        sql = "SELECT UserAffiliation FROM users WHERE UserID = %s"
        cursor.execute(sql, val)
        orgName = cursor.fetchone()[0]

        sql = "INSERT INTO driversponsorassociations (DriverID, DriverName, SponsorID, SponsorName, DriverPoints) VALUES (%s, %s, %s, %s, %s)"
        val = (driverID, driverName, orgID, orgName, 0)
        cursor.execute(sql, val)

        sql = "UPDATE applications SET ApplicationStatus = %s WHERE ApplicationID = %s"
        val = ('closed', appid)
        cursor.execute(sql, val)

        sql = "UPDATE users SET UserAffiliation = %s WHERE UserID = %s"
        val = ('yes', driverID)
        cursor.execute(sql, val)

        sql = "SELECT OrganizationNumberEmployees FROM organizations WHERE OrganizationID = %s"
        val = (orgID,)
        cursor.execute(sql, val)
        num = cursor.fetchone()[0]

        num_new=num+1

        sql = "UPDATE organizations SET OrganizationNumberEmployees = %s WHERE OrganizationID = %s"
        val = (num_new, orgID)
        cursor.execute(sql, val)
        mysql.connection.commit()

        return home()




