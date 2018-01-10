from datetime import datetime
import logging
from django.dispatch import receiver
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

@receiver(PAYMENT_SENT)
def fund_mbta_and_send_receipt(request):
    fund_mbta(request)
    receipt = Receipt(request['user'], request['amount'])
    return receipt.render_html()

def fund_mbta(request):
    response = make_funding_request(request)
    if response.status_code >= 400:
        raise MyException('Request failed due to medical emergency at Charles/MGH')

    response_data = response.json()
    persist(response_data)

    fund_status = response.get('payment_status')
    if status != 'success':
        raise MyException('Unsuccessful payment. LOL')

def persist(data):
    # we pretend that logging data "persists" it
    log.warn(data)

def make_funding_request(request):
    params = {
        'user': request['user'],
        'amount': request['amount'],
        'item': request['item_id'],
    }
    headers = {}
    if request['use_auth']:
        headers = {'stuff_about_auth': request['auth_info']}
    url = 'http://mbta.payments.com/this/will/probably/fail/send_funds'
    return requests.post(url, params=params, headers=headers)
