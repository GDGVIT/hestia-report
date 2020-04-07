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
            #data['user_id'] = user_check["message"]["_id"]
            data['reported_by'] = user_check["message"]["_id"]
            report_serializer = ReportUserSerializer(data=data)
            
            if report_serializer.is_valid():
                
                reported_by=user_check["message"]["_id"]
                user_id=request.data.get('user_id')

                check_previous_report = ReportUser.objects.filter(
                user_id=user_id, 
                reported_by=reported_by
                )

                if check_previous_report:
                    Response.status_code = 409
                    return Response({
                        "status": "error",
                        "message": "Already reported once",
                        "payload": ""
                        })
                
                if user_id == user_check["message"]["_id"]:
                    Response.status_code = 409
                    return Response({
                        "status": "error",
                        "message": "User cannot report self",
                        "payload": ""
                        })
                
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

            shop_recommendation = CreateShopRecommendation.objects.filter(recommended_for=user_check["message"]["_id"])
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
            print(user_check["message"]["_id"])
            data = request.data
            data['user_id'] = user_check["message"]["_id"]
            recommendation_serializer = CreateShopRecommendationSerializer(data=data)
            
            if recommendation_serializer.is_valid():

                uncreated_recommendation = CreateShopRecommendation.objects.filter(
                    user_id=user_check["message"]["_id"],
                    recommended_for=request.data.get('recommended_for'),
                    item=request.data.get('item')
                )

                if uncreated_recommendation:
                    Response.status_code = 409
                    return Response({
                        "status": "error",
                        "message": "Already recommended this item to the receiver!",
                        "payload" : ""
                    })
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
            print(self.recommendations.filter(recommended_for=user_check["message"]["_id"]))
            serializer = CreateShopRecommendationSerializer(
                self.recommendations.filter(recommended_for=user_check["message"]["_id"]), 
                many=True
                )

            print(user_check["message"]["_id"])
            Response.status_code = 200
            return Response({
                "status": "success",
                "message": "Fetched all recommendations",
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



class ReportUserCheckView(APIView):
    all_reports = ReportUser.objects.all()
    def get(self, request):
        first_user = request.query_params.get('first_user')
        second_user = request.query_params.get('second_user')

        if not(first_user and second_user):
            Response.status_code = 400
            return Response({
                "message": "Need user ids as first_user and second_user as get params"
            })
        first_reports_second = self.all_reports.filter(user_id=first_user, reported_by=second_user)
        second_reports_first = self.all_reports.filter(user_id=second_user, reported_by=first_user)

        if first_reports_second:
            user_1 = first_user
            user_2 = second_user
        elif second_reports_first:
            user_1 = second_user
            user_2 = first_user
        else:
            Response.status_code = 400
            return Response({
                "message": "None are blocked"
            })
        
        Response.status_code = 200
        return Response({
            "message": "{} blocked {}".format(user_1, user_2)
        })
