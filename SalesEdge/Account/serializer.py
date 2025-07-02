from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile, Lead

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        print(data)
        return data
    
    def create(self, validated_data):
        role = validated_data.pop("role")
        user =User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(user=user, role=role)
        
        return validated_data
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("User does not exist.")
        return data
    
    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            return{'message': 'Invalid credentials'}
        refresh = RefreshToken.for_user(user)

        return {'message': 'Login successful', 'refresh': str(refresh), 'access': str(refresh.access_token)}
    


class LeadSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(userprofile__role="salesperson"),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Lead
        fields = "__all__"
