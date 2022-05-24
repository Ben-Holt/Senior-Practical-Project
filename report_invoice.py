# from __main__ import app
from FlaskImport import *
from home import home
import collections

@app.route('/invoice', methods = ['POST', 'GET'])
def invoice():
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        
        sql = "SELECT OrganizationName FROM organizations"
        cursor.execute(sql)
        names = cursor.fetchall()
        all = ("All",)
        all_tuple= (all,)
        snames=names+all_tuple
        return render_template("report_invoice_settings.html", snames=snames)
    
    if request.method == 'POST':
        start = request.form.get('start')
        end = request.form.get('end')
        sname = request.form['sname']
        report = request.form['csv']
        cursor = mysql.connection.cursor()

        if sname=="All" :
            
            sql="SELECT SponsorName from purchases GROUP BY SponsorName"
            cursor.execute(sql)
            orgs = cursor.fetchall()

            purchases={'':''}
            costs={'':''}


            if(report=='yes') :
                f = open('reports/invoice.csv', 'w')
                fieldnames=['DriverName', 'SponsorName', 'PurchaserName', 'ProductActualCost', 'ProductPointCost', 'DateOfPurchase', 'PurchaseStatus', 'ProductName']
                writer = csv.writer(f)

            for org in orgs :
                val=(start,end,org)
                sql = "SELECT DriverName, SponsorName, PurchaserName, ProductActualCost, ProductPointCost, DateOfPurchase, PurchaseStatus, ProductName FROM purchases WHERE DateOfPurchase BETWEEN %s AND %s AND SponsorName=%s"
                cursor.execute(sql, val)
                purchases[org]=(cursor.fetchall())

                sql = "SELECT SUM(ProductActualCost) FROM purchases WHERE DateOfPurchase BETWEEN %s AND %s AND SponsorName=%s"
                cursor.execute(sql, val)
                costs[org]=(cursor.fetchone()[0])

                if(report=='yes') :
                    writer.writerow(fieldnames)                    
                    writer.writerow(purchases[org])
                    writer.writerow(costs)

            if(report=='yes') :                
                f.close()
            return render_template("report_invoice_all.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs, orgs=orgs)

        else: 

            val=(sname,start,end)
            sql = "SELECT DriverName, SponsorName, PurchaserName, ProductActualCost, ProductPointCost, DateOfPurchase, PurchaseStatus, ProductName FROM purchases WHERE SponsorName = %s AND DateOfPurchase BETWEEN %s AND %s"
            cursor.execute(sql, val)
            purchases = cursor.fetchall()
            
            sql = "SELECT SUM(ProductActualCost) FROM purchases WHERE SponsorName = %s AND DateOfPurchase BETWEEN %s AND %s"
            cursor.execute(sql, val)
            costs = cursor.fetchone()[0]

            if(report=='yes') :
                f = open('reports/invoice_one.csv', 'w')
                fieldnames=['DriverName', 'SponsorName', 'PurchaserName', 'ProductActualCost', 'ProductPointCost', 'DateOfPurchase', 'PurchaseStatus', 'ProductName']
                writer = csv.writer(f)
                writer.writerow(fieldnames)                    
                writer.writerow(purchases)
                f.close()

            return render_template("report_invoice.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs)







