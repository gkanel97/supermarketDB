#!/usr/bin/env python
# coding: utf-8

import csv
import random
import datetime

# Global data parameters

product_data = 'product_data.txt'
prod_availability = [[0.8, 0.85, 0.7, 0.6], [0.6, 0.75, 0.98], [0.85, 0.6], 1]

street_data = ['Athens_streets.txt', 'Thessaloniki_streets.txt', 'Volos_streets.txt']
cities = ['Athens', 'Thessaloniki', 'Volos']
city_weights = [5, 3, 2]
postal_codes = [range(11850,11860), range(54620,54625), range(38222,38225)]

aisles = 5
shelves = 3
online_store = 10
stores_by_loc = [[1,2,3,4],[5,6,7],[8,9]]
working_hours = [*[[8,21]]*5, [9,20]]
working_hours_str = ['Mon-Fri: 08-21, Sat: 09-20, Sun: CLOSED', 'Mon-Sun: OPEN 24h']
area = [[400, 500, 320, 250], [240, 350, 1000], [500, 250], 'NULL']

first_reg_date = datetime.date(2019,1,1)
last_reg_date = datetime.date(2020,5,1)
first_birth_date = datetime.date(1945,1,1)
last_birth_date = datetime.date(2000,1,1)
first_price_date = datetime.date(2019,1,2)
last_price_date = datetime.date(2020,6,1)
max_price_changes = 10

reg_customers = 200
unreg_customers = 100


# Import product data from product_data.txt
# Products belonging to different categories are separated by an empty line 
# and a line '===== {Category_name} ====='
    
product_name = []
product_price = []
product_category = []

cat = 0
fp = open(product_data, 'r')
line = fp.readline()
while line:
    if line != '\n':
        tokens = line.split(',')
        if (tokens[0][0] != '='):
            product_category.append(cat)
            product_name.append(tokens[0])
            product_price.append(float(tokens[1]))
        else:
            cat += 1
    line = fp.readline()
fp.close()

# random.sample returns unique elements
# barcodes need to be sorted so that product weights remain valid
product_barcode = sorted(random.sample(range(10**12,10**13),len(product_name)))


# Read street names from txt files and save them in a dictionary
city_dict = {}

for street_file,city,ps in zip(street_data, cities, postal_codes):
    
    city_dict[city] = {}
    with open(street_file,'r') as f:
        city_dict[city]['Streets'] = []
        line = f.readline()
        while(line):
            if line:
                city_dict[city]['Streets'].append(line.replace(' \n',''))
            line = f.readline()
        city_dict[city]['Postal_codes'] = ps


def generate_random_datetime(start_datetime, end_datetime):
    date_delta = (end_datetime - start_datetime).days
    time_delta = (end_datetime - start_datetime).seconds
    if not date_delta:
        random_date = start_datetime + datetime.timedelta(seconds = random.randrange(time_delta))
    elif not time_delta:
        random_date = start_datetime + datetime.timedelta(days = random.randrange(date_delta))
    else:
        random_date = start_datetime + datetime.timedelta(days = random.randrange(date_delta), 
                                                          seconds = random.randrange(time_delta))
    return random_date


def generate_random_sorted_dates(start_date, end_date, count):

    days_between_dates = (end_date - start_date).days
    
    # Make sure that "count" random days can be returned
    if (end_date - start_date).days < count:
        return False
    
    # Generate random dates until the number of unique random dates equals to count"
    while True:   
        random_dates = []
        for i in range(count):
            random_dates.append(generate_random_datetime(start_date, end_date))
        sorted_unique_dates = sorted(set(random_dates))
        
        if len(sorted_unique_dates) == count:
            return sorted_unique_dates


# Generate a timestamp for a given date at which a transaction is possible
# The online store (store_id == 10) is open 24/7
# The physical stores are open Mon-Fri: 8-21 and Sat: 9-20

def generate_random_working_datetime(date, store):
    
    if store == online_store:
        time = datetime.time(hour = random.randrange(0,23), minute = random.randrange(0,60), 
                             second = random.randrange(0,60))
    else:
        day = date.weekday()
        if day < len(working_hours):
            opening = working_hours[day][0]
            closing = working_hours[day][1]
            time = datetime.time(hour = random.randrange(opening,closing-1), minute = random.randrange(0,60), 
                                 second = random.randrange(0,60))
        else:
            raise ValueError('The chosen store is closed at the given date')
   
    return datetime.datetime.combine(date, time)


