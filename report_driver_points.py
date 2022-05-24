# from __main__ import app
from FlaskImport import *
from home import home

@app.route('/report_driver_points', methods = ['POST', 'GET'])
def report_driver_points():
    cursor = mysql.connection.cursor()

    if request.method == 'GET':

        return render_template("report_driver_points_settings.html")
    
    if request.method == 'POST':
        start = request.form.get('start')
        end = request.form.get('end')
        name = request.form['name']
        report = request.form['csv']
        cursor = mysql.connection.cursor()

        val=(name,start,end)
        sql = "SELECT PointDriverName, PointTotal, PointChange, PointDate, PointSponsorName, PointReason FROM points WHERE PointDriverName = %s AND PointDate BETWEEN %s AND %s"
        cursor.execute(sql, val)
        points = cursor.fetchall()

        if(report=='yes') :
            f = open('reports/driver_points_one.csv', 'w')
            fieldnames=['PointDriverName', 'PointTotal', 'PointChange', 'PointDate', 'PointSponsorName', 'PointReason']
            writer = csv.writer(f)
            writer.writerow(fieldnames)                    
            writer.writerow(points)
            f.close()

        return render_template("report_driver_points.html", points=points)