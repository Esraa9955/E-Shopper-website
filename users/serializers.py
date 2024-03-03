from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Profile
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # confirmPassword = serializers.CharField()
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'confirmPassword', 'phone', 'usertype', 'address', 'shopname', 'is_superuser', 'birthdate']
        extra_kwargs = {
            'password': {'required': True, 'allow_blank': False, 'min_length': 8},
            'confirmPassword': {'required': True, 'allow_blank': False,'min_length': 8 },
            'email': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
        }

    def validate_shopname(self, value):
        usertype = self.initial_data.get('usertype')
        if usertype == 'vendor' and not value:
            raise serializers.ValidationError("Shop name is required for vendors.")
        elif usertype != 'vendor' and value:
            raise serializers.ValidationError("Shop name is for vendors only.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirmPassword'):
            raise serializers.ValidationError("The passwords do not match.")
        return attrs

        

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        cpassword = validated_data.pop('confirmPassword', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        if cpassword is not None:
            instance.confirmPassword=password


        instance.save()
        return instance
    

    def update(self, instance, validated_data):
        # Only allow updating certain fields based on user type
        if instance.usertype == 'vendor':
            allowed_fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'shopname']
        else:
            allowed_fields = ['first_name', 'last_name', 'email', 'address', 'phone']

        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance
    
    def validate_phone(self, value):
        if not value.startswith('+20'):
            raise serializers.ValidationError("Mobile number must begin with +20.")
        return value
    