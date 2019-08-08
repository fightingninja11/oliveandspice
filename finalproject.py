from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Restaurant, MenuItem
import ctypes

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

session = scoped_session(sessionmaker(bind=engine))

@app.route('/restaurants/')
def restaurants():
	items = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants=items)

@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	restaurantname = session.query(Restaurant).filter_by(id=restaurant_id).one().name
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash('Restaurant edited')
		return redirect(url_for('restaurants', restaurant_id=restaurant_id))
	else:
		return render_template('editrestaurant.html', restaurant_id=restaurant_id, restaurantname=restaurantname)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	restaurantname = session.query(Restaurant).filter_by(id=restaurant_id).one().name
	if request.method == 'POST':
		session.delete(deletedRestaurant)
		session.commit()
		flash('Restaurant deleted')
		return redirect(url_for('restaurants'))
	else:
		return render_template('deleterestaurant.html', restaurant_id=restaurant_id, restaurantname=restaurantname)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newItem = Restaurant(name=request.form['name'])
		session.add(newItem)
		session.commit()
		flash('New restaurant added')
		return redirect(url_for('restaurants'))
	else:
		return render_template('newrestaurant.html')


### Menu Items from here on ###

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
	menuitems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	restaurantname = session.query(Restaurant).filter_by(id=restaurant_id).one().name
	return render_template('menu.html', restaurant_id=restaurant_id, menuitems=menuitems, restaurantname=restaurantname)

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'], price='$'+request.form['price'], description=request.form['description'], course=request.form['course'], restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash('Nem menu item added')
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = '$'+request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		flash('Menu item edited')
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id, menu_id=menu_id))
	else:
		return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deletedMenuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(deletedMenuItem)
		session.commit()
		flash('Menu item deleted')
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id, menu_id=menu_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedMenuItem)



### JSONIFY

@app.route('/restaurants/JSON/')
def restaurantsJSON():
	items = session.query(Restaurant).all()
	return jsonify(Restaurants=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	singlemenuitem = session.query(MenuItem).filter_by(id=menu_id).all()
	return jsonify(MenuItem=[i.serialize for i in singlemenuitem])

























if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
