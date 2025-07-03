from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.contrib.auth import authenticate
# from rest_framework.permissions import IsAuthenticated, AllowAny
from Account.serializer import RegisterSerializer,LoginSerializer
from rest_framework import status




class RegisterView(APIView):  
    def post(self, request):
        print("USER:", request.user)

        try:
            data = request.data
            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
                
        except Exception as e:
            return Response({"error": str(e)}, status=500)
          
           
        

class LoginView(APIView):  
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=400)

            response = serializer.get_jwt_token(serializer.validated_data)

            return Response(response, status=200)
    
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        

