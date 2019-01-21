<h1>ShopifyStore Challenge: <em>Working Checkout Purchase API solution for Summer 2019 Internship Challenge</em></h1>


by: Aman Adhav <a href="https://linkedin.com/in/amanadhav"><img src="https://raw.githubusercontent.com/jrobchin/phormatics/master/screenshots/linkedin.png" height="20px"></a> <a href="https://github.com/dreamincodeforlife"><img src="https://raw.githubusercontent.com/jrobchin/phormatics/master/screenshots/github.png" height="20px"></a>

[Shopify 2019](https://www.shopify.com/careers/) API developed focusing on using Checkout, Purchasing, Admin right, and creating a tested solution.
Key Points to Highlight : 
Implementation List :
- Task: Build the barebones of an online marketplace.

To do this, build a server side web api that can be used to fetch products either one at a time or all at once.
Every product should have a title, price, and inventory_count.

Querying for all products should support passing an argument to only return products with available inventory. 

Products should be able to be "purchased" which should reduce the inventory by 1. Products with no inventory cannot be purchased.

- Fit these product purchases into the context of a simple shopping cart. 

That means purchasing a product requires first creating a cart, adding products to the cart, and then "completing" the cart.
The cart should contain a list of all included products, a total dollar amount (the total value of all products), and product inventory shouldn't reduce until after a cart has been completed.

- Bonus points for making your API (at least partly) secure, writing documentation that doesn’t suck, including unit tests,
 

### Flask API:
This app runs as an API built with Flask. Endpoints and locally hosted sever with queries is performed by the [Flask](http://flask.pocoo.org/) API.

### Currently Supported Functions:

- add-item: *Add Item to the collection registered_items in DB ShopifyStore*
- update_item: *Update Item to the collection registered_items in DB ShopifyStore.*
- show_all: *List of all current items in ShopifyStore (Collection registered_items)*
- filter_by_item : *View Items in ShopifyStore in various orders including : highest-lowest price, lowest-highest price, highest-lowest quantity, lowest-highest quantity*
- purchase : *Make a Purchase of given quantity for a particular item*
- checkout : *Add items to a cart (collection checked_item)*
- checkout_total : *List of all current items in Checkout window with a subtotal*
### Usage:

You'll need a few things:

* [Python 3.5.0+](https://www.python.org/downloads/)
* [MongoDB 4.0](https://www.mongodb.com/mongodb-4.0), current database is localhost mongodb running on 27017 port
* [NGROK](https://ngrok.com/), only required for testing when making API public
* [Git](https://git-scm.com/), to clone this repository
* [Postman](https://www.getpostman.com/), necessary for initial testing purposes

First we must install the python dependencies Via pip. We assume that you have Git, Python, MongoDB, Postman and NGROK installed. If you don't, please visit the links above to install them.

First, clone the git repository:
```
$ git clone https://github.com/dreamInCoDeforlife/ShopifyChallenge-AmanAdhav.git
```

Then, cd into the repository:
```
$ cd ShopifyChallenge-AmanAdhav
```

Install all dependencies inside requirements.txt file for python:
```
$ pip install requirements.txt
```

Now let's initialize the flask application:
```
$ python app.py
```

After that, you should get a response that looks something like this:

```
$ FLASK_APP=demoo.py flask run
 * Running on http://localhost:5000/
```
Now we can turn this private local API public with NGROK:

```
$ ngrok https 5000
ngrok by @inconshreveable                                                                               (Ctrl+C to quit)

Session Status                online
Session Expires               7 hours, 59 minutes
Version                       2.2.8
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://58a205b8.ngrok.io -> localhost:5000
Forwarding                    https://58a205b8.ngrok.io -> localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```
Note : The url address changes every 7 hours.


### Interacting with the API:
For this tutorial I will make the API requests using cURL and briefly highlight how each function works

* Start Up and endpoints : 
    API will be running on port 5000 
```
if __name__ == '__main__':
    from argparse import ArgumentParser   
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type = int, help = 'port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port = port)
 ```
 For usage the url for communicating with the API would be http:\\localhost:5000/query
 
 * /add-item
Add Item to the collection registered_items in DB ShopifyStore.
    REST Call : POST Message
    Post Request Attributes

        ===== Attributes =====
        item : Name of the Item 
        price : Price of the Given Item
        Quantity : Quantity supplied for the given state of the item
        id : Only admins with User Id 1287498729198 can use this command
        
        Preconditions:
            Assume User ID 1287498729198 exists
        
        Throws Exception :  
        If all Attributes are not provided -> return value is Invalid Entry
        If userId is not 1287498729198 -> return value is Error: Unauthorized User Cannot add to database
        If item is just an empty string "" -> return value is Invalid item name : Name cannot be an empty string
        If item already exists in the collection -> return value is Item is already in this system! Use the update function to change items values
 
 POST REQUEST:
 ```
 curl -X POST \
  http://localhost:5000/add-item \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "item": "Granny Smith Aples", "price" : 10, "quantity": 100, "uID": "1287498729198"
}'
 ```
 
 * /update_item
 Update Item to the collection registered_items in DB ShopifyStore.
    REST Call : POST Message
    Post Request Attributes

        ===== Attributes =====
        item : Name of the Item 
        price : Changed Price of the Given Item
        Quantity : Changed Quanitity supplied for the given state of the item
        id : Only admins with User Id 1287498729198 can use this command
        
        Preconditions:
            Assume User ID 1287498729198 exists
        
        Throws Exception :  
        If all Attributes are not provided -> return value is Invalid Entry
        If userId is not 1287498729198 -> return value is Error: Unauthorized User Cannot add to database
        If item is just an empty string "" -> return value is Invalid item name : Name cannot be an empty string
        If item does not exist in collection -> return value is Cannot Update Item that does not exist! Please check the item name! Or use the /add-item command
 
 POST REQUEST : 
 ```
 curl -X POST \
  http://localhost:5000/update-item \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
  "item": "Granny Smith Apples", "price" : 7, "quantity": 50, "uID": "1287498729198"
}'
```

* /all-items 
List of all current items in ShopifyStore (Collection registered_items)
    REST Call : GET Message
    Post Request Attributes

        ===== Attributes =====
        None
        
        Return Type :
        List of all the values in Collection

 GET REQUEST : 
 ```
 curl -X GET \
  http://localhost:5000/all-items \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
	"item_name": "Granny Smith Apples", "quantity": 15
}'
```

* /fetch-items
View Items in ShopifyStore in various orders including : highest-lowest price, lowest-highest price, highest-lowest quantity, lowest-highest quantity
    REST Call : POST Message
    Post Request Attributes

        ===== Attributes =====
        filter_type : Order of sorting for values in Collection (highest-lowest price, lowest-highest price, highest-lowest quantity, lowest-highest quantity)
        name_search : Fiter names of items with key words such as 'Apples in Granny Smith Apples, or Apple play book' both these items will be returned becuase of filter 'Apple'
        
        
        Throws Exception :  
        If all Attributes are not provided -> return value is Invalid Entry
        
        Return Type : 
        List of all items with a particular filter in a particular order 
        Example : 
        POST Message 
       {
	"filter_type": "lowest-highest price", "provided_name": "Granny" 
        }
        Return : 
        [{'_id': ObjectId('5c440a45dda55f106ccd1328'), 'item_name': 'Granny Smith Apples', 'price': 7, 'quantity': 20},
        {'_id': ObjectId('5c440ef4dda55f1254cd9820'), 'item_name': 'Granny Smasdfth Apples', 'price': 7, 'quantity': 50}, 
        {'_id': ObjectId('5c440efbdda55f1254cd9821'), 'item_name': 'Granny Smah Apples', 'price': 7, 'quantity': 50}, 
        {'_id': ObjectId('5c440a51dda55f106ccd1329'), 'item_name': 'Granny Smith Aples', 'price': 10, 'quantity': 100}]
        
        Values sorted from lowest to highest with key name filter Granny in them
 
 POST REQUEST:
 ```
 curl -X POST \
  http://localhost:5000/fetch-items \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
	"filter_type": "lowest-highest price", "provided_name": "Granny" 
}'
```

* /purchase-item
Make a Purchase of given quantity for a particular item
    REST Call : POST Message
    Post Request Attributes

        ===== Attributes =====
        purchased_item : Name of item user wants to purchase
        purchased_quantity : Quantity user wishes to purchase


        Throws Exception :  
        If all Attributes are not provided -> return value is Invalid Entry
        If quantity requested exceeds quantity in ShopifyStore -> return value Error : Purchase exceeds quantity limit! Cannot execute order
        If item does not exist in collection -> return value is Cannot Update Item that does not exist! Please check the item name! Or use the /add-item command
        
 POST REQUEST : 
 ```
 curl -X POST \
  http://localhost:5000/purchase-item \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
	"item_name": "Granny Smith Apples", "quantity": 15
}'
```

* /add-to-cart
Add items to a cart (collection checked_item) 
    REST Call : POST Message
    Post Request Attributes

        ===== Attributes =====
        checked_item : Name of item user wants to purchase/add to cart
        checked_quantity : Quantity user wishes to purchase/add to cart
        checked_price : Price of item 


        Throws Exception :  
        If all Attributes are not provided -> return value is Invalid Entry
        If quantity requested exceeds quantity in ShopifyStore -> return value Error : Purchase exceeds quantity limit! Cannot execute order
        If item does not exist in collection -> return value is Cannot checkout item that does not exist! Please check the item name! Or use the /add-item command
        If Quantity being added exceeds the quantity in collection registered_items -> return value is Error : Checkout exceeds quantity limit! Cannot add to order
        
 POST REQUEST : 
 ```
 curl -X POST \
  http://localhost:5000/add-to-cart \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{
	"item_name": "Granny Smith Apples", "item_price": 7, "quantity": 15
}'
```

* /checkout-total
List of all current items in Checkout window 
    REST Call : GET Message
    Post Request Attributes

        ===== Attributes =====
        None
        
        Return Type :
        List of all the values in Collection
 
 GET REQUEST:
 ```
 curl -X GET \
  http://localhost:5000/add-to-cart \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
 ```