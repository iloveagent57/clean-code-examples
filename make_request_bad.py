from datetime import datetime
import logging
from django.dispatch import receiver
import requests

class MyException(Exception):
    pass

@receiver(PAYMENT_SENT)
def fund_mbta_and_send_receipt(request):
    # make a call to fund the MBTA
    params = {
        'user': request['user'],
        'amount': request['amount'],
        'item': request['item_id'],
    }
    headers = {}
    if request['use_auth']:
        headers = {
            'stuff_about_auth': request['auth_info']
        }
    url = 'http://mbta.payments.com/this/will/probably/fail/send_funds'
    fund_request = requests.post(url, params=params, headers=headers)
    response = fund_request.json()

    if response.status_code >= 400:
        raise MyException('Request failed due to medical emergency at Charles/MGH')

    fund_status = response.get('payment_status')
    log.warn(fund_status) # pretend that this persists the data

    if fund_status != 'success':
        raise MyException('Unsuccessful payment. LOL')

    return "<h1>Your Receipt</h1><p>The user: {user}</p><p>Amount: {amount}</p><p>Timestamp {timestamp}</p>".format(
        user=request['user'],
        amount=response.get('amount'),
        timestamp=datetime.utcnow()
    )