# Generate a pseudo-random price history consisting of a number of changes

def generate_price_history(start_price, changes):
    price_hist_arr = [start_price]
    for i in range(changes):
        price_hist_arr.append(round(price_hist_arr[i]*random.uniform(0.8, 1.2),2))
    if (random.random() < 0.1):
        price_hist_arr[-1] = "NULL"
    return price_hist_arr


# Retrieve the product price that was valid at the date the transaction occured

def get_current_price(price_info_dict, shop_date):
    for pr,sd,ed in zip(price_info_dict['Price'], price_info_dict['Start_date'], price_info_dict['End_date']):
        if sd <= shop_date:
            if ed == 'NULL':
                return pr
            elif ed > shop_date:
                return pr
            
    raise ValueError('The product had no valid price at the given date')


# Choose the next store and shooping according to the shopping profile of each customer
# freq represents how often a customer shops on average
# store_pool are the stores the customer shops from

def get_next_date_store(previous_date, freq, store_pool, store_weight):
    
    new_date = previous_date + datetime.timedelta(days = random.randrange(max(0,freq-2),freq+2))
    chosen_store = random.choices(store_pool, weights = store_weight)[0]
    
    while True:

        # Online store is open every weekday and transactions can be performed
        # Physical stores are closed on Sundays (weekday 6)

        if chosen_store == online_store:                 # Accept every new date
            shop_date = new_date
            return shop_date, chosen_store
        else:
            if new_date.weekday() < len(working_hours):   # Accept all weekdays except Sunday
                shop_date = new_date
                return shop_date, chosen_store

        new_date = previous_date + datetime.timedelta(days = random.randrange(max(0,freq-2),freq+2))  


# Generate pseudo-random products for a specific transaction using the fuctions specified above
# average_items shows the average number of items a specific customer buys
# prod_weight shows the customer's preference for the offered products

def generate_items(barcodes, average_items, price_dict, shop_date, prod_weight):
    
    transaction_items = random.randint(max(1,average_items-5),average_items+5)
    chosen_products = random.choices(barcodes, k = transaction_items, weights = prod_weight)
    chosen_prod_dict = dict((x, dict(quantity = chosen_products.count(x))) for x in set(chosen_products))
    
    for b,info in chosen_prod_dict.items():
        info['price'] = get_current_price(price_dict[b], shop_date)

    # Keep only the products that have a valid price at transaction date    
    temp_dict = {}
    for b,info in chosen_prod_dict.items():
        if info['price'] != 'NULL':
            temp_dict[b] = info
            
    return temp_dict


# Generete a shopping profile for each customer

def generate_prod_weights(shop_profile, pet, all_barcodes, barcodes_in_store):
    
    # Profile: Fit single
    # Shops mainly fresh and refrigerated products, some personal care and less liquor and homeware
    if shop_profile < 0.15:
        prod_weight = [10]*37 + [8]*32 + [2]*26 + [4]*17 + [1]*18

    # Profile: Lazy single
    # Shops mainly refrigerated and personal care, some vegetables and liquor and less homeware
    elif shop_profile < 0.4:
        prod_weight = [4]*37 + [8]*32 + [3]*26 + [6]*17 + [1]*18

    # Profile: Family guy
    # Shops mainly fresh and refrigerated products and personal care, some liquor and homeware
    else:
        prod_weight = [10]*37 + [8]*32 + [2]*26 + [7]*17 + [2]*18

    if pet == 'dog':
        prod_weight += [5]*4 + [0]*8
    elif pet == 'cat':
        prod_weight += [0]*4 + [5]*5 + [0]*3
    elif pet == 'parrot':
        prod_weight += [0]*9 + [5]*3
    else:
        prod_weight += [0]*12
        
    # Keep only the weights for the products sold in the chosen store
    weights_in_store = []
    for b,w in zip(all_barcodes,prod_weight):
        if b in barcodes_in_store:
            weights_in_store.append(w)

    return weights_in_store


# Define the number and ID of the stores a specific customer shops from

