from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Profile
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password','confirm_password','phone', 'usertype', 'address', 'shopname', 'is_superuser']
        # not show pass to user
        extra_kwargs = {
            'password': {'required': True, 'allow_blank': False, 'min_length': 8, 'write_only': True},
            'confirm_password': {'required': True, 'allow_blank': False,'min_length': 8, 'write_only': True },
            'email': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            # 'username': {},
        }

    def validate_shopname(self, value):
        usertype = self.initial_data.get('usertype')
        if usertype == 'vendor' and not value:
            raise serializers.ValidationError("Shop name is required for vendors.")
        elif usertype != 'vendor' and value:
            raise serializers.ValidationError("Shop name is for vendors only.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError("The passwords do not match.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    