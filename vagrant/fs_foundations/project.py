from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/json')
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItems=[item.serialize for item in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json')
def restaurant_menu_item_json(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menu_item.serialize)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for new_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == "POST":
        menu_item = MenuItem(name=request.form["name"], restaurant_id=restaurant_id)
        session.add(menu_item)
        session.commit()
        flash("New menu item created!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant_id=restaurant_id)

# Task 2: Create route for edit_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
        edited_item = session.query(MenuItem).filter_by(id=menu_id).one()
        if request.method == 'POST':
            if request.form['name']:
                edited_item.name = request.form['name']
            session.add(edited_item)
            session.commit()
            flash("Menu item edited!")
            return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
        else:
            # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
            # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
            return render_template(
                'edit_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item=edited_item)

# Task 3: Create a route for delete_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        session.delete(item_to_delete)
        session.commit()
        flash("Menu item deleted!")
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'delete_menu_item.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item_to_delete)

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)