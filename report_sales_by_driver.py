# from __main__ import app
from FlaskImport import *
from home import home

@app.route('/sales_by_driver', methods = ['POST', 'GET'])
def sales_by_driver():
    cursor = mysql.connection.cursor()

    if request.method == 'GET':
        
        sql = "SELECT OrganizationName FROM organizations"
        cursor.execute(sql)
        names = cursor.fetchall()
        all = ("All",)
        all_tuple= (all,)
        snames=names+all_tuple
        return render_template("report_sales_by_driver_settings.html", snames=snames)
    
    if request.method == 'POST':
        start = request.form.get('start')
        end = request.form.get('end')
        sname = request.form['sname']
        category = request.form['category']
        dname = request.form['dname']
        report = request.form['csv']
        cursor = mysql.connection.cursor()

        if sname=="All" :
            
            purchases={'':''}
            costs={'':''}

            sql="SELECT PurchaserName from purchases WHERE SponsorID IS NULL GROUP BY PurchaserName"
            cursor.execute(sql)
            drivers = cursor.fetchall()

            if(report=='yes') :
                f = open('reports/sales_by_driver_all_sponsors.csv', 'w')
                fieldnames=['DriverName', 'SponsorName', 'PurchaserName', 'ProductActualCost', 'ProductPointCost', 'DateOfPurchase', 'PurchaseStatus', 'ProductName']
                writer = csv.writer(f)

            for driver in drivers :
                val=(start,end,driver)
                sql = "SELECT DriverName, SponsorName, PurchaserName, ProductActualCost, ProductPointCost, DateOfPurchase, PurchaseStatus, ProductName FROM purchases WHERE SponsorID IS NULL AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s"
                cursor.execute(sql, val)
                purchases[driver]=(cursor.fetchall()) 

                sql = "SELECT SUM(ProductActualCost) FROM purchases WHERE SponsorID IS NULL AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s"
                cursor.execute(sql, val)
                costs[driver]=(cursor.fetchone()[0])

                if(report=='yes') :
                    writer.writerow(fieldnames)                    
                    writer.writerow(purchases[driver])
                    writer.writerow(costs)

            if(report=='yes') :                
                f.close()

            if category == "detailed" :
                return render_template("report_sales_by_driver_detailed_all.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs, drivers=drivers)
            else :
                return render_template("report_sales_by_driver_all.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs, drivers=drivers)

        else: 
            if dname == 'All' :
                sql="SELECT PurchaserName from purchases WHERE SponsorID IS NULL AND SponsorName=%s GROUP BY PurchaserName"
                cursor.execute(sql, (sname,))
                drivers = cursor.fetchall()

                purchases={'':''}
                costs={'':''}

                if(report=='yes') :
                    f = open('reports/sales_by_driver_all_drivers_in_sponsor.csv', 'w')
                    fieldnames=['DriverName', 'SponsorName', 'PurchaserName', 'ProductActualCost', 'ProductPointCost', 'DateOfPurchase', 'PurchaseStatus', 'ProductName']
                    writer = csv.writer(f)

                for driver in drivers :
                    val=(start,end,driver,sname)
                    sql = "SELECT DriverName, SponsorName, PurchaserName, ProductActualCost, ProductPointCost, DateOfPurchase, PurchaseStatus, ProductName FROM purchases WHERE SponsorID IS NULL AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s AND SponsorName=%s"
                    cursor.execute(sql, val)
                    purchases[driver]=(cursor.fetchall()) 

                    sql = "SELECT SUM(ProductActualCost) FROM purchases WHERE SponsorID IS NULL AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s AND SponsorName=%s"
                    cursor.execute(sql, val)
                    costs[driver]=(cursor.fetchone()[0])

                    if(report=='yes') :
                        writer.writerow(fieldnames)                    
                        writer.writerow(purchases[driver])
                        writer.writerow(costs)

                if(report=='yes') :                
                    f.close()

                if category == "detailed" :
                    return render_template("report_sales_by_driver_detailed_all.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs, drivers=drivers)
                else :
                    return render_template("report_sales_by_driver_all.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs, drivers=drivers)

            else:
                sql="SELECT * from driversponsorassociations WHERE DriverName=%s AND SponsorName=%s"
                val=(dname, sname)
                if(cursor.execute(sql,val)) :
                    val=(sname,start,end,dname)
                    sql = "SELECT DriverName, SponsorName, PurchaserName, ProductActualCost, ProductPointCost, DateOfPurchase, PurchaseStatus, ProductName FROM purchases WHERE SponsorName = %s AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s"
                    cursor.execute(sql, val)
                    purchases = cursor.fetchall()
                    
                    sql = "SELECT SUM(ProductActualCost) FROM purchases WHERE SponsorName = %s AND DateOfPurchase BETWEEN %s AND %s AND PurchaserName=%s"
                    cursor.execute(sql, val)
                    costs = cursor.fetchone()[0]

                    if(report=='yes') :
                        f = open('reports/sales_by_driver_one.csv', 'w')
                        fieldnames=['DriverName', 'SponsorName', 'PurchaserName', 'ProductActualCost', 'ProductPointCost', 'DateOfPurchase', 'PurchaseStatus', 'ProductName']
                        writer = csv.writer(f)
                        writer.writerow(fieldnames)                    
                        writer.writerow(purchases)
                        f.close()

                    if category == "detailed" :
                        return render_template("report_sales_by_driver_detailed.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs)
                    else :
                        return render_template("report_sales_by_driver.html", purchases=purchases, start=start, end=end, sname=sname, costs=costs)

                else:
                    sql = "SELECT OrganizationName FROM organizations"
                    cursor.execute(sql)
                    names = cursor.fetchall()
                    all = ("All",)
                    all_tuple= (all,)
                    snames=names+all_tuple
                    err="Driver Is Not In Selected Sponsor"
                    return render_template("report_sales_by_driver_settings.html", snames=snames,err=err)













