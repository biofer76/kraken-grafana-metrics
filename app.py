#
#
# Balance Result:
# {'error': [], 'result': {'ZUSD': '0.0000', 'XXBT': '0.0434289700'}}
# ISSUE WITH STRING VALUES
#
#

import os
import schedule
import time, datetime
import krakenex
from influxdb import InfluxDBClient

k = krakenex.API()
k.load_api_key(os.environ.get('KRAKEN_API_KEY'), os.environ.get('KRAKEN_API_SECRET'))

infx_client = InfluxDBClient(host=os.environ.get('INFLUXDB_HOST'), port=os.environ.get('INFLUXDB_PORT'))
infx_client.switch_database('db')


def collect():
    balance_result = k.query_private('Balance')
    balance_return = balance(balance_result)
    print(balance_return)

def balance(balance_result):
    # data = [
    #     {
    #         "measurement": "kraken_user_balance",
    #         "tags": {
    #             "exchange": "kraken",
    #             "app": "kraken-grafana-metrics"
    #         },
    #         "time": str(datetime.datetime.now()),
    #         "fields": json.dumps(balance_result)
    #     }
    # ]

    data = [
        {
            "measurement": "kraken_balance",
            "tags": {
                "exchange": "kranken"
            },
            "time": str(datetime.datetime.now()),
            "fields": {
                "USD": float(balance_result['result']['ZUSD']),
                "BTC": float(balance_result['result']['XXBT']),
            }
        }
    ]
    write_result = infx_client.write_points(data)
    query_result = infx_client.query('SELECT "duration" FROM "cpu_load_short"')
    return query_result


schedule.every(5).seconds.do(collect)

while 1:
    schedule.run_pending()
    time.sleep(1)

