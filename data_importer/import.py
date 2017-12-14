import pysher

from influxdb import InfluxDBClient
# Add a logging handler so we can see the raw communication data
import logging
import sys
import time
import json
import datetime

log = logging.getLogger()
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
log.addHandler(ch)

pusher = pysher.Pusher('de504dc5763aeef9ff52')

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able


"""Instantiate a connection to the InfluxDB."""
host = "influxdb"
port = 8086
user = 'root'
password = 'root'
dbname = 'bitstamp_ltc'


client = InfluxDBClient(host, port, user, password, dbname)

log.info("Create database: " + dbname)
client.create_database(dbname)


def connect_handler(data):

    channel = pusher.subscribe('live_trades_ltceur')
    channel.bind('trade', handler)


def handler(data):

    transaction_data = json.loads(data)
    data_list = []
# {'buy_order_id': 592937652, 'sell_order_id': 592932336, 'price': 252.8, 'amount': 0.19338406, 'amount_str': '0.19338406', 'timestamp': '1513206525', 'id': 32620182, 'type': 0, 'price_str': '252.80'}
    transaction_time = transaction_data.get('timestamp')
    order_time = datetime.datetime.fromtimestamp(int(transaction_time))

    order_type = ""

    if transaction_data.get('type') == 1:
        order_type = "sell"
    else:
        order_type = "buy"

    point_values = {
        "measurement": "ltc_price",
        "time": order_time,
        "fields": {
            "price": transaction_data.get('price'),
            "amount": transaction_data.get('amount'),
            "buy_order_id": transaction_data.get("buy_order_id"),
            "sell_order_id": transaction_data.get('sell_order_id'),
            "order_type": order_type}
    }

    data_list.append(point_values)
    client.write_points(data_list)


pusher.connection.bind('pusher:connection_established', connect_handler)
pusher.connect()

log.info('Waiting for events....')

while True:
    # Do other things in the meantime here...
    time.sleep(1)
