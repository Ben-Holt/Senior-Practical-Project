# from __main__ import app
from FlaskImport import *
from home import home

@app.route('/admin_pair', methods = ['POST', 'GET'])
def admin_pair():
    fname = request.form['fname']
    lname = request.form['lname']
    sname = request.form['sname']
    name = fname+' '+lname

    cursor = mysql.connection.cursor()

    sql="SELECT OrganizationNumberEmployees FROM organizations WHERE OrganizationName = %s"
    val=(sname,)
    cursor.execute(sql,val)
    currnum=cursor.fetchone()[0]
    num=currnum+1
    sql="UPDATE organizations SET OrganizationNumberEmployees = %s WHERE OrganizationName = %s"
    val=(num,sname)
    cursor.execute(sql,val)

    sql="UPDATE users SET UserAffiliation=%s WHERE UserFirstName=%s AND UserLastName=%s"
    val=('yes',fname,lname)
    cursor.execute(sql,val)

    sql="SELECT UserID FROM users WHERE UserFirstName=%s AND UserLastName=%s"
    val=(fname,lname)
    cursor.execute(sql,val)
    driverID=cursor.fetchone()[0]

    sql="SELECT OrganizationID FROM organizations WHERE OrganizationName=%s"
    val=(sname,)
    cursor.execute(sql,val)
    orgID=cursor.fetchone()[0]

    sql = "INSERT INTO driversponsorassociations (DriverID, DriverName, SponsorID, SponsorName, DriverPoints) VALUES (%s, %s, %s, %s, %s)"
    val = (driverID, name, orgID, sname, 0)
    cursor.execute(sql, val)

    sql ="SELECT * FROM applications WHERE ApplicationSponsorID = %s AND ApplicationStatus = 'open' AND ApplicationDriverID=%s"
    val=(orgID,driverID)
    if (cursor.execute(sql, val)) :
        sql="UPDATE applications SET ApplicationStatus=%s WHERE ApplicationSponsorID = %s AND ApplicationStatus = 'open' AND ApplicationDriverID=%s"
        val=('closed',orgID,driverID)
        cursor.execute(sql,val)

    mysql.connection.commit()
    cursor.close()

    return home()