def generate_store_preference(store_profile):
    
    stores = 0
    for sub_arr in stores_by_loc:
        stores += len(sub_arr)
    
    if store_profile < 0.55:     # Customer shops from only one physical store
        store_pref = [random.randint(stores_by_loc[0][0],stores_by_loc[-1][-1])]
        store_prob = [1]

    elif store_profile < 0.7:   # Customer shops from one physical store and online
        store_pref = [random.randint(stores_by_loc[0][0],stores_by_loc[-1][-1]), online_store]
        rand = random.uniform(0.7,0.95)
        store_prob = [rand, 1-rand]

    elif store_profile < 0.8:  # Customer shops from 2 physical stores
        store_pref = random.sample(stores_by_loc[random.randint(0,len(stores_by_loc)-1)], k = 2)
        rand = random.uniform(0.7,0.95)
        store_prob = [rand, 1-rand]

    elif store_profile < 0.9:  # Customer shops from 2 physical stores + online
        store_pref = [*random.sample(stores_by_loc[random.randint(0,len(stores_by_loc)-1)], k = 2), online_store]
        rand_1 = random.uniform(0.6, 0.8)
        rand_2 = random.uniform(0.05, 0.15)
        store_prob = [rand_1, rand_2, 1 - rand_1 - rand_2]

    else:                       # Customer shops only online
        store_pref = [online_store]
        store_prob = [1]

    return store_pref, store_prob


def generate_random_address(city):
    
    address_dict = {}
    address_dict['Street'] = random.choice(city_dict[city]['Streets'])
    address_dict['Number'] = random.randint(1,200)
    address_dict['Postal_code'] = random.choice(city_dict[city]['Postal_codes'])
    address_dict['City'] = city
    
    return address_dict


# Save store information in a dictionary

# Add information for physical stores
store_dict = {}
for store_team, area_team, city in zip(stores_by_loc, area, cities):
    for s,a in zip(store_team, area_team):
        store_dict[s] = {}
        store_dict[s]['Area'] = a
        store_dict[s]['Opening_hours'] = working_hours_str[0]
        store_dict[s]['Address'] = generate_random_address(city)

# Add information for the online store, assuming it is co-located with the first store
store_dict[online_store] = {}
store_dict[online_store]['Area'] = 'NULL'
store_dict[online_store]['Opening_hours'] = working_hours_str[1]
store_dict[online_store]['Address'] = store_dict[stores_by_loc[0][0]]['Address']


# Information for the price history of a product

price_hist_dict = {
    b: {
        'Price':[p], 
        'Start_date':[first_reg_date],
        'End_date':[]
    } for b,p in zip(product_barcode, product_price)
}

for key, val in price_hist_dict.items():
    price_change_dates = generate_random_sorted_dates(first_price_date,last_price_date,
                                                      random.randint(0,max_price_changes))
    price_hist = generate_price_history(val['Price'][0], len(price_change_dates))
    price_hist_dict[key]['Price'] = price_hist
    price_hist_dict[key]['Start_date'] += price_change_dates
    price_hist_dict[key]['End_date'] = price_change_dates + ['NULL']


# Generate pseudo-random information for many customers and save them to a dictionary

while True:
    card_id = [random.randint(10**7, 10**8) for i in range(reg_customers)]
    if len(card_id) == len(list(set(card_id))):
        break
    
customer_name = ['Customer-{}'.format(i) for i in range(reg_customers)]
customer_sex = ['M' if random.random() < 0.5 else 'F' for i in range(reg_customers)]
reg_date = [generate_random_datetime(first_reg_date, last_reg_date) for i in range(reg_customers)]
customer_dob=[generate_random_datetime(first_birth_date,last_birth_date) for i in range(reg_customers)]

pet = []
for i in range(reg_customers):
    rand = random.random()
    if rand < 0.2:
        pet.append('dog')
    elif rand < 0.3:
        pet.append('cat')
    elif rand < 0.35:
        pet.append('parrot')
    else:
        pet.append('NULL')
        
customer_dict = {
    card: {
        'Name': n,
        'Sex': s,
        'Points': 0,
        'Registration_date': d,
        'Pet': p,
        'DoB': dob,
    } for (card,n,s,d,p,dob) in zip(card_id, 
                                      customer_name, 
                                      customer_sex, 
                                      reg_date, pet, 
                                      customer_dob
                                     )
}


