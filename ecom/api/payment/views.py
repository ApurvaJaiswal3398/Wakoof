from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import braintree

# Create your views here.
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox,
        merchant_id='tx9vgt9n3ppjk667',
        public_key='x7kkympb2nkzfx5s',
        private_key='8baf48cffcae719fcc97865c0bebdfd2'
    )
)

def validate_user_session(id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False

@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session, Please Login Again!'})
    return JsonResponse({'clientToken': gateway.client_token.generate(), 'success':True})

@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session, Please Login Again!'})
    
    nonce_from_client = request.POST['paymentMethodNonce']
    amount_from_client = request.POST['amount']

    result = gateway.transaction.sale({
        'amount': amount_from_client,
        'payment_method_nonce': nonce_from_client,
        'options': {
            "submit_for_settlement": True
        }
    })
    
    if result.is_success:
        return JsonResponse({'success': result.is_success,'transaction': {'id': result.transaction.id, 'amount': result.transaction.amount}})
    else:
        return JsonResponse({'error': True, 'success': False})