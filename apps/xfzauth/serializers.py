from rest_framework import  serializers
from .models import User

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields =('uuid','telephone','username','email','is_staff','is_active')