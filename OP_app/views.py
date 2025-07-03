from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Account.serializer import LeadSerializer
from rest_framework import status
from .models import Lead


# Create your views here.
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
