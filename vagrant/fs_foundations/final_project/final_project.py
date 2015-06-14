from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
app = Flask(__name__)

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/")
@app.route("/restaurants")
def show_restaurants():
    all_restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants=all_restaurants)

@app.route("/restaurant/new", methods=["GET", "POST"])
def new_restaurant():
    # return "This page will be for making a new restaurant"
    if request.method == "POST":
        restaurant = Restaurant(name=request.form["name"])
        session.add(restaurant)
        session.commit()
        flash("New Restaurant Created")
        return redirect(url_for("show_restaurants"))
    else:
        return render_template("new_restaurant.html")

@app.route("/restaurant/<int:restaurant_id>/edit", methods=["GET", "POST"])
def edit_restaurant(restaurant_id):
    # return "This page will be for editing restaurant %s" % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == "POST":
        restaurant.name = request.form["name"]
        session.add(restaurant)
        session.commit()
        flash("Restaurant Successfully Edited")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template("edit_restaurant.html", restaurant=restaurant)

@app.route("/restaurant/<int:restaurant_id>/delete", methods=["GET", "POST"])
def delete_restaurant(restaurant_id):
    # return "This page will be for deleting restaurant %s" % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == "POST":
        session.delete(restaurant)
        session.commit()
        flash("Restaurant Successfully Deleted")
        return redirect(url_for("show_restaurants"))
    else:
        return render_template("delete_restaurant.html", restaurant=restaurant)

@app.route("/restaurant/<int:restaurant_id>")
@app.route("/restaurant/<int:restaurant_id>/menu")
def show_menu(restaurant_id):
    # return "This page is the menu for restaurant %s" % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template("menu.html", restaurant=restaurant, menu_items=items)

@app.route("/restaurant/<int:restaurant_id>/menu/new", methods=["GET", "POST"])
def new_menu_item(restaurant_id):
    # return "This page is for making a new menu item for restaurant %s" % restaurant_id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == "POST":
        item = MenuItem(name=request.form["name"], price=request.form["price"], course=request.form["course"],
                        description=request.form["description"], restaurant=restaurant)
        session.add(item)
        session.commit()
        flash("New Menu Item Created")
        return redirect(url_for("show_menu", restaurant_id=restaurant_id))
    else:
        return render_template("new_menu_item.html", restaurant=restaurant)

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit", methods=["GET", "POST"])
def edit_menu_item(restaurant_id, menu_id):
    # return "This page is for editing menu item %s" % menu_id
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == "POST":
        item.name = request.form["name"]
        item.price = request.form["price"]
        item.course = request.form["course"]
        item.description = request.form["description"]
        session.add(item)
        session.commit()
        flash("Menu Item Successfully Edited")
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template("edit_menu_item.html", restaurant=item.restaurant, menu_item=item)

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete", methods=["GET", "POST"])
def delete_menu_item(restaurant_id, menu_id):
    # return "This page is for deleting menu item %s" % menu_id
    item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == "POST":
        session.delete(item)
        session.commit()
        flash("Menu Item Successfully Deleted")
        return redirect(url_for('show_menu', restaurant_id=restaurant_id))
    else:
        return render_template("delete_menu_item.html", restaurant=item.restaurant, menu_item=item)

# API Endpoints
@app.route("/restaurants/json")
def restaurants_json():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])

@app.route("/restaurant/<int:restaurant_id>/menu/json")
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[item.serialize for item in items])

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/json")
def restaurant_menu_item_json(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)

if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
