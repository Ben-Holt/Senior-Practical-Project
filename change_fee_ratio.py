from FlaskImport import *
from home import home

@app.route('/change_fee_ratio', methods = ['POST', 'GET'])
def change_fee_ratio() :
    
    cursor = mysql.connection.cursor()
     
    if request.method == 'POST':
        ratio = request.form.get('ratio', type=float)
        uid = session['uid']

        sql = "SELECT UserAffiliation FROM users WHERE UserID = %s"
        cursor.execute(sql, (uid,))
        sname = cursor.fetchone()[0]

        val = (ratio, sname)
        sql = "UPDATE organizations SET OrganizationPointValue = %s WHERE OrganizationName = %s"
        cursor.execute(sql,val)
        mysql.connection.commit()
        cursor.close()
        return home()