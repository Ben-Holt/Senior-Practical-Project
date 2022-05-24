from FlaskImport import *
from home import home

@app.route('/changePoints', methods = ['POST', 'GET'])
def changePoints():
    if request.method == 'GET':
        return render_template('change_points.html')
     
    if request.method == 'POST':
        pointsChange = request.form.get('points', type=int)
        reason=request.form['reason']
        sname = request.form['sname']

        uid = session['uid']
        if session['changeid'] != None :
            uid = session['changeid']

        cursor = mysql.connection.cursor()

        val = (sname, uid)
        sql = "SELECT DriverName FROM driversponsorassociations WHERE SponsorName = %s AND DriverID = %s"
        cursor.execute(sql, val)
        name = cursor.fetchone()[0]

        sql = "SELECT DriverPoints FROM driversponsorassociations WHERE SponsorName = %s AND DriverID = %s"
        cursor.execute(sql, val)
        points = cursor.fetchone()[0]

        points = points + pointsChange

        sql = "UPDATE driversponsorassociations SET DriverPoints = %s WHERE SponsorName = %s AND DriverID = %s"
        val = (points, sname, uid)
        cursor.execute(sql, val)

        sql = "INSERT INTO points (PointDate, PointSponsorName, PointDriverName, PointChange, PointTotal, PointReason) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (date.today(), sname, name, pointsChange, points, reason)
        cursor.execute(sql, val)


        mysql.connection.commit()
        cursor.close()

        session.pop('changeid', None)

        return home()