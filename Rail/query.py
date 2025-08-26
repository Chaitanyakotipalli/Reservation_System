from django.db import connection
from .functions import *

def get_trains(from_des,to_des,date,category):


    all_trains = None


    train_query = """
        call route_lookup('%s','%s','%s'); ; 
    """ % (from_des,to_des,date)

    all_trains=execute_sql(train_query)

    for train in all_trains:
        train["Start_station_details"] = get_station_details(train["Start_station_id"])
        train["End_station_details"] = get_station_details(train["End_station_id"])
        train["Seat_availability"] = get_seat_available(train["Route_id"],category)
        train["Train_name"] = get_train_name(train["Train_id"])
        train["category"] = category


    print(all_trains)
    return all_trains

def get_seat_available(route_id,category="NA"):
    available_table =  execute_sql("CALL seat_avail(%s)"%(route_id))
    
    Seat_availability = {}
    for row in available_table:
        Seat_availability[row["seat_class"]] = (row["available_seats"] - get_num_WL(route_id,row["seat_class"]),get_price(route_id,row["seat_class"],category))
    return Seat_availability

def get_num_WL(route_id,S_class):
    query = """
    SELECT count(*) as total FROM dbms.rail_bookings where Booking_Status="WL" and Route_id = %s and Seat_no like '%s%%';
    """ % (route_id,S_class)
    print(query)
    return execute_sql(query)[0]["total"]

def get_price(route_id,S_cls,category="NA"):
    query = """
        SELECT Taxable_value as price FROM dbms.rail_ticket_price where Route_id=%s and Seat_class="%s";
    """ % (route_id,S_cls)
    price = execute_sql(query)[0]["price"]
    if category=='SEC':
        price = (price*80)//100
    elif category=="STD":
        price = (price*70)//100

    print(category,price)

    return price

def get_station_details(id):
    query = "SELECT Station_name ,District from dbms.rail_stations where id = %s ;" % id
    station = execute_sql(query)
    if len(station)==0:
        return ""
    return station[0]

def get_train_name(train_id):
    query = "SELECT Train_name from dbms.rail_trains where Train_id = %s ;" % train_id
    station = execute_sql(query)
    if len(station)==0:
        return ""
    return station[0]["Train_name"]

def route_not_exit(route_id):
    query = "SELECT count(*) as cnt from dbms.rail_routes where Route_id = %s ;" % route_id
    station = execute_sql(query)
    if station[0]["cnt"] == 1:
        return False
    else:
        return True
    
def seats_not_exist(route_id,S_cls):
    query = "SELECT count(*) as cnt from dbms.rail_seats where Route_id = %s and Seat_class = '%s';" % (route_id,S_cls)
    seats = execute_sql(query)
    if seats[0]["cnt"] == 0:
        return True
    else:
        return False
    
def get_ticket_details(route_id,S_cls='SL',category="NA"):
    train_query = """
        SELECT * FROM dbms.rail_routes where Route_id = %s ;
    """ % route_id

    query_output=execute_sql(train_query)
    train_details = {}

    if len(query_output) != 1:
        return train_details
    
    train_details = query_output[0]
    train_details["Start_station_details"] = get_station_details(train_details["Start_station_id"])
    train_details["End_station_details"] = get_station_details(train_details["End_station_id"])
    train_details["bill"] = get_bill(route_id,S_cls,category)
    train_details["category"] = category
    train_details["Train_name"] = get_train_name(train_details["Train_id"])

    return train_details

def get_bill(route_id,S_cls,category="NA"):
    query = """
        SELECT Seat_class, Taxable_value, CGST, CESS, Taxable_value+ CGST+ CESS+ Route_id as total FROM dbms.rail_ticket_price where Route_id=%s and Seat_class="%s";
    """ % (route_id,S_cls)

    price = {}
    output = execute_sql(query)

    if len(output)!=0:
        price = output
    else:
        return price

    if category=='SEC':
        price["discount"] = (price["Taxable_value"]*20)//100
    elif category=="STD":
        price["discount"] = (price["Taxable_value"]*30)//100
    else :
        price["discount"] = 0

    price["total"] -= price["discount"]
    return price

def confirm_booking(data,route_id,S_cls,category="NA"):
    query = """
        call insert_booking("%s","%s","%s","%s","%s",%s,"%s");
    """ % (data["name"],data["Phone_no"],"2005-10-10","ON",S_cls,route_id,category)

    return execute_sql(query)[0]

def cancel_booking(PNR):
    query = """
        call cancellation(%s);
    """% PNR

    message = execute_sql(query)[0]["Message"]

    if(message == "done"):
        return True
    else:
        return False
    
def get_user_pnr(PNR):
    query = """
        call PNR_details_to_user(%s);
    """% PNR

    return execute_sql(query)[0]


def get_train(train_id,date):
    train_query = """
    select * from rail_routes where train_id = %s and date(Start_time) = "%s";
""" % (train_id,date)
    print(train_query)
    all_trains=execute_sql(train_query)

    for train in all_trains:
        train["Start_station_details"] = get_station_details(train["Start_station_id"])
        train["End_station_details"] = get_station_details(train["End_station_id"])
        train["Seat_availability"] = get_seat_available(train["Route_id"])
        train["Train_name"] = get_train_name(train["Train_id"])

    print(all_trains)
    return all_trains

def get_passengers(train_id,date):
    query = """
    call  passenger_list(%s,"%s");
""" % (train_id,date)
    
    return execute_sql(query)

def get_wl_passengers(train_id,date):
    query = """
    call  list_passenger_wl(%s,"%s");
""" % (train_id,date)
    
    return execute_sql(query)

def get_refund_amount(route_id):
    query = """
    call  refund_amount(%s);
""" % (route_id)
    
    return execute_sql(query)

def get_revenue(from_date,to_date):
    query = """
    call  Revenue_over_time('%s','%s');
""" % (from_date,to_date)
    
    return execute_sql(query)[0]

def get_refunded_list():
    query = """
    call  cancellation_records();
"""
    return execute_sql(query)

def get_busiest_route():
    query = """
    call busy_routes();
"""
    return execute_sql(query)[0]
