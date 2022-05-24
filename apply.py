# from __main__ import app
from FlaskImport import *
from home import home
from sponsor_apply_page import sponsor_apply

@app.route('/apply', methods = ['POST', 'GET'])
def apply():
    cursor = mysql.connection.cursor()
    if request.method == 'GET':

        if sponsor_check(session['uid']) == True:
            return sponsor_apply()
        else:
            return render_template('apply.html')
    
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        sname = request.form['sname']
        uid = session['uid']
        cursor = mysql.connection.cursor()

        sql = "SELECT OrganizationID FROM organizations WHERE EXISTS(SELECT * FROM organizations WHERE OrganizationName = %s)"
        if cursor.execute(sql, (sname,)) :

            sql = "SELECT OrganizationID FROM organizations WHERE OrganizationName = %s"
            cursor.execute(sql, (sname,))
            orgID = cursor.fetchone()[0]

            sql = "SELECT UserFirstName FROM users WHERE UserID = %s"
            cursor.execute(sql, (uid,))
            fname = cursor.fetchone()[0]
            sql = "SELECT UserLastName FROM users WHERE UserID = %s"
            cursor.execute(sql, (uid,))
            lname = cursor.fetchone()[0]

            name = fname + ' ' + lname

            sql = "INSERT INTO applications (ApplicationSponsorID, ApplicationSponsorName, ApplicationDriverID, ApplicationDriverName, ApplicationStatus, ApplicationDate) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (orgID, sname, uid, name, 'open', date.today())
            cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()
            return home()
        
        else :
            err = "The sponsor you entered does not exist."
            return (render_template("apply.html", err = err))