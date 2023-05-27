from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.signin, name='signin'),
    path('logout/<int:id>/', views.signout, name='signout'),
]