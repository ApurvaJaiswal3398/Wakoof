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
