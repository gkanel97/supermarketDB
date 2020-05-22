import mysql.connector
from mysql.connector import Error
import connect_to_db
import query
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2 style='color:green'>Database presentation homepage</h2>"

@app.route("/customer-stats", methods = ['GET', 'POST'])
def customer_stats():

    customer_dict = {}
    data_dict = {}

    if request.method == 'GET':
        return render_template("customer_stats.html", customer = None, data = None)

    if request.method == 'POST':
        selected_card = request.form.get("insert_card")
        selected_name = request.form.get("insert_name")

        if selected_card != "":
            customer_dict['card_id'] = selected_card
            selected_name = query.get_one_col("SELECT name FROM Customer WHERE card_id = {}".format(selected_card))
            if not selected_name:
                customer_dict['name'] = None
                return render_template("customer_stats.html", customer = customer_dict, data = None)
            else:
                customer_dict['name'] = selected_name[0]
                selected_name = customer_dict['name']	

        elif selected_name != "":
            customer_dict['name'] = selected_name
            selected_card = query.get_one_col("SELECT card_id FROM Customer WHERE name = '{}'".format(selected_name))
            if not selected_card:
                customer_dict['card_id'] = None
                return render_template("customer_stats.html", customer = customer_dict, data = None)
            else:
                customer_dict['card_id'] = selected_card[0]
                selected_card = customer_dict['card_id']

        else:
            return render_template("customer_stats.html", customer = None, data = None)         

        top10_products = query.get_table("SELECT P.barcode, P.name, sum(B.quantity) AS total_quantity FROM buy_products as B INNER JOIN Product as P ON B.barcode = P.barcode and B.transaction_id IN (SELECT transaction_id FROM Transaction WHERE card_id = {}) GROUP BY P.barcode ORDER BY total_quantity DESC LIMIT 10".format(selected_card)) 
        visited_stores = query.get_table("SELECT DISTINCT T.store_id, S.store_name FROM Transaction AS T INNER JOIN Store AS S ON T.store_id = S.store_id AND T.card_id = {} ORDER BY store_id".format(selected_card))

        data_dict['fav_prod'] = {}
        data_dict['fav_prod']['table'] = top10_products
        data_dict['fav_prod']['headers'] = ['barcode', 'product name', 'total quantity']

        data_dict['stores'] = {}
        data_dict['stores']['table'] = visited_stores
        data_dict['stores']['headers'] = ['store ID', 'Store name']

        return render_template("customer_stats.html", customer = customer_dict, data = data_dict)

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

            if selected_tid != "":
                selected_data = query.get_table("SELECT * FROM Transaction WHERE transaction_id = {}".format(selected_tid))
            else:
                query_arr = ["SELECT * FROM Transaction"]
                if selected_store != None:
                    query_arr.append("store_id = (SELECT store_id FROM Store WHERE store_name = '{}')".format(selected_store))
                if selected_payment != None:
                    query_arr.append("payment_method = '{}'".format(selected_payment))
                if selected_date != "":
                    query_arr.append("timestamp like '{}%'".format(selected_date))
                if selected_quantity != "":
                    query_arr.append("total_pieces = {}".format(selected_quantity))

                query_str = query_arr[0] + " WHERE "
                for q in query_arr[1:-1]:
                    query_str += q + " AND "
                query_str += query_arr[-1]
                print(query_str)
                selected_data = query.get_table(query_str)

            headers = query.get_one_col("DESCRIBE Transaction")
            return render_template("presentation.html", data = [headers, selected_data])


        elif selected_table == "Product":
            selected_category = str(request.form.get("select_category"))
            selected_barcode = str(request.form.get("barcode"))
            if selected_barcode != "":
                selected_data = query.get_table("SELECT * FROM Product WHERE barcode = {}".format(selected_barcode))
            else:
                selected_data = query.get_table("SELECT * FROM Product WHERE category_id = (SELECT category_id FROM Category WHERE category_name = '{}')".format(selected_category))
            headers = query.get_one_col("DESCRIBE Product")
            return render_template("presentation.html", data = [headers, selected_data])

        elif selected_table == "Customer":
            selected_card = request.form.get("card_id")
            selected_reg_date = request.form.get("reg_date")
            selected_pet = request.form.get("select_pet")
            print("selected pet =", selected_pet)
            if selected_card != "":
                selected_data = query.get_table("SELECT * FROM Customer WHERE card_id = {}".format(selected_card))
            else:
                query_arr = ["SELECT * FROM Customer"]
                if selected_pet != None:
                    query_arr.append("pet = '{}'".format(selected_pet)) 
                if selected_reg_date != "":
                    query_arr.append("reg_date = '{}'".format(str(selected_reg_date))) 

                query_str = query_arr[0] + " WHERE "
                for q in query_arr[1:-1]:
                    query_str += q + " AND "
                query_str += query_arr[-1]
                print(query_str)
                selected_data = query.get_table(query_str) 

            headers = query.get_one_col("DESCRIBE Customer")
            return render_template("presentation.html", data = [headers, selected_data])

        else:
            selected_store = request.form.get("select_store")
            selected_city = request.form.get("select_city")
            return "Store = {}, city = {}".format(selected_store, selected_city)

if __name__ == "__main__":
   app.run(host='0.0.0.0')
