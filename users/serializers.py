from rest_framework import serializers
from .models import UserProfile, EmailOTP
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import random
from rest_framework import serializers
from .models import EmailOTP, UserProfile
from django.utils import timezone
from orders.models import Order
from orders.serializers import OrderSerializer
from utils.email_utils import send_otp_email


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField()
    address = serializers.CharField()

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_username(self, value):
        if UserProfile.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']
        phone = validated_data['phone']
        address = validated_data['address']

        # Send OTP
        otp = random.randint(100000, 999999)
        EmailOTP.objects.update_or_create(email=email, defaults={'otp': otp})

        send_otp_email(user, otp, user.email)

        # Create user with is_verified=False
        user = UserProfile.objects.create_user(
            email=email,
            username=username,
            password=password,
            phone=phone,
            address=address,
            is_verified=False,
            is_active=False,  # optional, will activate after OTP
        )

        return {
            "email": email,
            "message": "OTP sent successfully. Please verify to complete registration."
        }




class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

    def validate(self, data):
        try:
            otp_obj = EmailOTP.objects.get(email=data['email'])
            print("DB OTP:", otp_obj.otp, "User Entered OTP:", data['otp'])
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("OTP not found. Please register again.")

        if otp_obj.otp != data['otp']:
            raise serializers.ValidationError("Incorrect OTP.")

        return data

    def save(self, **kwargs):
        email = self.validated_data['email']

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("User not found. Please register again.")

        user.is_verified = True
        user.is_active = True  # Optional, if you had set it False initially
        user.save()

        EmailOTP.objects.filter(email=email).delete()

        return {"message": "Email verified successfully."}



class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        identifier = data.get("email_or_username")
        password = data.get("password")

        user = UserProfile.objects.filter(email=identifier).first() or \
               UserProfile.objects.filter(username=identifier).first()

        if not user:
            raise serializers.ValidationError("User not found.")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        if not user.is_verified:
            raise serializers.ValidationError("Email not verified.")

        data["user"] = user
        return data


class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, error_messages={'required': 'Please provide password'})
    email = serializers.EmailField(error_messages={'required': 'Please provide email'})
    username = serializers.CharField(error_messages={'required': 'Please provide username'})
    phone = serializers.CharField(error_messages={'required': 'Please provide phone number'})
    address = serializers.CharField(error_messages={'required': 'Please provide address'})

    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'password', 'phone', 'address']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserProfile.objects.create_user(
            **validated_data,
            is_admin=True,
            is_verified=True,
            is_active=True
        )
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many = True, read_only = True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'phone', 'address', 'is_verified', 'orders']
        # fields = ['id', 'username', 'email', 'phone', 'address', 'is_verified', 'orders']
        # exclude = ['password']
