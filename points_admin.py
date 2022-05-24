from FlaskImport import *

@app.route('/points_admin', methods = ['POST', 'GET'])
def points_admin():

    if request.method == 'GET':
        return  render_template('points_admin.html')
     
    if request.method == 'POST':

        fname = request.form['fname']
        lname = request.form['lname']
        val = (fname, lname)
        sql = "SELECT UserID FROM users WHERE UserFirstName = %s AND UserLastName = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sql, val)
        uid = cursor.fetchone()[0]
        session['changeid'] = uid
        val = (uid,)

        sql = "SELECT UserPoints FROM users WHERE UserID = %s"
        val = (uid, )
        cursor.execute(sql, val)
        points = cursor.fetchone()[0]
        return render_template('points_admin.html', points=points)