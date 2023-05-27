from rest_framework import serializers
    # Allows to bring password to plain text format, and hashes them
from django.contrib.auth.hashers import make_password
    # Allows write/add something to the predefined things remotely
from rest_framework.decorators import authentication_classes, permission_classes
from .models import CustomUser

class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password', None) #Getting user entered password
        instance = self.Meta.model(**validated_data)    #Saving it to the password created in the model
        
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
    class Meta:
        model = CustomUser
        extra_kwargs = {'password': {'write_only': True}}
            # All attributes defined in CustomUser, whereas is_active, is_staff and is_superuser is inherited from AbstractUser
        fields = ('name', 'email', 'password', 'phone', 'gender', 'is_active', 'is_staff', 'is_superuser')