from django.db import connection

def get_train_id(ids):
    s = ','.join([str(x["id"]) for x in ids])
    
    print(s)  # 1
    return s

def execute_sql(query):
    out = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        out=dictfetchall(cursor)
    return out

def pnr_exist(PNR):
    query = """
        select exists(select * from rail_bookings where PNR= %s) as exist;
    """% PNR
    if(execute_sql(query)[0]["exist"] == 1):
        return True
    else:
        return False
    
def get_routid_pnr(PNR):
    query = """
    select route_id from rail_bookings where PNR= %s;
    """% PNR
    return execute_sql(query)[0]["route_id"]

def get_booking_details(PNR):
    query = """
        SELECT PNR,Booking_Status,Transaction_id,Booking_Catogory,Seat_no as Seat_id,user_id from rail_bookings where PNR = %s;            
""" % PNR
    return execute_sql(query)[0]

def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    if cursor.description == None:
        return []
    
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]