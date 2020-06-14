from django.contrib.auth import get_user_model
from rest_framework import serializers

from contacts.models import Contact

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
                    mobile=validated_data.get('mobile'),
                    password=validated_data.get('password'),
                    full_name=validated_data.get('full_name'),
                    email=validated_data.get('email'),
                )
        return user
