# from __main__ import app
from FlaskImport import *
from home import home

@app.route('/profile_sponsor', methods = ['POST', 'GET'])
def profile_sponsor():
    cursor = mysql.connection.cursor()
    uid = session['uid']

    if request.method == 'GET':
        val = (uid,)
        sql = "SELECT UserAffiliation FROM users WHERE UserID = %s AND UserTypeID = 2"
        cursor.execute(sql, val)
        sname = cursor.fetchone()[0]

        val = (sname,)
        sql = "SELECT OrganizationID FROM organizations WHERE OrganizationName = %s"
        cursor.execute(sql, val)
        orgID = cursor.fetchone()[0]
        val = (orgID,)

        sql = "SELECT DriverID FROM driversponsorassociations WHERE EXISTS(SELECT * FROM driversponsorassociations WHERE SponsorID=%s)"
        if (cursor.execute(sql, val)) :
            sql = "SELECT DriverID FROM driversponsorassociations WHERE SponsorID=%s"
            val = (orgID,)
            cursor.execute(sql, val)
            driverIDs = cursor.fetchall()

            sql = "SELECT UserAddress, UserEmail, UserPhone, UserName, UserFirstName, UserLastName FROM users WHERE UserID IN %s"
            val = (driverIDs)
            cursor.execute(sql, [driverIDs])
            info = cursor.fetchall()

            sql = "SELECT DriverName, DriverPoints FROM driversponsorassociations WHERE SponsorID=%s"
            val = (orgID,)
            cursor.execute(sql, val)
            points = cursor.fetchall()

            return render_template('profile_sponsor.html', info=info, points=points)
        else :
            return render_template('profile_sponsor.html', err="No Current Drivers")

    if request.method == 'POST':
        name = request.form['name']
        reason = request.form['reason']
        pointsChange = request.form.get('points', type=int)

        val = (uid,)
        sql = "SELECT UserAffiliation FROM users WHERE UserID = %s AND UserTypeID = 2"
        cursor.execute(sql, val)
        sname = cursor.fetchone()[0]

        val = (name, sname)
        sql = "SELECT DriverPoints FROM driversponsorassociations WHERE DriverName = %s AND SponsorName = %s"
        cursor.execute(sql, val)
        currPoints = cursor.fetchone()[0]

        newPoints=currPoints+pointsChange

        sql = "UPDATE driversponsorassociations SET DriverPoints= %s WHERE DriverName = %s AND SponsorName = %s"
        val = (newPoints, name, sname)
        cursor.execute(sql, val)

        sql = "INSERT INTO points (PointDate, PointSponsorName, PointDriverName, PointChange, PointTotal, PointReason) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (date.today(), sname, name, pointsChange, newPoints, reason)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()

        return home()