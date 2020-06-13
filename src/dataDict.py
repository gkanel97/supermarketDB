from datetime import date

Customer_data = {'card_id':       { 'type' : 'int',  'value' : None },
                 'customer_name': { 'type' : 'str',  'value' : None },
                 'reg_date':      { 'type' : 'date', 'value' : str(date.today()) },
                 'date_of_birth': { 'type' : 'date', 'value' : None },
                 'pet':           { 'type' : 'str',  'value' : None },
                 'sex':           { 'type' : 'str',  'value' : None },
                 'points':        { 'type' : 'int',  'value' : None },
                 'street_name':   { 'type' : 'str',  'value' : None },
                 'street_number': { 'type' : 'int',  'value' : None },
                 'city':          { 'type' : 'str',  'value' : None },
                 'postal_code':   { 'type' : 'int',  'value' : None }
               }

Product_data = { 'barcode':       { 'type' : 'int',  'value' : None }, 
                 'product_name':  { 'type' : 'str',  'value' : None },
                 'current_price': { 'type' : 'float','value' : None },
                 'category_id':   { 'type' : 'int',  'value' : None },
                 'label':         { 'type' : 'bool', 'value' : None }
               }

Store_data =   { 'store_id':      { 'type' : 'int',  'value' : None },
                 'store_name':    { 'type' : 'str',  'value' : None },
                 'area':          { 'type' : 'int',  'value' : None }, 
                 'street_name':   { 'type' : 'str',  'value' : None }, 
                 'street_number': { 'type' : 'int',  'value' : None },
                 'city':          { 'type' : 'str',  'value' : None }, 
                 'postal_code':   { 'type' : 'int',  'value' : None },
                 'opening_hours': { 'type' : 'str',  'value' : None }
               } 