offers_dict = {}
for store_team, avail_team in zip(stores_by_loc, prod_availability):
    for s,av in zip(store_team, avail_team):
        offers_dict[s] = {}
        for b in random.sample(product_barcode, int(len(product_barcode)*av)):
            offers_dict[s][b] = {
                'Aisle': random.randint(1,aisles),
                'Shelf': random.randint(1,shelves)
            }
            
offers_dict[online_store] = {}
for b in random.sample(product_barcode, int(len(product_barcode)*prod_availability[-1])):
    offers_dict[online_store][b] = {
        'Aisle': 'NULL',
        'Shelf': 'NULL'
    }


# Generate pseudo-random transactions for all customers taking into account each customers profile
# (shop_freq, average_items, pet, shop_profile, payment_profile, store_pref, store_prob)
# as well as the availability of products at the chose store the chosen date 
# and the price at the transaction date 

transaction_dict = {}
for i in range(reg_customers):
    
    shop_freq = random.randint(2,8)
    average_items = random.randint(5,20)
    customer_id = card_id[i]
    reg_date = customer_dict[customer_id]['Registration_date']
    pet = customer_dict[customer_id]['Pet']
    shop_profile = random.random()
    payment_profile = random.random()
    store_pref, store_prob = generate_store_preference(random.random())
    points = 0        # 1 point is given for 3 euros spent (no rewards are assumed)

    # Start from registration date (or the next few days) and until last_price_date
    shop_date, chosen_store = get_next_date_store(reg_date, 0, store_pref, store_prob)
    while shop_date < last_price_date:

        transaction_id = random.randint(10**12, 10**13)
        payment_method = 'cash' if random.random() < payment_profile else 'credit_card'
        barcode_in_store = sorted(list(offers_dict[chosen_store].keys()))
        barcode_weight = generate_prod_weights(shop_profile, pet, product_barcode, barcode_in_store)
        shopped_prod = generate_items(barcode_in_store, average_items, price_hist_dict, shop_date, barcode_weight)

        amount = 0
        quantity = []
        for key,val in shopped_prod.items():
            amount += val['price'] * val['quantity']
            quantity.append(val['quantity'])
        points += int(amount/3) 
        total_pieces = sum(quantity)

        # Save all information on a dictionary
        transaction_dict[transaction_id] = {
            'timestamp': generate_random_working_datetime(shop_date, chosen_store),
            'store_id': chosen_store,
            'card_id': customer_id,
            'payment_method': payment_method,
            'products': list(shopped_prod.keys()),
            'quantity': quantity,
            'total_amount': amount,
            'total_pieces': total_pieces
        }

        shop_date, chosen_store = get_next_date_store(shop_date, shop_freq, store_pref, store_prob)
        
    customer_dict[customer_id]['Points'] = points
    
    # The store a customer mainly shops from shows the place they live in
    # Assume weighted distribution for customers who shop only online
    if store_pref[0] < 5:
        customer_dict[customer_id]['Address'] = generate_random_address('Athens')
    elif store_pref[0] < 8:
        customer_dict[customer_id]['Address'] = generate_random_address('Thessaloniki')
    elif store_pref[0] < 10:
        customer_dict[customer_id]['Address'] = generate_random_address('Volos')
    else:
        customer_dict[customer_id]['Address'] = generate_random_address(random.choices(['Athens','Thessaloniki','Volos'], 
                                                                                       weights = [5, 3, 2], 
                                                                                       k = 1)[0])

# Repeat the previous procedure, but assume that the customers are not registered and have no personal card
# As a result no customer information can be kept
# Assume that they have similar habits with registered customers

for i in range(unreg_customers):
    
    shop_freq = random.randint(2,8)
    average_items = random.randint(5,20)
    reg_date = first_reg_date
    pet = customer_dict[card_id[i]]['Pet']
    shop_profile = random.random()
    store_pref, store_prob = generate_store_preference(random.random())

    shop_date, chosen_store = get_next_date_store(reg_date, 0, store_pref, store_prob)
    while shop_date < last_price_date:

        transaction_id = random.randint(10**12, 10**13)
        payment_method = 'cash' if random.random() < 0.4 else 'credit_card'
        barcode_in_store = sorted(list(offers_dict[chosen_store].keys()))
        barcode_weight = generate_prod_weights(shop_profile, pet, product_barcode, barcode_in_store)
        shopped_prod = generate_items(barcode_in_store, average_items, price_hist_dict, shop_date, barcode_weight)
        
        amount = 0
        quantity = []
        for key,val in shopped_prod.items():
            amount += val['price'] * val['quantity']
            quantity.append(val['quantity'])
        total_pieces = sum(quantity)

        transaction_dict[transaction_id] = {
            'card_id': 'NULL',
            'timestamp': generate_random_working_datetime(shop_date, chosen_store),
            'store_id': chosen_store,
            'payment_method': payment_method,
            'products': list(shopped_prod.keys()),
            'quantity': quantity,
            'total_amount': amount,
            'total_pieces': total_pieces
        }

        shop_date, chosen_store = get_next_date_store(shop_date, shop_freq, store_pref, store_prob)


