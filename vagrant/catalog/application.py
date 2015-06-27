from flask import Flask, render_template
app = Flask(__name__)


# Show all catalog categories
@app.route("/")
@app.route("/catalog/")
def show_catalog():
    return "This will be the main catalog page"


# Show items for specified category
@app.route("/catalog/<string:category_name>")
def show_catalog_items(category_name):
    return "This page will show all items for category: %s" % category_name


# Show specified item for specified category
@app.route("/catalog/<string:category_name>/<string:item_name>")
def show_catalog_item(category_name, item_name):
    return "This page will be for showing item: %s for category: %s" % (item_name, category_name)


# Create new item for specified category
@app.route("/catalog/<string:category_name>/new")
def new_catalog_item(category_name):
    return "This page will be for creating a new item for category: %s" % category_name


# Edit item for specified category
@app.route("/catalog/<string:category_name>/<string:item_name>/edit")
def edit_catalog_item(category_name, item_name):
    return "This page will be for editing item: %s for category: %s" % (item_name, category_name)


# Delete item for specified category
@app.route("/catalog/<string:category_name>/<string:item_name>/delete")
def delete_catalog_item(category_name, item_name):
    return "This page will be for deleting item: %s for category: %s" % (item_name, category_name)


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
