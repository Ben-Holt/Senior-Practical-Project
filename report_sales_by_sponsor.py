# from __main__ import app
from FlaskImport import *
from home import home
import collections

@app.route('/sales_by_sponsor', methods = ['POST', 'GET'])
def sales_by_sponsor():
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        
        sql = "SELECT OrganizationName FROM organizations"
        cursor.execute(sql)
        names = cursor.fetchall()
        all = ("All",)
        all_tuple= (all,)
        snames=names+all_tuple
        return render_template("report_sales_by_sponsor_settings.html", snames=snames)
    
    if request.method == 'POST':
        start = request.form.get('start')
        end = request.form.get('end')
        sname = request.form['sname']
        category = request.form['category']
        report = request.form['csv']
        cursor = mysql.connection.cursor()

        if sname=="All" :
            sql="SELECT PurchaserName from purchases WHERE SponsorID IS NOT NULL GROUP BY PurchaserName"
            cursor.execute(sql)
            orgs = cursor.fetchall()

            purchases={'':''}
            costs={'':''}

            if(report=='yes') :
                f = open('reports/sales_by_sponsor.csv', 'w')
                fieldnames=['DriverName', 'SponsorName', 'PurchaserName', 'ProductActualCost', 'ProductPointCost', 'DateOfPurchase', 'PurchaseStatus', 'ProductName']
                writer = csv.writer(f)
            
            for org in orgs :
                val=(start,end,org)
                sql = "SELECT DriverName, SponsorName, PurchaserName, ProductActualCost, ProductPointCost, DateOfPurchase, PurchaseStatus, ProductName FROM purchases WHERE SponsorID IS NOT NULL AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s"
                cursor.execute(sql, val)
                purchases[org]=(cursor.fetchall()) 

                sql = "SELECT SUM(ProductActualCost) FROM purchases WHERE SponsorID IS NOT NULL AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s"
                cursor.execute(sql, val)
                costs[org]=(cursor.fetchone()[0])

                if(report=='yes') :
                    writer.writerow(fieldnames)                    
                    writer.writerow(purchases[org])
                    writer.writerow(costs)

            if(report=='yes') :                
                f.close()

            if category == "detailed" :
                return render_template("report_sales_by_sponsor_detailed_all.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs, orgs=orgs)
            else :
                return render_template("report_sales_by_sponsor_all.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs, orgs=orgs)

        else:
            val=(sname,start,end,sname)
            sql = "SELECT DriverName, SponsorName, PurchaserName, ProductActualCost, ProductPointCost, DateOfPurchase, PurchaseStatus, ProductName FROM purchases WHERE SponsorName = %s AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s"
            cursor.execute(sql, val)
            purchases = cursor.fetchall()
            
            sql = "SELECT SUM(ProductActualCost) FROM purchases WHERE SponsorName = %s AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s"
            cursor.execute(sql, val)
            costs = cursor.fetchone()[0]
            
            if(report=='yes') :
                f = open('reports/sales_by_sponsor_one.csv', 'w')
                fieldnames=['DriverName', 'SponsorName', 'PurchaserName', 'ProductActualCost', 'ProductPointCost', 'DateOfPurchase', 'PurchaseStatus', 'ProductName']
                writer = csv.writer(f)
                writer.writerow(fieldnames)                    
                writer.writerow(purchases)
                f.close()

        if category == "detailed" :
            return render_template("report_sales_by_sponsor_detailed.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs)
        else :
            return render_template("report_sales_by_sponsor.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs)


