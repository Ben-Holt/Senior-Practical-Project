from FlaskImport import *
from home import home

@app.route('/driver_view', methods = ['POST', 'GET'])
def driver_view():
    if request.method == 'GET':
        return render_template("driver_view.html")
     
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        if sponsor_check(session['uid']) :
            fname = request.form['fname']
            lname = request.form['lname']
            name=fname+' '+lname

            val = (session['uid'],)
            sql = "SELECT UserAffiliation FROM users WHERE UserID=%s"
            cursor.execute(sql, val)
            sname = cursor.fetchone()[0]

            sql = "SELECT * FROM driversponsorassociations WHERE SponsorName=%s AND DriverName=%s"
            val=(sname, name)            
            if(cursor.execute(sql, val)) :
                val = (fname, lname)
                sql = "SELECT UserID FROM users WHERE UserFirstName = %s AND UserLastName = %s"
                cursor.execute(sql, val)
                uid = cursor.fetchone()[0]

                session['uid'] = uid
                return home()
            else:    
                err='Driver Not In Your Sponsor'
                return render_template("driver_view.html",err=err)

        else:
                
            fname = request.form['fname']
            lname = request.form['lname']

            val = (fname, lname)
            sql = "SELECT UserID FROM users WHERE UserFirstName = %s AND UserLastName = %s"
            cursor.execute(sql, val)
            uid = cursor.fetchone()[0]

            session['uid'] = uid

            mysql.connection.commit()
            cursor.close()

            return home()