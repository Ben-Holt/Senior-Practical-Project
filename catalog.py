# from FlaskImport import *

from FlaskImport import *
import requests

# getRequest = requests.get("https://openapi.etsy.com/v2/listings/active?api_key=h7ctibmsc63qthr5ozej14i4")

# response = getRequest.json()

# products = ""

# for i in (response["results"]):
#         products = products + i["title"]

@app.route('/catalog', methods = ['POST', 'GET'])
def catalog():
        return render_template('catalog.html')

