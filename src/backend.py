import mysql.connector
from mysql.connector import Error
import connect_to_db
import query
from flask import Flask, render_template, request 

app = Flask(__name__)

@app.route("/")
def home():
    return "<h2 style='color:green'>Database presentation homepage</h2>"

@app.route("/modify-tables", methods = ['GET', 'POST'])
def modify():

    if request.method == 'GET':
        return render_template("modify_tables.html", selected = None, data = None)

    if request.method == 'POST':
       
        selected_table = request.form.get("select_table")
        selected_action = request.form.get("select_action")
        step = request.form.get("form_step")
 
        data_dict = {}
        if not selected_table or not selected_action:
            return render_template("modify_tables.html", selected = None, step = 'zero')
        else:
            data_dict['table'] = selected_table
            data_dict['action'] = selected_action
 
        if step == 'one':
            return render_template("modify_tables.html", selected = data_dict, step = 'two')

        elif step == 'three':

            if data_dict['action'] in ['modify', 'delete']:
                
                if data_dict['table'] == 'Customer':
                    
                    print("Here")
 
                    selected_card = request.form.get("insert_card")
                    selected_name = request.form.get("insert_name")

                    if selected_card != "":
                        data_dict['card_id'] = selected_card
                        selected_name = query.get_one_col("SELECT name FROM Customer WHERE card_id = {}".format(selected_card))
                        if not selected_name:
                            data_dict['name'] = None
                            return render_template("modify_tables.html", selected = data_dict, step = 'four')
                        else:
                            data_dict['name'] = selected_name[0]
                            selected_name = data_dict['name']

                    elif selected_name != "":
                        data_dict['name'] = selected_name
                        selected_card = query.get_one_col("SELECT card_id FROM Customer WHERE name = '{}'".format(selected_name))
                        if not selected_card:
                            data_dict['card_id'] = None
                            return render_template("modify_tables.html", selected = data_dict, step = 'four')
                        else:
                            data_dict['card_id'] = selected_card[0]
                            selected_card = data_dict['card_id']

                    else:
                        return render_template("modify_tables.html", selected = data_dict, step = 'two')

                    customer_data = ['sex','points','reg_date','pet','date_of_birth','street','number','postal_code','city']
                    for d in customer_data:
                        data_dict[d] = query.get_one_col("SELECT {} FROM Customer WHERE card_id = {}".format(d, selected_card))[0]
           
                    return render_template("modify_tables.html", selected = data_dict, step = 'four') 

                elif data_dict['table'] == 'Product':

                    selected_barcode = request.form.get("insert_barcode")
                    if selected_barcode != "":
                        data_dict['barcode'] = selected_barcode
                        selected_prod_data = query.get_table("SELECT name,label,current_price,category_id FROM Product WHERE barcode = {}".format(selected_barcode))
                        if not selected_prod_data:
                            data_dict['prod_name'] = None
                            return render_template("modify_tables.html", selected = data_dict, step = 'four')
                        else:
                            print(selected_prod_data, selected_prod_data[0])
                            data_dict['prod_name'] = selected_prod_data[0][0] 
                            data_dict['label'] = selected_prod_data[0][1]
                            data_dict['current_price'] = selected_prod_data[0][2]
                            data_dict['category_id'] = selected_prod_data[0][3]
                            return render_template("modify_tables.html", selected = data_dict, step = 'four')
                    else:
                        return render_template("modify_tables.html", selected = data_dict, step = 'two')

                elif data_dict['table'] == 'Store':
                    selected_store = request.form.get("insert_store_id")
                    if selected_store != "":
                        data_dict['store_id'] = selected_store
                        selected_store_name = query.get_one_col("SELECT store_name FROM Store WHERE store_id = {}".format(selected_store))
                        if not selected_store_name:
                            data_dict['store_name'] = None
                            return render_template("modify_tables.html", selected = data_dict, step = 'four')
                        else:
                            data_dict['store_name'] = selected_store_name[0]
                            store_data = ['area','opening_hours','street_name','street_number','city','postal_code']
                            for d in store_data:
                                data_dict[d] = query.get_one_col("SELECT {} FROM Store WHERE store_id = {}".format(d, selected_store))[0]
                            return render_template("modify_tables.html", selected = data_dict, step = 'four')
                    else:
                        return render_template("modify_templates.html", selected = data_dict, step = 'two')

        elif step == 'five':
            if selected_table == 'Customer':
                return render_template("modify_tables.html", selected = data_dict, step = 'done')
            
            elif selected_table == 'Product':
                return render_template("modify_tables.html", selected = data_dict, step = 'error')

            elif selected_table == 'Store':
                return render_template("modify_tables.html", selected = data_dict, step = 'done')

        if data_dict['action'] == 'delete-backup':
            if data_dict['table'] == 'Customer':
                data_dict['card'] = request.form.get("insert_card")
                return "<h3>Selected card ID = {}</h3>".format(data_dict['card'])
            elif data_dict['table'] == 'Product':
                data_dict['barcode'] = request.form.get("insert_barcode")
                return "<h3>Selected barcode = {}</h3>".format(data_dict['barcode'])
            elif data_dict['table'] == 'Store':
                data_dict['store'] = request.form.get("insert_store_id")
                return "<h3>Selected store ID = {}</h3>".format(data_dict['store'])

        return render_template("modify_tables.html", selected = None, data = None)

