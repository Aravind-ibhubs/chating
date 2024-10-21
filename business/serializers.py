from rest_framework import serializers
from business.models import User

class UserSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    is_staff = serializers.BooleanField(default=False)
    is_admin = serializers.BooleanField(default=False)
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)

