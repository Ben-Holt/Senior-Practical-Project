# from __main__ import app
from unicodedata import category
from FlaskImport import *
from home import home

@app.route('/auditLog', methods = ['POST', 'GET'])
def auditLog():
    cursor = mysql.connection.cursor()

    if request.method == 'GET':

        sql = "SELECT OrganizationName FROM organizations"
        cursor.execute(sql)
        names = cursor.fetchall()
        all = ("All",)
        all_tuple= (all,)
        snames=names+all_tuple
        return render_template("auditLog_settings.html", snames=snames)
    
    if request.method == 'POST':
        start = request.form.get('start')
        end = request.form.get('end')
        sname = request.form['sname']
        category = request.form['category']
        report = request.form['csv']    
        cursor = mysql.connection.cursor()


        if sname == 'All' :
            
            val = (start, end)
            sql = "SELECT ApplicationDate, ApplicationSponsorName, ApplicationDriverName, ApplicationDriverID, ApplicationStatus, ApplicationReason FROM applications WHERE ApplicationDate BETWEEN %s AND %s"
            cursor.execute(sql, val)
            applications = cursor.fetchall()

            sql = "SELECT PointDate, PointChange, PointDriverName, PointSponsorName, PointTotal, PointReason FROM points WHERE PointDate BETWEEN %s AND %s"
            cursor.execute(sql, val)
            points = cursor.fetchall()

            sql = "SELECT LogPasswordDate, LogDriverName, LogPasswordTypeChange FROM logs WHERE LogPasswordDate BETWEEN %s AND %s"
            cursor.execute(sql, val)
            passChanges = cursor.fetchall()
            
            sql = "SELECT LoginUsername, LoginDate, LoginSuccessful FROM logins WHERE LoginDate BETWEEN %s AND %s"
            cursor.execute(sql, val)
            logins = cursor.fetchall()

            if category=='applications':
                if(report=='yes') :
                    f = open('reports/audit_log_applications_all.csv', 'w')
                    fieldnames=['ApplicationDate', 'ApplicationSponsorName', 'ApplicationDriverName', 'ApplicationDriverID', 'ApplicationStatus', 'ApplicationReason']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)                    
                    writer.writerow(applications)
                    f.close()
                return render_template("auditLog_applications.html", logs=applications)

            if category=='points':
                if(report=='yes') :
                    f = open('reports/audit_log_points_all.csv', 'w')
                    fieldnames=['PointDate', 'PointChange', 'PointDriverName', 'PointSponsorName', 'PointTotal', 'PointReason']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)                    
                    writer.writerow(points)
                    f.close()
                return render_template("auditLog_points.html", logs=points)

            if category=='passwords':
                if(report=='yes') :
                    f = open('reports/audit_log_passwords_all.csv', 'w')
                    fieldnames=['LogPasswordDate', 'LogDriverName', 'LogPasswordTypeChange']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)                    
                    writer.writerow(passChanges)
                    f.close()
                return render_template("auditLog_passwords.html", logs=passChanges)

            if category=='logins':
                if(report=='yes') :
                    f = open('reports/audit_log_logins_all.csv', 'w')
                    fieldnames=['LoginUsername', 'LoginDate', 'LoginSuccessful']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)                    
                    writer.writerow(logins)
                    f.close()
                return render_template("auditLog_logins.html", logs=logins)
            
            return render_template("auditLog.html")

        else:
        
            val = (sname, start, end)
            sql = "SELECT ApplicationDate, ApplicationSponsorName, ApplicationDriverName, ApplicationDriverID, ApplicationStatus, ApplicationReason FROM applications WHERE ApplicationSponsorName=%s AND ApplicationDate BETWEEN %s AND %s"
            cursor.execute(sql, val)
            applications = cursor.fetchall()

            sql = "SELECT PointDate, PointChange, PointDriverName, PointSponsorName, PointTotal, PointReason FROM points WHERE PointSponsorName=%s AND PointDate BETWEEN %s AND %s"
            cursor.execute(sql, val)
            points = cursor.fetchall()

            sql = "SELECT DriverID FROM driversponsorassociations WHERE SponsorName=%s"
            cursor.execute(sql, (sname,))
            ids = cursor.fetchall()

            sql = "SELECT UserName FROM users WHERE UserID IN %s"
            cursor.execute(sql, [ids])
            ids = cursor.fetchall()
            
            val=(start,end)
            sql = "SELECT LogPasswordDate, LogDriverName, LogPasswordTypeChange FROM logs WHERE LogPasswordDate BETWEEN %s AND %s"
            cursor.execute(sql, val)
            passChanges = cursor.fetchall()
            
            sql = "SELECT LoginUsername, LoginDate, LoginSuccessful FROM logins WHERE LoginDate BETWEEN %s AND %s"
            cursor.execute(sql, val)
            logins = cursor.fetchall()

            if category=='applications':
                if(report=='yes') :
                    f = open('reports/audit_log_applications_one.csv', 'w')
                    fieldnames=['ApplicationDate', 'ApplicationSponsorName', 'ApplicationDriverName', 'ApplicationDriverID', 'ApplicationStatus', 'ApplicationReason']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)                    
                    writer.writerow(applications)
                    f.close()
                return render_template("auditLog_applications.html", logs=applications)

            if category=='points':
                if(report=='yes') :
                    f = open('reports/audit_log_points_one.csv', 'w')
                    fieldnames=['PointDate', 'PointChange', 'PointDriverName', 'PointSponsorName', 'PointTotal', 'PointReason']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)                    
                    writer.writerow(points)
                    f.close()
                return render_template("auditLog_points.html", logs=points)

            if category=='passwords':
                if(report=='yes') :
                    f = open('reports/audit_log_passwords_one.csv', 'w')
                    fieldnames=['LogPasswordDate', 'LogDriverName', 'LogPasswordTypeChange']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)                    
                    writer.writerow(passChanges)
                    f.close()
                return render_template("auditLog_passwords.html", logs=passChanges)

            if category=='logins':
                if(report=='yes') :
                    f = open('reports/audit_log_logins_one.csv', 'w')
                    fieldnames=['LoginUsername', 'LoginDate', 'LoginSuccessful']
                    writer = csv.writer(f)
                    writer.writerow(fieldnames)                    
                    writer.writerow(logins)
                    f.close()
                return render_template("auditLog_logins.html", logs=logins)

            return render_template("auditLog.html")