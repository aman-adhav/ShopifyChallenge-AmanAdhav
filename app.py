"""Shopify API Mock Store Backend & Production Engineer Challenge
=== Module description ===
This file is the flask api for the 2019 - Shopify Student Developer Challenge
DB : MongoDB
Dependencies : Check 'requirements.txt' in file path

***Both Extra Credit Critrea have been met***
"""


import requests
from flask_cors import CORS
from flask import Flask, jsonify, request
import math
import pymongo

'''
Initialize Flask under function '__name__' (check lines 221)
MongoDB is being run on port 27017 for local builds.
The Database name we will refer to will be called ShopifyStore

'''
app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)
mydb = client["ShopifyStore"]


"""Add Item to the collection registered_items in DB ShopifyStore.
    REST Call : POST Message
    Post Request Attributes

        ===== Attributes =====
        item : Name of the Item 
        price : Price of the Given Item
        Quantity : Quanitity supplied for the given state of the item
        id : Only admins with User Id 1287498729198 can use this command
        
        Preconditions:
            Assume User ID 1287498729198 exists
        
        Throws Exception :  
        If all Attributes are not provided -> return value is Invalid Entry
        If userId is not 1287498729198 -> return value is Error: Unauthorized User Cannot add to database
        If item is just an empty string "" -> return value is Invalid item name : Name cannot be an empty string
        If item already exists in the collection -> return value is Item is already in this system! Use the update function to change items values
    
        """
@app.route('/add-item', methods=['POST'])
def add_item():
    try:
        values = request.get_json()
        item = values['item']
        price = values['price']
        quantity = values['quantity']
        id = values['uID']
    except:
        return "Invalid Entry"
    if id != "1287498729198":
        return "Error: Unauthorized User Cannot add to database", 200
    if item == "":
        return "Invalid item name : Name cannot be an empty string", 200
    
    register_item = mydb["registered_items"]
    myQuery = {"item_name" : item}
    mydoc = register_item.find(myQuery)
    temp_array = [x for x in mydoc]
    if len(temp_array) > 0 :
        return "Item is already in this system! Use the update function to change items values", 200
    elif len(temp_array) == 0:   
        response = {
            "item_name" : item,
            "price" : price,
            "quantity" : quantity
         }
        register_item.insert_one(response)
        return "Success", 200

"""Update Item to the collection registered_items in DB ShopifyStore.
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
    
        """
@app.route('/update-item', methods=['POST'])
def update_item():
    try:
        values = request.get_json()
        item = values['item']
        changed_price = values['price']
        changed_quantity = values['quantity']
        id = values['uID']
    except:
        return "Invalid Entry"
    if id != "1287498729198":
        return "Error: Unauthorized User Cannot add to database", 200
    if item == "":
        return "Invalid item name : Name cannot be an empty string", 200
     
    update_item = mydb["registered_items"]
    myQuery = {"item_name" : item}
    find_item = update_item.find(myQuery)
    temp_array = [x for x in find_item]
    if len(temp_array) == 0:
        return ("Cannot Update Item that does not exist! Please check the item name! Or use the /add-item command", 200)
    else:
        mydoc = update_item.update_one(myQuery,
                {
                    "$set": {
                        "price":changed_price,
                        "quantity":changed_quantity
                    }
                }
            )
        return "Update successful!", 200
 
 
"""List of all current items in ShopifyStore (Collection registered_items)
    REST Call : GET Message
    Post Request Attributes

        ===== Attributes =====
        None
        
        Return Type :
        List of all the values in Collection
    
        """ 
@app.route('/all-items', methods=['GET'])
def show_all():
    update_item = mydb["registered_items"]
    find_item = [x for x in update_item.find()]
    return str(find_item), 200


"""View Items in ShopifyStore in various orders including : highest-lowest price, lowest-highest price, highest-lowest quantity, lowest-highest quantity
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
        """
@app.route('/fetch-items', methods=['POST'])
def filter_by_item():
    try:
        values = request.get_json()
        filter_type = values['filter_type'] #low-high price, low-high quantity
        name_search = values['provided_name'] #part of the actual title of the item list 
    except:
        return "Invalid Entry : Check Docstring on how to use command", 200
    
    update_item = mydb["registered_items"]
      
    if filter_type == "highest-lowest price":
        find_item = [x for x in update_item.find()]
        newlist = sorted(regex(find_item, name_search), key=lambda k: k['price'])
        return str(newlist.reverse()), 200  
    elif filter_type == "lowest-highest price":
        find_item = [x for x in update_item.find()]
        newlist = sorted(regex(find_item, name_search), key=lambda k: k['price'])
        return str(newlist), 200        
    elif filter_type == "highest-lowest quantity":
        find_item = [x for x in update_item.find()]
        newlist = sorted(regex(find_item, name_search), key=lambda k: k['quantity'])
        return str(newlist.reverse()), 200  
    elif filter_type == "lowest-highest quantity":
        find_item = [x for x in update_item.find()]
        newlist = sorted(regex(find_item, name_search), key=lambda k: k['quantity'])
        return str(newlist), 200  

