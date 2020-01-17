import peeweedbevolve # For migration
from flask import Flask, render_template, request, flash, redirect, url_for
from models import db
from models import Store

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

@app.route("/store_form")
def store_form():
   store_name = Store(name=request.args.get('store_name'))
   # store_name = request.args.get('store_name')
   # save_store_name = Store(name=store_name) # Create an instance (Store is the table in models.py)
   if store_name.save():
      flash("Store successfully saved")
      return redirect(url_for('store'))
   else:   
      return render_template('store.html',store_name=store_name)
   

if __name__ == '__main__':
   app.run()