from FlaskImport import *

@app.route('/points_driver', methods = ['POST', 'GET'])
def points_driver():
    cursor = mysql.connection.cursor()
    uid = session["uid"]
    sql = "SELECT UserPoints FROM users WHERE UserID = %s"
    val = (uid, )
    cursor.execute(sql, val)
    points = cursor.fetchone()[0]
    return render_template('points_driver.html', points=points)