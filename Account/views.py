from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from Account.serializer import RegisterSerializer,LoginSerializer,LeadSerializer
from rest_framework import status
from .models import UserProfile,Lead
import pandas as pd






class RegisterView(APIView):
    
    
    def post(self, request):
        print("USER:", request.user)

        try:
            # if request.user.userprofile.role == "admin":
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
        


class OPLeaderView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        try:
            if request.user.userprofile.role == "operations_lead":
                leads = Lead.objects.get(accounts_status="verified")
                return Response({'leads': leads})
            else:
                return Response({"error": "Unauthorized"}, status=403)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    def patch(self, request):
        try:
            data = request.data
            lead = Lead.objects.get(uid= data.get('uid'))

            serializer = LeadSerializer(lead,data=data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)      
            #changing only status here            
            new_status = request.data.get("operations_status")
            if not new_status:
                return Response({"error": "Missing 'status' field"}, status=400)

            lead.sales_status = new_status
            lead.save()    
            serializer = LeadSerializer(lead)
            return Response(
                {'data': serializer.data,
                 "message": "Lead updated successfully"},
                status=status.HTTP_200_OK
            )
        except Lead.DoesNotExist:   
            return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SalesExecutiveView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        try:
            if request.user.userprofile.role == "sales_executive":
                leads = Lead.objects.filter(assigned_to=request.user,
                                         sales_status__in=["new", "contacted", "qualified"])
                serializer = LeadSerializer(leads, many=True)
                return Response({'leads': serializer.data})
            else:
                return Response({"error": "Unauthorized"}, status=403)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    def patch(self, request):
        try:
            data = request.data
            lead = Lead.objects.get(uid= data.get('uid'))

            serializer = LeadSerializer(lead ,data=data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)  
            #changing only status here            
            new_status = request.data.get("sales_status")
            if not new_status:
                return Response({"error": "Missing 'status' field"}, status=400)

            lead.sales_status = new_status
            lead.save()    
            serializer = LeadSerializer(lead)
            return Response(
                {'data': serializer.data,
                 "message": "Lead updated successfully"},
                status=status.HTTP_200_OK
            )
        except Lead.DoesNotExist:   
            return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class AccountsManagerView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        try:
            if request.user.userprofile.role == "accounts_manager":
                leads = Lead.objects.filter(sales_status="converted")
                serialized_leads = LeadSerializer(leads, many=True)


                return Response({'leads': serialized_leads.data})
            else:
                return Response({"error": "Unauthorized"}, status=403)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    def patch(self, request):
        try:
            data = request.data
            lead = Lead.objects.filter(uid= data.get('uid'))

            serializer = LeadSerializer(lead[0] ,data=data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)      
            #changing only status here            
            new_status = request.data.get("accounts_status")
            if not new_status:
                return Response({"error": "Missing 'status' field"}, status=400)

            lead.sales_status = new_status
            lead.save()    
            serializer = LeadSerializer(lead)
            return Response(
                {'data': serializer.data,
                 "message": "Lead updated successfully"},
                status=status.HTTP_200_OK
            )
        except Lead.DoesNotExist:   
            return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AdminView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            if request.user.userprofile.role == "admin":
                leads = Lead.objects.all()
                serialized_leads = LeadSerializer(leads, many=True)
                return Response({'leads': serialized_leads.data})
            else:
                return Response({"error": "Unauthorized"}, status=403)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    def patch(self, request):
        try:
            data = request.data
            lead = Lead.objects.get(uid= data.get('uid'))
            serializer = LeadSerializer(lead ,data=data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            serializer.save()
            return Response(
                {'data': serializer.data,
                 "message": "Lead updated successfully"},
                status=status.HTTP_200_OK
            )
        except Lead.DoesNotExist:
            return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        try:
            data = request.data
            lead = Lead.objects.filter(uid=data.get('uid'))
            if not lead.exists():
                return Response({"error": "Lead not found"}, status=status.HTTP_404_NOT_FOUND)
            lead.delete()
            return Response({"message": "Lead deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            excel_file = request.FILES.get('excelfile')
            if not excel_file:
                return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                cd = {
                'name' : row['Name'],
                'email' : row['Email'],
                'phone' : row['Phone'],
                'source' : row['Source']
                }
                serializer = LeadSerializer(data=cd)
                if not serializer.is_valid():
                        return Response(serializer.errors, status=400)
                serializer.save()
            return Response({"message": "Leads registered successfully"}, status=201)
                
        except Exception as e:
            return Response({"error": str(e)}, status=500)