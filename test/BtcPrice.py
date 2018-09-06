import requests
import time

BTC_PRICE_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS = 'https://maker.ifttt.com/trigger/{}/with/key/{}'
EVENT_NAME = 'btc_price'
KEY = ''

WHAT_YOU_WANT = 6000


# nohup python BtcPrice.py > btc.log &

def get_btc_price():
    response = requests.get(BTC_PRICE_URL)
    try:
        return float(response.json()[0]['price_usd'])
    except Exception as e:
        print(e)
        raise RuntimeError("Unable to get BTC price")


def post_ifttt_webhooks(value_json):
    requests.post(url=IFTTT_WEBHOOKS.format(EVENT_NAME, KEY), data=value_json)


if __name__ == '__main__':
    while True:
        price = get_btc_price()
        # if price <= WHAT_YOU_WANT:
        post_ifttt_webhooks(value_json={"value1": str(price)})
        time.sleep(5 * 60)
