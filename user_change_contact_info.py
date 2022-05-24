from FlaskImport import *
from home import home

@app.route('/contact', methods = ['POST', 'GET'])
def contact():
    return render_template('contact.html')
 
@app.route('/contactChange', methods = ['POST', 'GET'])
def contactChange():
    if request.method == 'GET':
        return "Change Contact Information with Form"
     
    if request.method == 'POST':
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        cursor = mysql.connection.cursor()
        uid = session['uid']

        if session.get('changeid') != None :
            uid = session['changeid']

        sql = "UPDATE users SET UserAddress = %s, UserEmail = %s, UserPhone = %s WHERE UserID = %s"
        val = (address, email, phone, uid)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        session.pop('changeid', None)

        return home()
