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
   # store_name = request.args.get('store_name')
   # save_store_name = Store(name=store_name) # Create an instance (Store is the table in models.py)
   # save_store_name.save() 
   # return render_template('index.html',store_name=store_name)
   return render_template('index.html')

@app.route("/store")   
def store():
   return render_template('store.html')      

@app.route("/store_form", methods=["POST"])
def store_form():
   store_name = Store(name=request.form.get('store_name'))
   # store_name = request.args.get('store_name')
   # save_store_name = Store(name=store_name) # Create an instance (Store is the table in models.py)
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

   

if __name__ == '__main__':
   app.run()