from FlaskImport import *

@app.route('/driver_cart', methods = ['POST', 'GET'])
def driver_cart():
        itemIDList = []
        if request.method == 'POST':
                print("adding item to cart")
                cursor = mysql.connection.cursor()
                itemID = str(request.form["item_id"])
                itemIDList.append(itemID)
                sql = "SELECT * FROM products where ProductID = %s"
                val = itemID
                cursor.execute(sql, [val])
                newItem = cursor.fetchone()
                cursor.close()

                cursor = mysql.connection.cursor()
                sql = "INSERT INTO carts (UserID, ProductID, ProductName, ProductPrice, ProductDescription, ProductNumberInInventory) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (str(session["uid"]), str(newItem[0]), str(newItem[1]), str(int(float(newItem[2]) * 100)), str(newItem[3]), str(newItem[4]))
                cursor.execute(sql, val)
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
        for item in cart:
                price = price + int(item[3])
                itemList.append(item[2])

                


        return render_template('driver_cart.html', price=price, itemList=itemList, itemIDList=itemIDList)