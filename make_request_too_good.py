from datetime import datetime
import logging

import requests


log = logging.getLogger(__name__)


class MyException(Exception):
    pass


class Receipt():
    def __init__(self, user, amount=0):
        self.user = user
        self.amount = amount
        self.timestamp = datetime.utcnow()

    def render_html(user, amount):
        return "<h1>Your Receipt</h1><p>The user: {user}</p><p>Amount: {amount}</p><p>Timestamp {timestamp}</p>".format(
            user=self.user,
            amount=self.amount,
            timestamp=self.timestamp
        )


def fund_mbta_and_send_receipt(request):
    # make a call to fund the MBTA
    response = make_funding_request(request)
    check_fund_response_status(response)    
    response_data = response.json()
    persist(response_data)
    check_payment_status(response)

    # return a receipt
    receipt = make_receipt(request)
    return receipt.render_html()


def make_funding_request(request):
    params = make_params(request)
    headers = make_headers(request)
    url = 'http://mbta.payments.com/this/will/probably/fail/send_funds'
    response = requests.post(url, params=params, headers=headers)
    return response


def make_params(request):
    return {
        'user': request['user'],
        'amount': request['amount'],
        'item': request['item_id'],
    }

def make_headers(request):
    if request['use_auth']:
        return {'stuff_about_auth': request['auth_info']}
    return {}


def check_fund_response_status(response):
    if response_status_is_bad(response):
        raise MyException('Request failed due to medical emergency at Charles/MGH')


def response_status_is_bad(response):
    return response.status_code >= 400


def persist(data):
    log.warn(data)


def check_payment_status(response):
    fund_status = response.get('payment_status')
    if not status_is_successful(fund_status)
        raise MyException('Unsuccessful payment. LOL')


def status_is_successful(status):
    return status == 'success'


def make_receipt(request):
    return Receipt(request['user'], request['amount'])
