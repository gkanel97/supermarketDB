import mysql.connector
from mysql.connector import Error
import connect_to_db
import query
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2 style='color:green'>Database presentation homepage</h2>"

@app.route("/hello")
def hello():
    return "Hello world!"

@app.route("/select", methods = ['GET', 'POST'])
def select():
    tables = ['Product', 'Store', 'Customer', 'Transaction']
    if request.method == 'GET':
        return render_template("select.html", table_names = tables, selected_table="")
    if request.method == 'POST':
        selected_t = request.form.get("select_table")
        stores = query.get_one_col("SELECT store_name from Store")
        categories = query.get_one_col("SELECT category_name from Category")
        return render_template("select.html", selected_table = selected_t, table_names = tables, store_names = stores, category_names = categories)

@app.route("/presentation", methods = ['POST'])
def present():
    if request.method == 'POST':
        selected_table = request.form.get("select_table")

        if selected_table == "Transaction":
            selected_store = request.form.get("select_store")
            selected_payment = request.form.get("payment_method")
            selected_date = request.form.get("shop_date")
            selected_tid = request.form.get("transaction_id")
            selected_quantity = request.form.get("total_quantity")
            return "Store = {}, payment method = {}, date = {}, id = {}".format(selected_store, selected_payment, selected_date, selected_tid)

        elif selected_table == "Product":
            selected_category = str(request.form.get("select_category"))
            selected_barcode = str(request.form.get("barcode"))
            if selected_barcode != "":
                selected_data = query.get_table("SELECT * FROM Product where barcode = {}".format(selected_barcode))
            else:
                selected_data = query.get_table("SELECT * FROM Product where category_id = (SELECT category_id from Category where category_name = '{}')".format(selected_category))
            headers = query.get_one_col("DESCRIBE Product")
            return render_template("presentation.html", data = [headers, selected_data])

        elif selected_table == "Customer":
            selected_reg_date = request.form.get("reg_date")
            selected_card = request.form.get("card_id")
            selected_pet = request.form.get("select_pet")
            return "Card ID = {}, registration date = {}, pet = {}".format(selected_card, selected_reg_date, selected_pet)

        else:
            selected_store = request.form.get("select_store")
            selected_city = request.form.get("select_city")
            return "Store = {}, city = {}".format(selected_store, selected_city)

if __name__ == "__main__":
   app.run(host='0.0.0.0')
