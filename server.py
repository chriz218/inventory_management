import peeweedbevolve # For migration
from flask import Flask, render_template, request, flash, redirect, url_for
from models import db
from models import Store, Warehouse

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.before_request
def before_request():
   db.connect()

@app.after_request
def after_request(response):
   db.close()
   return response

@app.cli.command() # new
def migrate(): # new 
   db.evolve(ignore_tables={'base_model'}) # new

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/store")   
def store():
   return render_template('store.html')      

@app.route("/store_form", methods=["POST"])
def store_form():
   store_name = Store(name=request.form.get('store_name'))
   if store_name.save():
      flash("Store successfully saved")
      return redirect(url_for('store'))
   else:   
      return render_template('store.html',store_name=store_name)

@app.route("/warehouse")
def warehouse():
   stores = Store.select() # Selects the whole table 
   return render_template('warehouse.html', stores=stores)

@app.route("/warehouse_form", methods=["POST"])
def warehouse_form():
   warehouse_store = request.form.get('warehouse_store') # getting value from warehouse.html
   warehouse_location = request.form.get('warehouse_location') # getting value from warehouse.html
   # breakpoint()
   warehouse_instance = Warehouse(store_id=warehouse_store, location = warehouse_location) # creating an instance (row) of Warehouse 
   if warehouse_instance.save():
      flash("Warehouse successfully saved")
      return redirect(url_for('warehouse'))
   else:   
      return render_template('warehouse.html',warehouse_location=warehouse_location, warehouse_store=warehouse_store)   

@app.route("/store/<id>")
def store_info(id):
   store_obj = Store.get_by_id(id)
   count_no_warehouse = len([wh.location for wh in store_obj.warehouses])
   return render_template('editstore.html', store_obj = store_obj, count_no_warehouse=count_no_warehouse)

@app.route("/store_info_edit/<id>", methods=["POST"])
def store_info_edit(id):
   store_obj = Store.get_by_id(id) # gets the row in Store table that matches the id
   store_name = request.form.get('store_name') # getting value from editstore.html
   store_obj.name = store_name # Setting a new name for the name in the row of Store table that matches the id 
   if store_obj.save():
      return redirect(url_for('store_info', id=id))  

@app.route("/store/content")
def content():
   stores = Store.select() # Selects the whole table
   return render_template('content.html', stores=stores)

@app.route("/store/delete", methods=["POST"])
def delete():
   stores = Store.select() # Selects the whole table
   id_to_delete = request.form.get('delete-btn') # Set the variable, id_to_delete, to the value of the button named, delete-btn
   instance_to_delete = Store.get_by_id(id_to_delete) # Select the row where id_to_delete is
   Warehouse.delete().where(Warehouse.store_id == id_to_delete).execute() # You need to delete from Warehouse before you delete from Store
   instance_to_delete.delete_instance()
   return redirect(url_for('content'))   

if __name__ == '__main__':
   app.run()