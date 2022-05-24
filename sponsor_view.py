from FlaskImport import *
from home import home

@app.route('/sponsor_view', methods = ['POST', 'GET'])
def sponsor_view():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()

        sql = "SELECT OrganizationName FROM organizations"
        cursor.execute(sql)
        snames = cursor.fetchall()
        return render_template("sponsor_view.html",snames=snames)
     
    if request.method == 'POST':
        sname = request.form['sname']

        cursor = mysql.connection.cursor()
        val = (sname, )
        sql = "SELECT UserID FROM users WHERE UserAffiliation=%s"
        cursor.execute(sql, val)
        uid = cursor.fetchone()[0]

        session['uid'] = uid

        mysql.connection.commit()
        cursor.close()

        return home()