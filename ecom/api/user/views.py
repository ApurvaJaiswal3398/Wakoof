from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import random
import re

# Create your views here.
def generate_session_token(length = 10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(length))

@csrf_exempt    # TO tell Django that the sign up using othee origin request
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a POST Request with valid paramenters only'})
        # Extracting Username (email) and Password using the POST method
    username = request.POST['email']    # Since Django treats it as a username, hence the name
    password = request.POST['password']
        # Validations
    if not re.match("\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b", username):
        return JsonResponse({'error': 'Enter a Valid Email'})
    
    if len(password) < 6:
        return JsonResponse({'error': 'Password needs to be atleast 6 characters'})
        # Grabbing User Model
    UserModel = get_user_model()
    
    try:
        user = UserModel.objects.get(email=username)    # Get user with the given email
        if user.check_password(password):   # Match the password
                # get all users with the given email (which is only one), extract their (its) password
            usr_dict = UserModel.objects.filter(email=username).values().first()    
            usr_dict.pop('password')    # Removing passwor dfrom the details so that it does not reach the frontend
            
            if user.session_token !=  '0':  # If session exists already for the user
                user.session_token = '0'    # Setting sessiojn to zero
                user.save()
                return JsonResponse({'error': 'Previous Session Exists!'})
            
            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)    # Login done by Django
            return JsonResponse({'token': token, 'user': usr_dict}) # Here usr_dict does not contain password
        else:
            return JsonResponse({'error': 'Invalid Password!'})      
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email!'})
    
def signout(request, id):
    logout(request) # Let Django log out
    UserModel = get_user_model()    # Grabbing User Model
    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = '0'
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid User Id!'})
    return JsonResponse({'success': 'Logged Out Successfully'})

class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]