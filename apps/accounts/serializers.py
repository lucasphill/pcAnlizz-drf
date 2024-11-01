from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.accounts.models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    detail_link = serializers.SerializerMethodField()
    class Meta:
        password = serializers.CharField(
            style={'input_type': 'password'}
        )
        model = User
        fields = ['detail_link', 'id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined', 'groups', 'user_permissions']       

    def get_detail_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/details/{obj.id}/')

import django.contrib.auth.password_validation as validators

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text='Will be used to login and shown in the system',
        style={'placeholder': 'Username'}
    )
    email = serializers.CharField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text='Insert unique and valid email',
        style={'placeholder': 'email@email.com'}
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        # min_length=8,
        help_text='Insert a strong password',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Confirm password',
        style={'input_type': 'password', 'placeholder': 'Confirm password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def create(self, data):
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password_confirm'])
        user.save()
        return user
        
    def validate(self, validated_data):
        validators.validate_password(validated_data['password'])

        if validated_data['password'] != validated_data['password_confirm']:
            raise serializers.ValidationError({"password_confirm":"Password doesn't match"})
        return validated_data