# Save all the generated data at csv files so it can be imported to the SQL database

with open('csv_files/store.csv','w') as store_csv:
    store_writer = csv.writer(store_csv, delimiter=',', quotechar='"')
    store_writer.writerow(['store_id','area','street_name','street_number','postal_code','city','opening_hours'])
    for key,val in store_dict.items():
        store_writer.writerow([key, val['Area'], val['Address']['Street'], val['Address']['Number'],
                               val['Address']['Postal_code'], val['Address']['City'], val['Opening_hours']])

with open('csv_files/product.csv', 'w') as data_csv:
    data_writer = csv.writer(data_csv, delimiter=',', quotechar='"')
    data_writer.writerow(['barcode','name','label','current_price','category_id'])
    for c,b,n in zip(product_category, product_barcode, product_name):
        p = price_hist_dict[b]['Price'][-1]
        data_writer.writerow([b,n,random.randint(0,1),p,c])

with open('csv_files/price.csv', 'w') as hist_csv:
    hist_writer = csv.writer(hist_csv, delimiter = ',', quotechar = '"')
    hist_writer.writerow(['barcode', 'start_date', 'end_date', 'amount'])
    for key,val in price_hist_dict.items():
        for i in range(len(val['Price'])):
            hist_writer.writerow([key, val['Start_date'][i], val['End_date'][i], val['Price'][i]])

with open('csv_files/customer.csv', 'w') as customer_csv:
    customer_writer = csv.writer(customer_csv, delimiter = ',', quotechar = '"')
    customer_writer.writerow(['card_id','name','reg_date','points','pet','sex','date_of_birth','street', 
                              'number','postal_code','city'])
    for key,val in customer_dict.items():
        customer_writer.writerow([key, val['Name'], val['Registration_date'], val['Points'], val['Pet'], 
                                  val['Sex'], val['DoB'], val['Address']['Street'], val['Address']['Number'], 
                                  val['Address']['Postal_code'], val['Address']['City']])

with open('csv_files/offers_products.csv', 'w') as offers_csv:
    offers_writer = csv.writer(offers_csv, delimiter = ',', quotechar = '"')
    offers_writer.writerow(['store_id','barcode','aisle','shelf'])
    for store,loc_dict in offers_dict.items():
        for barcode,val in loc_dict.items():
            offers_writer.writerow([store, barcode, val['Aisle'], val['Shelf']])

with open('csv_files/transaction.csv', 'w') as transaction_csv:
    transaction_writer = csv.writer(transaction_csv, delimiter = ',', quotechar = '"')
    transaction_writer.writerow(['transaction_id','total_amount','payment_method','timestamp','total_pieces',
                                 'store_id','card_id'])
    for key,val in transaction_dict.items():
        transaction_writer.writerow([key, '{:.2f}'.format(val['total_amount']), val['payment_method'], 
                                     val['timestamp'], val['total_pieces'], val['store_id'], val['card_id']])

with open('csv_files/buy_products.csv', 'w') as buy_csv:
    buy_writer = csv.writer(buy_csv, delimiter = ',', quotechar = '"')
    buy_writer.writerow(['transaction_id','barcode','quantity'])
    for key,val in transaction_dict.items():
        for b,q in zip(val['products'], val['quantity']):
            buy_writer.writerow([key, b, q])

category_name = ['Fresh products','Refrigerated products','Liquor','Personal care','Homeware','Pet products']
with open('csv_files/categories.csv', 'w') as categ_csv:
    categ_writer = csv.writer(categ_csv, delimiter = ',', quotechar = '"')
    categ_writer.writerow(['category_id','category_name'])
    for cid,cname in zip(range(1,7),category_name):
        categ_writer.writerow([cid, cname])