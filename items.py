from FlaskImport import *
import requests
import json

@app.route('/items', methods = ['POST', 'GET'])
def items():

        getRequest = requests.get("https://openapi.etsy.com/v2/listings/active?api_key=h7ctibmsc63qthr5ozej14i4")

        response = getRequest.json()

        cursor = mysql.connection.cursor()

        sql = "SELECT ProductID FROM products"
        cursor.execute(sql)
        newItems = cursor.fetchall()
        items = [item for tuple in newItems for item in tuple]
        cursor.close()

        for product in (response["results"]):
                if (product["listing_id"] not in items and (bool(product.get('title')))):
                        cursor = mysql.connection.cursor()
                        sql = "INSERT INTO products (ProductID, ProductName, ProductPrice, ProductDescription, ProductNumberInInventory) VALUES (%s, %s, %s, %s, %s)"
                        val = (str(product["listing_id"]), product["title"], str(product["price"]), product["description"], str(product["quantity"]))
                        cursor.execute(sql, val)
                        mysql.connection.commit()
                        cursor.close()
        

        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM products"
        cursor.execute(sql)
        response = cursor.fetchall()
        cursor.close()

        catalog = []
        for item in response[:100]:
                catalog.append([item[0], item[1], int(item[2]*100), item[4]])

        return json.dumps(catalog)