def regex(list_, item_name):
    array = []
    for product_des in list_:
        temp_var = product_des["item_name"]
        if item_name in temp_var:
            array.append(product_des)

    return array

"""Make a Purchase of given quantity for a particular item
    REST Call : POST Message
    Post Request Attributes

        ===== Attributes =====
        purchased_item : Name of item user wants to purchase
        purchased_quantity : Quantity user wishes to purchase


        Throws Exception :  
        If all Attributes are not provided -> return value is Invalid Entry
        If quantity requested exceeds quantity in ShopifyStore -> return value Error : Purchase exceeds quantity limit! Cannot execute order
        If item does not exist in collection -> return value is Cannot Update Item that does not exist! Please check the item name! Or use the /add-item command
        
        """
@app.route('/purchase-item', methods=['POST'])
def purchase():
    try:
        values = request.get_json()
        purchased_item = values["item_name"] 
        purchased_quantity = values['quantity']
    except:
        return "Invalid Entry : Check Docstring on how to use command", 200
    
    purchase_item = mydb["registered_items"]
    myQuery = {"item_name" : purchased_item}
    find_item = purchase_item.find(myQuery)
    temp_array = [x for x in find_item]

    if len(temp_array) == 0:
        return ("Cannot purchase item that does not exist! Please check the item name! Or use the /add-item command", 200)
    elif len(temp_array) == 1:
        current_quantity = temp_array[0]['quantity'] - purchased_quantity
        if current_quantity < 0:
            return "Error : Purchase exceeds quantity limit! Cannot execute order", 200
        else:
            mydoc = purchase_item.update_one(myQuery,
                    {
                        "$set": {
                            "quantity": current_quantity
                        }
                    }
                )
            return "Purchase Successful!", 200
        
"""Add items to a cart (collection checked_item) 
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
        
        """
@app.route('/add-to-cart', methods=['POST'])
def checkout():
    try:
        values = request.get_json()
        checked_item = values["item_name"]
        checked_price = values["item_price"]
        checked_quantity = values['quantity']
    except:
        return "Invalid Entry : Check Docstring on how to use command", 200
    
    check_item = mydb["registered_items"]
    myQuery = {"item_name" : checked_item}
    find_item = check_item.find(myQuery)
    temp_array = [x for x in find_item]
    if len(temp_array) == 0:
        return ("Cannot checkout item that does not exist! Please check the item name! Or use the /add-item command", 200)
    elif len(temp_array) == 1:
        current_quantity = temp_array[0]['quantity'] #quantity of product
        checkout_cart = mydb["checked_items"]
        myQuery = {"item_name" : checked_item}
        find_item = checkout_cart.find(myQuery)
        temp_array = [x for x in find_item]
        if len(temp_array) == 0:
            if checked_quantity <= current_quantity:
                response = {
                    "item_name" : checked_item,
                    "price" : checked_price,
                    "quantity" : checked_quantity
                 }
                checkout_cart.insert_one(response)
                return "Added to Shopping Cart!", 200
            else:
                return "Error : Checkout exceeds quantity limit! Cannot add to order", 200
        else:
            checkout_current_quantity = temp_array[0]['quantity']
            if current_quantity - checkout_current_quantity >=0 : 
                mydoc = checkout_cart.update_one(myQuery,
                                                   {
                                "$set": {
                                    "quantity":checked_quantity
                                }
                            }
                        )
                return "Checkout successful!", 200
            else:
                return "Error : Checkout exceeds quantity limit! Cannot add to order", 200

"""List of all current items in Checkout window 
    REST Call : GET Message
    Post Request Attributes

        ===== Attributes =====
        None
        
        Return Type :
        List of all the values in Collection
    
        """ 
@app.route('/checkout-total', methods=['GET'])
def checkout_total():
    checkout_item = mydb["checked_items"]
    find_item = [x for x in checkout_item.find()]
    total = 0
    for i in find_item:
        total += i['price']
    return str(find_item) + "Your Total is $"+ str(total), 200

    
    

if __name__ == '__main__':
    from argparse import ArgumentParser   
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type = int, help = 'port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port = port)