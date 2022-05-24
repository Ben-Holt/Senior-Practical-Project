from FlaskImport import *

@app.route('/driver_cart_remove', methods = ['POST', 'GET'])
def driver_cart_remove():
        if request.method == 'POST':
                print("deleting item from cart")

                cursor = mysql.connection.cursor()
                sql = "DELETE FROM carts WHERE ProductName LIKE %s"
                val = str(request.form["item_id"])
                val = '%' + val + '%'
                
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