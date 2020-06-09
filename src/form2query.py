import query
from flask import request
from datetime import date

def insert(form_fields, field_type, table):

    field_arr = []
    value_arr = []
    type_arr = []

    for field,type in zip(form_fields, field_type):
        new_data = request.form.get("insert_" + field)
        if new_data != "" and new_data != None:
            field_arr.append(field)
            value_arr.append(new_data)
            type_arr.append(type)

    field_tuple = "("
    value_tuple = "("
    for f,v,t in zip(field_arr[:-1], value_arr[:-1], type_arr[:-1]):
        field_tuple += f + ", "
        if t == 'str': 
            value_tuple += "'" + v + "', "
        else:
            value_tuple += v + ", "
    field_tuple += field_arr[-1] + ")"
    if type_arr[-1] == 'str': 
        value_tuple += "'" + value_arr[-1] + "')"
    else:
        value_tuple += value_arr[-1] + ")"
        
    query_str = "INSERT INTO " + table + " " + field_tuple + " VALUES " + value_tuple + ";"
    return [query_str]

def update(form_fields, field_type, table):

    field_arr = []
    value_arr = []
    type_arr = []
    query_arr = []

    for field,type in zip(form_fields, field_type):
        new_data = request.form.get("insert_" + field)
        if new_data != "" and new_data != 'None':
            field_arr.append(field)
            value_arr.append(new_data)
            type_arr.append(type)

    query_str = "UPDATE " + table + " SET "
    for f,v,t in zip(field_arr[1:-1], value_arr[1:-1], type_arr[1:-1]):
        if t == 'str':
            query_str += f + " = '" + v + "', "
        else:
            query_str += f + " = " + v + ", "
    if type_arr[-1] == 'str':
        query_str += field_arr[-1] + " = '" + value_arr[-1] + "' "
    else:
        query_str += field_arr[-1] + " = " + value_arr[-1] + " "

    if table == 'Customer':
        query_str += "WHERE card_id = {};".format(value_arr[0])
    elif table == 'Product':
        query_str += "WHERE barcode = {};".format(value_arr[0])
    elif table == 'Store':
        query_str += "WHERE store_id = {};".format(value_arr[0])
    else:
        print("Wrong table!")

    query_arr.append(query_str)

    if table == 'Product':
        old_price = float(query.get_one_col("SELECT current_price FROM Product WHERE barcode = {}".format(value_arr[0]))[0])
        new_price = float(request.form.get("insert_current_price"))
        if old_price != new_price: 
            query_arr.append("UPDATE Price SET end_date = '{}' WHERE barcode = {} AND amount = {}".format(str(date.today()), value_arr[0], old_price))
            query_arr.append("INSERT INTO Price (barcode, start_date, amount) VALUES ({}, '{}', {})".format(value_arr[0], str(date.today()), new_price))

    return query_arr
