from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from utils.email_utils import send_new_otp_email
from .filters import *
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import UserProfile
from django.utils import timezone
from .permissions import IsAdminUser

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=200)
        return Response(serializer.errors, status=400)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Email verified successfully."}, status=200)
        return Response(serializer.errors, status=400)

class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            otp_entry = EmailOTP.objects.get(email=email)
            user = UserProfile.objects.get(email=email)
            # Generate new OTP
            new_otp = random.randint(100000, 999999)
            otp_entry.otp = new_otp
            otp_entry.created_at = timezone.now()
            otp_entry.save()

            # Send email
            send_new_otp_email(user, new_otp, email)

            return Response({"message": "OTP resent successfully."}, status=200)

        except EmailOTP.DoesNotExist:
            return Response({"error": "Email not found or not registered."}, status=404)
        

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=200)
        return Response(serializer.errors, status=400)
    
    
class AdminRegisterView(APIView):
    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin registered successfully."}, status=201)
        return Response(serializer.errors, status=400)
    

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=200)



class GetAllUsersView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserProfileFilter