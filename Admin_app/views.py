from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Account.serializer import LeadSerializer
from rest_framework import status
from .models import  Lead
import pandas as pd 

# Create your views here.
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