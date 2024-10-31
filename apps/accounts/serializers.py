from rest_framework import serializers
from apps.accounts.models import User


# class UserSerializer(serializers.ModelSerializer ):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined', 'groups', 'user_permissions']
#         # extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        password = serializers.CharField(
            style={'input_type': 'password'}
        )
        model = User
        fields = "__all__"

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user