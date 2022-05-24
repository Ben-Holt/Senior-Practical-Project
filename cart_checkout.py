from FlaskImport import *
from datetime import date

@app.route('/cart_checkout', methods = ['POST', 'GET'])
def cart_checkout():

        if request.method == 'POST':
                print("adding cart items to purchased table")
                
                # Copy items in cart table to purchases table
                today = date.today()
                cursor = mysql.connection.cursor()
                sql = "INSERT INTO purchases (BeneficiaryID, ProductName, ProductPointCost, DateOfPurchase, PurchaseStatus) SELECT UserID, ProductName, ProductPrice, %s, %s FROM carts WHERE UserID = %s"
                val = (str(today), "Complete", str(session["uid"]))
                cursor.execute(sql, val)
                mysql.connection.commit()

                # Decrement user points
                sql = "SELECT UserPoints FROM users WHERE UserID = %s"
                val = str(session["uid"])
                cursor.execute(sql, (val,))
                currentpoints = cursor.fetchone()[0]
                newpoints = currentpoints - int(request.form["points"])

                sql = "UPDATE users SET UserPoints = %s WHERE UserID = %s"
                val = (str(newpoints), str(session["uid"]))
                cursor.execute(sql, val)
                mysql.connection.commit()

                # Clear the cart
                print("removing items from cart")
                sql = "DELETE FROM carts WHERE UserID = %s"
                val = str(session["uid"])
                
                cursor.execute(sql, (val,))
                mysql.connection.commit()
                cursor.close()
        
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM carts where UserID = %s"
        val = str(session["uid"])
        cursor.execute(sql, [val])
        cart = cursor.fetchall()

        cursor.close()

        print(cart)

        price = 0
        itemList = []
        itemIDList = []
        for item in cart:
                price = price + int(item[3])
                itemList.append(item[2])

                


        return render_template('driver_cart.html', price=price, itemList=itemList, itemIDList = itemIDList)