@app.route("/price-history", methods = ['GET', 'POST'])
def price_history():

    if request.method == 'GET':
        return render_template("price_history.html", data = None)

    if request.method == 'POST':
       
        selected_barcode = request.form.get("insert_barcode")
        if selected_barcode == "":
           return render_template("price_history.html", data = None)

        data_dict = {}
        data_dict['barcode'] = selected_barcode
        description = query.get_one_col("SELECT name FROM Product WHERE barcode = {}".format(selected_barcode))         
        print(description)
        if not description:
            data_dict['description'] = None
        else:
            data_dict['description'] = description[0]

        data_dict['headers'] = ['start date', 'end date', 'amount']
        data_dict['values'] = query.get_table("SELECT start_date, end_date, amount " +
                                              "FROM Price " +
                                              "WHERE barcode = {}".format(selected_barcode))

        return render_template("price_history.html", barcode = selected_barcode, data = data_dict)

@app.route("/shopping-stats", methods = ['GET', 'POST'])
def shopping_stats():

    if request.method == 'GET':
       return render_template("shopping_stats.html", metric = None, data = None)

    if request.method == 'POST':

       selected_metric = request.form.get("select_metric")
       print(selected_metric)
       data_dict = {}
       
       if selected_metric == 'fav_pairs':
           data_dict['fav_pairs'] = {}
           data_dict['fav_pairs']['headers'] = ['Barcode 1', 'Product name 1', 'Barcode 2', 'Product name 2', 'Pair frequency']
           data_dict['fav_pairs']['values'] = query.get_table("WITH buy_products_names(barcode, name, transaction_id) AS " +
                                                                   "(SELECT P.barcode, P.name, B.transaction_id FROM buy_products AS B NATURAL JOIN Product AS P) " + 
                                                              "SELECT B1.barcode, B1.name, B2.barcode, B2.name, COUNT(*) AS pair_freq " +
                                                              "FROM buy_products_names AS B1, buy_products_names AS B2 " +
                                                              "WHERE B1.transaction_id = B2.transaction_id and B1.barcode < B2.barcode " +
                                                              "GROUP BY B1.barcode, B2.barcode " +
                                                              "ORDER BY pair_freq DESC " +
                                                              "LIMIT 10")
       if selected_metric == 'fav_spot':
           data_dict['fav_spot'] = {}
           data_dict['fav_spot']['headers'] = ['Store_id', 'Aisle', 'Shelf', 'Shelf share']
           data_dict['fav_spot']['values'] = query.get_table("SELECT O.store_id, O.aisle, O.shelf, SUM(B.quantity) * 100.0 / SUM(SUM(B.quantity)) OVER(PARTITION BY O.store_id) AS shelf_share " +
                                                             "FROM offers_products as O, buy_products as B, Transaction as T " +
                                                             "WHERE O.barcode = B.barcode AND T.transaction_id = B.transaction_id AND O.store_id = T.store_id " +
                                                             "GROUP BY O.store_id, O.aisle, O.shelf " +
                                                             "ORDER BY O.store_id, O.aisle, O.shelf")

       if selected_metric == 'label_pop':
           data_dict['label_pop'] = {}
           data_dict['label_pop']['headers'] = ['Category', 'is_label', 'Percentage']
           data_dict['label_pop']['values'] = query.get_table("SELECT P.category_id, P.label, SUM(B.quantity) * 100.0 / SUM(SUM(B.quantity)) OVER(PARTITION BY category_id) AS label_share " +
                                                              "FROM Product as P INNER JOIN buy_products as B ON P.barcode = B.barcode " +
                                                              "GROUP BY P.category_id, P.label " +
                                                              "ORDER BY P.category_id, P.label")

       if selected_metric == 'fav_hour':
           data_dict['money_hour'] = {} 
           data_dict['money_hour']['headers'] = ['Store_id', 'Hour', 'Share']
           data_dict['money_hour']['values'] = query.get_table("SELECT store_id, HOUR(timestamp) AS shop_time, " + 
                                                                      "SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER(PARTITION BY store_id) AS amount_per_hour " +
                                                               "FROM Transaction " +
                                                               "GROUP BY store_id, shop_time " +
                                                               "ORDER BY store_id, shop_time")

           data_dict['age_hour'] = {}
           data_dict['age_hour']['headers'] = ['Age', 'Hour', 'Share']
           data_dict['age_hour']['values'] = query.get_table("SELECT FLOOR(YEAR(C.date_of_birth)/10)*10 AS age, HOUR(T.Timestamp) as shop_time, " + 
                                                                    "COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY FLOOR(YEAR(C.date_of_birth)/10)*10) as share " +
                                                             "FROM Transaction AS T INNER JOIN Customer AS C ON T.card_id = C.card_id " +
                                                             "GROUP BY age, shop_time " +
                                                             "ORDER BY age, shop_time")

       return render_template("shopping_stats.html", metric = selected_metric, data = data_dict)

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

        top10_products = query.get_table("SELECT P.barcode, P.name, sum(B.quantity) AS total_quantity " + 
                                         "FROM buy_products AS B INNER JOIN Product AS P ON B.barcode = P.barcode " +
                                         "AND B.transaction_id IN (SELECT transaction_id FROM Transaction WHERE card_id = {}) ".format(selected_card) +
                                         "GROUP BY P.barcode " + 
                                         "ORDER BY total_quantity DESC " +
                                         "LIMIT 10") 

        visited_stores = query.get_table("SELECT DISTINCT T.store_id, S.store_name " + 
                                         "FROM Transaction AS T INNER JOIN Store AS S ON T.store_id = S.store_id AND T.card_id = {} ".format(selected_card) +
                                         "ORDER BY store_id")

        visit_per_hour = query.get_table("SELECT HOUR(timestamp) AS dt, SUM(total_amount) AS amount_per_dt, " +
                                                "SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER () AS share_per_dt " +
                                         "FROM Transaction "+
                                         "WHERE card_id = {} ".format(selected_card) +
                                         "GROUP BY dt " +
                                         "ORDER BY dt")

        hours_visit = query.get_one_col("SELECT HOUR(timestamp) AS dt " +
                                        "FROM Transaction " +
                                        "WHERE card_id = {} ".format(selected_card) +
                                        "GROUP BY dt " +
                                        "ORDER BY dt")

        hours_share = query.get_one_col("SELECT SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER () AS share_per_dt, HOUR(timestamp) AS dt " +
                                         "FROM Transaction " +
                                         "WHERE card_id = {} ".format(selected_card) +
                                         "GROUP BY dt " +
                                         "ORDER BY dt")

        week_average = query.get_table("SELECT YEAR(timestamp) AS t_year, WEEK(timestamp) AS t_week, SUM(total_amount) AS week_total " +
                                       "FROM Transaction " +
                                       "WHERE card_id = {} ".format(selected_card) +
                                       "GROUP BY t_year, t_week " +
                                       "ORDER BY t_year, t_week")

        month_average = query.get_table("SELECT YEAR(timestamp) AS t_year, MONTH(timestamp) AS t_month, SUM(total_amount) AS month_total " +
                                       "FROM Transaction " +
                                       "WHERE card_id = {} ".format(selected_card) +
                                       "GROUP BY t_year, t_month " +
                                       "ORDER BY t_year, t_month")

        data_dict['fav_prod'] = {}
        data_dict['fav_prod']['table'] = top10_products
        data_dict['fav_prod']['headers'] = ['barcode', 'product name', 'total quantity']

        data_dict['stores'] = {}
        data_dict['stores']['table'] = visited_stores
        data_dict['stores']['headers'] = ['store ID', 'Store name']

        data_dict['fav_hour'] = {}
        data_dict['fav_hour']['table'] = visit_per_hour
        data_dict['fav_hour']['headers'] = ['hour', 'Total amount per hour', 'share per hour']

        data_dict['week_avg'] = {}
        data_dict['week_avg']['table'] = week_average
        data_dict['week_avg']['headers'] = ['year', 'week', 'Week total']

        data_dict['month_avg'] = {}
        data_dict['month_avg']['table'] = month_average
        data_dict['month_avg']['headers'] = ['year', 'month', 'month total'] 

        i = 0
        bar_values = []
        bar_labels = range(0,24)
        for h in bar_labels:
            if h == hours_visit[i]:
                bar_values.append(hours_share[i])
                if (i < len(hours_visit)-1):
                    i += 1
            else:
                bar_values.append(0.0)

        data_dict['fav_hour']['labels'] = bar_labels
        data_dict['fav_hour']['values'] = bar_values
        data_dict['fav_hour']['max'] = max(bar_values)

        return render_template("customer_stats.html", customer = customer_dict, data = data_dict)

@app.route("/select", methods = ['GET', 'POST'])
def select():

    filters_dict = {}
    filters_dict['tables'] = ['Product', 'Store', 'Customer', 'Transaction']
    if request.method == 'GET':
        filters_dict['selected_table'] = ""
        return render_template("select.html", filters = filters_dict)
    if request.method == 'POST':
        filters_dict['selected_table'] = request.form.get("select_table")
        filters_dict['store_names'] = query.get_one_col("SELECT store_name from Store")
        filters_dict['category_names'] = query.get_one_col("SELECT category_name from Category")
        return render_template("select.html", filters = filters_dict)

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
            selected_min_price = request.form.get("min_price")
            selected_max_price = request.form.get("max_price")

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
                if selected_min_price != "":
                    query_arr.append("total_amount > {}".format(selected_min_price))
                if selected_max_price != "":
                    query_arr.append("total_amount < {}".format(selected_max_price))

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
