import query
from flask import request
from datetime import datetime

def insert(form_data, table):
    for field_name, field_info in form_data.items():
        temp = request.form.get("insert_" + field_name)
        if temp != "" and temp != None:
            field_info['value'] = temp

    field_tuple = "("
    value_tuple = "("
    for field_name, field_info in form_data.items():
        if field_info['value'] != None:
            field_tuple += field_name + ", "
            if field_info['type'] in ['str', 'date']:
                value_tuple += "'" + field_info['value'] + "', "
            else:
                value_tuple += field_info['value'] + ", "

    field_tuple = field_tuple[:-2] + ")"
    value_tuple = value_tuple[:-2] + ")"
    query_str = "INSERT INTO " + table + " " + field_tuple + " VALUES " + value_tuple

    query_arr = []
    query_arr.append(query_str)
    if table == 'Product':
        query_arr.append("INSERT INTO " + 
                         "Price (barcode, amount) " + 
                         "VALUES ({}, {})".format(form_data['barcode']['value'], form_data['current_price']['value']))
    return query_arr


def update(form_data, table):

    for field_name, field_info in form_data.items():
        temp = request.form.get("insert_" + field_name)
        if temp != "" and temp != None:
            field_info['value'] = temp

    query_str = "UPDATE " + table + " SET "
    for field_name, field_info in form_data.items():
        if field_info['value'] != None:
            if field_info['type'] in ['str', 'date']:
                query_str += field_name + " = '" + field_info['value'] + "', "
            else:
                query_str += field_name + " = " + field_info['value'] + ", "

    if table == 'Customer':
        query_str = query_str[:-2] + " WHERE card_id = {}".format(form_data['card_id']['value'])
    elif table == 'Product':
        query_str = query_str[:-2] + " WHERE barcode = {}".format(form_data['barcode']['value'])
    elif table == 'Store':
        query_str = query_str[:-2] + " WHERE store_id = {}".format(form_data['store_id']['value'])
    else:
        print("Wrong table!")

    query_arr = []
    query_arr.append(query_str)

    if table == 'Product':
        old_price = query.get_one_col("SELECT current_price FROM Product WHERE barcode = {}".format(form_data['barcode']['value']))[0]
        new_price = float(form_data['current_price']['value'])
        if old_price:
            old_price = float(old_price)
            if old_price != new_price:
                query_arr.append("UPDATE Price SET end_date = '{}' WHERE barcode = {} AND amount = {}".format(str(datetime.now()), form_data['barcode']['value'], old_price))
                query_arr.append("INSERT INTO Price (barcode, amount) VALUES ({}, {})".format(form_data['barcode']['value'], new_price))
        else:
            query_arr.append("INSERT INTO Price (barcode, amount) VALUES ({}, {})".format(form_data['barcode']['value'], new_price))

    return query_arr


def delete(table):

    query_arr = []
    if table == 'Customer':
        selected_card_id = request.form.get("insert_card_id")
        query_arr.append("UPDATE Transaction SET card_id = NULL WHERE card_id = {}".format(selected_card_id))
        query_arr.append("DELETE FROM Customer WHERE card_id = {}".format(selected_card_id))

    elif table == 'Product':
        selected_barcode = request.form.get("insert_barcode")
        old_price = query.get_one_col("SELECT current_price FROM Product WHERE barcode = {}".format(selected_barcode))[0]
        query_arr.append("UPDATE Price SET end_date = '{}' WHERE barcode = {} AND amount = {}".format(str(datetime.now()), selected_barcode, old_price))
        query_arr.append("INSERT INTO Price (barcode) VALUES ({})".format(selected_barcode)) 
        query_arr.append("UPDATE Product SET current_price = NULL WHERE barcode = {}".format(selected_barcode))

    elif table == 'Store':
        selected_store_id = request.form.get("insert_store_id")
        query_arr.append("DELETE FROM buy_products WHERE transaction_id IN (SELECT transaction_id FROM Transaction WHERE store_id = {})".format(selected_store_id))
        query_arr.append("DELETE FROM Transaction WHERE store_id = {}".format(selected_store_id))
        query_arr.append("DELETE FROM offers_products WHERE store_id = {}".format(selected_store_id))
        query_arr.append("DELETE FROM Store WHERE store_id = {}".format(selected_store_id))

    return query_arr
