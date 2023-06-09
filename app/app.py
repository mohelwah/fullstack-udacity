from flask import Flask, render_template,request,redirect,url_for,flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)
app.secret_key="HiSecretekey"
engine = create_engine("sqlite:///restaurantmenu.db")

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/")
@app.route("/restaurants/<int:restaurant_id>")
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    
    
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/new/", methods=['GET',"POST"])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id,description=request.form['description'],
                           price=request.form['price'])
        session.add(newItem)
        session.commit()
        flash("new menu item created!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/edit/", methods=['GET',"POST"])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
        if request.form['price']:
            menuItem.price = request.form['price']
        session.add(menuItem)
        session.commit()
        flash(" menu item Edited!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id,menu_id=menu_id)

# Task 3: Create a route for deleteMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/<int:menu_id>/delete/", methods=['GET',"POST"])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        
        session.delete(itemToDelete)
        session.commit()
        flash("menu item deleted!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',item=itemToDelete)

#making an Api Endpoint (Get Reqeust)
@app.route("/restaurants/<int:restaurant_id>/menu/JSON", methods=['GET',"POST"])
def restaurantMenuJson(restaurant_id):
   
    #restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items =  session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON", methods=['GET',"POST"])
def menuItemJson(restaurant_id,menu_id):
   
    #restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItem =  session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = menuItem.serialize)


if __name__ == "__main__":
    
    app.debug(True)
    app.run(host="127.0.0.1", port=5000)
    