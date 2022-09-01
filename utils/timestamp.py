from datetime import datetime, timedelta 
import settings

def generate_timestamp_for_now():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return timestamp

def generate_timestamp_for_current_minute():
    now = datetime.now()
    timestamp = datetime.timestamp(now.replace(second=0, microsecond=0))
    return timestamp

def generate_timestamp_before_time_delta(time_delta=None):
    if time_delta is None:
        time_delta = settings.time_delta
    now = datetime.now()
    time_delta = now + timedelta(minutes = - time_delta)
    timestamp = datetime.timestamp(time_delta.replace(second=0, microsecond=0))
    return timestamp

def timestamp_to_date(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return date


# default python timestamp which is float  should be converted to integer for using it in bybit and binance.
# python default timestamp takes 10 digits of float, 
# such as 1657162928.09135
def convert_timestamp_to_int(timestamp):
    # type of text which includes floatting point cannot be directly converted to type of integer.
    float_timestamp = float(timestamp)
    int_timestamp = int(float_timestamp)
    return int_timestamp

# timestamp used in bybit and binance is different.
# bybit adopts timestamp of 16 float type, such as 1567109419.049271.
# bybit can take 10 digits of integer timestamp. Therefore, no need to convert from python default timestamp.
# However, binance adopts timestamp of 13 digits integer type, such as 1591702613943.
# therefore, conversion between python default timestamp and binance timestamp is essential.
# We need timestamp of 10 digits of integer!!!!!

# binance timestamp to python timestamp 
# firstly, convert binance timestamp of 13 digits to 10 digits
# secondly, convert it to integer type <- just in case
def binance_timestamp_to_python_timestamp(binance_timestamp):
    timestamp = binance_timestamp / 1000
    timestamp = convert_timestamp_to_int(timestamp)
    return timestamp

# python timestamp to binance timestamp
def python_timestamp_to_binance_timestamp(python_timestamp):
    timestamp = convert_timestamp_to_int(python_timestamp)
    timestamp = timestamp * 1000
    return timestamp



if __name__ == '__main__':
    pass
    # Do TEST in main.py
    # from app.models.timestamp import (
    #     generate_timestamp_for_now,
    #     generate_timestamp_for_current_minute,
    #     generate_timestamp_before_time_delta,
    #     convert_timestamp_to_int,
    #     timestamp_to_date
    # )
    # from datetime import datetime
    # # get data of timestamp
    # now = datetime.now()
    # current_timestamp = generate_timestamp_for_now()
    # current_minutes = generate_timestamp_for_current_minute()
    # time_1 = generate_timestamp_before_time_delta(10)
    # time_2 = generate_timestamp_before_time_delta()
    # print(now)
    # print(current_timestamp)
    # print(current_minutes)
    # print(time_1)
    # print(time_2)
    # # to_integer
    # int_current_timestamp = convert_timestamp_to_int(current_timestamp)
    # print(int_current_timestamp)
    # int_current_minutes = convert_timestamp_to_int(current_minutes)
    # print(int_current_minutes)
    # int_time_1 = convert_timestamp_to_int(time_1)
    # print(int_time_1)
    # int_time_2 = convert_timestamp_to_int(time_2)
    # print(int_time_2)
    # # to_date_form_timestamp
    # print(timestamp_to_date(int_current_timestamp))
    # print(timestamp_to_date(int_current_minutes))
    # print(timestamp_to_date(int_time_1))
    # print(timestamp_to_date(int_time_2))
    
