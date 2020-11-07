from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from payu.models import Transaction
from payu.gateway import get_hash, capture_transaction, check_hash
from hashlib import sha512
import hashlib
from django.conf import settings
from assignment.settings import PAYU_MERCHANT_KEY, PAYU_MERCHANT_SALT


class GenerateHashKeyView(generics.GenericAPIView):
    """
    Class for creating API view for Payment gateway homepage.
    """
    permission_classes = ()

    def post(self, request, *args, **kwags):
        """
        Function for creating a charge.
        """
        key = PAYU_MERCHANT_KEY
        salt = PAYU_MERCHANT_SALT
        
        email = str(request.data.get('email'))
        firstname = str(request.data.get('firstname'))
        txnid = str(request.data.get('txnid'))
        amount = str(request.data.get('amount'))
        productinfo = str(request.data.get('productinfo'))
        

        data = {
            'key': key,
            'salt': salt,
            'email': email,
            'firstname': firstname,
            'txnid': txnid,
            'amount': amount,
            'productinfo': productinfo,
        }

        keys = ('txnid', 'firstname', 'email', 'amount', 'productinfo',
                'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7', 'udf8',
                'udf9', 'udf10')

        data['hash_key'] = get_hash(request.data)
        
        return Response(data)


class SuccessView(generics.GenericAPIView):
    """
    Transaction successful view
    """
    def post(self, request):
        status = request.data["status"]
        firstname = request.data["firstname"]
        amount = request.data["amount"]
        txnid = request.data["txnid"]
        posted_hash = request.data["hash"]
        key = request.data["key"]
        productinfo = request.data["productinfo"]
        email = request.data["email"]
        salt = PAYU_MERCHANT_SALT

        try:
            additional_charges = request.data["additionalCharges"]
            ret_hash_seq = additional_charges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname +\
                           '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
        except Exception:
            ret_hash_seq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|'\
                         + amount + '|' + txnid + '|' + key

        resonse_hash = hashlib.sha512(ret_hash_seq.encode()).hexdigest().lower()

        if resonse_hash == posted_hash:
            
            #update transaction details
            transaction = Transaction.objects.get(transaction_id=txnid)
            transaction.payment_gateway_type = request.data.get('PG_TYPE')
            transaction.transaction_date_time = request.data.get('addedon')
            transaction.mode = request.data.get('mode')
            transaction.status = status
            transaction.amount = amount
            transaction.mihpayid = request.data.get('mihpayid')
            transaction.bankcode = request.data.get('bankcode')
            transaction.bank_ref_num = request.data.get('bank_ref_num')
            transaction.discount = request.data.get('discount')
            transaction.additional_charges = request.data.get('additionalCharges', 0)
            transaction.txn_status_on_payu = request.data.get('unmappedstatus')
            transaction.hash_status = "Success" if resonse_hash == request.data.get('hash') else "Failed"
            transaction.save()
            
            message = ["Thank You. Your order status is " + status,
                       "Your Transaction ID for this transaction is " + txnid,
                       "We have received a payment of Rs. " + amount,
                       "Your order will soon be shipped."]
        else:
            message = ["Invalid Transaction. Please try again."]

        output_data = {
            "txnid": txnid,
            "status": status,
            "amount": amount
        }
        return Response(output_data, message)