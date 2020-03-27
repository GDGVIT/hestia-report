from rest_framework.views import APIView
from rest_framework.response import Response

from .local_helper_functions import (
    authorization, 
    getting_user
)

from .models import(
    ReportUser,
    CreateShopRecommendation
)

from .serializers import (
    ReportUserSerializer,
    CreateShopRecommendationSerializer
)

class ReportingUsersView(APIView):

    def get(self, request):
        
        authorization_check = authorization(request)
        if authorization_check:
            return authorization_check

        user_check = getting_user(request)

        if user_check['status'] == 'error':
            Response.status_code = 412
            return Response({
                "status": "error",
                "message": user_check["message"],
                "payload": ""
            })
        else:
            reports = ReportUser.objects.filter(user_id=user_check['message']['_id'])
            serializer = ReportUserSerializer(reports, many=True)
            return Response({
                "status": "success",
                "message": "Successfully retrieved user reports",
                "payload": serializer.data
            })

    def post(self, request):
        
        authorization_check = authorization(request)
        if authorization_check:
            return authorization_check
        
        
        user_check = getting_user(request)
        if user_check['status'] == 'error':
            Response.status_code = 412
            return Response({
                "status": "error",
                "message": user_check["message"],
                "payload": ""
            })
        else:
            data = request.data
            data['user_id'] = user_check["message"]["_id"]
            report_serializer = ReportUserSerializer(data=data)
            
            if report_serializer.is_valid():
                report_serializer.save()
                print("User with id {} successfully reported".format(user_check["message"]["_id"]))
                Response.status_code = 201
                return Response({
                    "status": "success",
                    "message": "User successfully reported",
                    "payload" : report_serializer.data
                })
            else:
                Response.status_code = 400
                return Response({
                    "status": "error",
                    "message": report_serializer.errors,
                    "payload" : ""
                })


class CreateShopRecommendationView(APIView):
    
    def get(self, request):
        
        authorization_check = authorization(request)
        if authorization_check:
            return authorization_check

        user_check = getting_user(request)
        if user_check['status'] == 'error':
            Response.status_code = 412
            return Response({
                "status": "error",
                "message": user_check["message"],
                "payload": ""
            })
        else:

            shop_recommendation = CreateShopRecommendation.objects.filter(user_id=user_check["message"]["_id"])
            serializer = CreateShopRecommendationSerializer(shop_recommendation, many=True)
            return Response({
                "status": "success",
                "message": "Successfully retrieved shop recommendations",
                "payload": serializer.data
            })

    def post(self, request):
        
        authorization_check = authorization(request)
        if authorization_check:
            return authorization_check
        
        
        user_check = getting_user(request)
        if user_check['status'] == 'error':
            Response.status_code = 412
            return Response({
                "status": "error",
                "message": user_check["message"],
                "payload": ""
            })

        else:
            data = request.data
            data['user_id'] = user_check["message"]["_id"]
            recommendation_serializer = CreateShopRecommendationSerializer(data=data)
            
            if recommendation_serializer.is_valid():
                recommendation_serializer.save()
                print("Recommendation successfully added")
                Response.status_code = 201
                return Response({
                    "status": "success",
                    "message": "Recommendation successfully added",
                    "payload" : recommendation_serializer.data
                })
            else:
                Response.status_code = 400
                return Response({
                    "status": "error",
                    "message": recommendation_serializer.errors,
                    "payload" : ""
                })


class CreateShopRecommendationUpdateView(APIView):
    recommendations = CreateShopRecommendation.objects.all()
    def get(self, request):

        authorization_check = authorization(request)
        if authorization_check:
            return authorization_check
        
        
        user_check = getting_user(request)
        if user_check['status'] == 'error':
            Response.status_code = 412
            return Response({
                "status": "error",
                "message": user_check["message"],
                "payload": ""
            })

        else:

            serializer = CreateShopRecommendationSerializer(
                self.recommendations.filter(read_by_user=0, recommended_for=user_check["message"]["_id"]), 
                many=True
                )
            return Response({
                "status": "success",
                "message": "Fetched all unread recommendations",
                "payload": serializer.data
            })

    def post(self, request):

        authorization_check = authorization(request)
        if authorization_check:
            return authorization_check
        
        
        user_check = getting_user(request)
        if user_check['status'] == 'error':
            Response.status_code = 412
            return Response({
                "status": "error",
                "message": user_check["message"],
                "payload": ""
            })

        else:
                
            if 'report_ids' not in request.data:
                Response.status_code = 400
                return Response({
                    "status": "Error",
                    "message" : "Need a list of report_ids to",
                    "payload": ""
                })
            
            objects = self.recommendations.filter(
                id__in=request.data.get('report_ids')
                )
            serializer = CreateShopRecommendationSerializer(objects, many=True)
            objects.update(read_by_user=1)
            
            Response.status_code = 202
            return Response({
                "status": "success",
                "message": "Updated the recommendation status",
                "payload": serializer.data
            })