from rest_framework import serializers
from .models import (
    ReportUser,
    CreateShopRecommendation
)




class ReportUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportUser
        fields = "__all__"
        
    
class CreateShopRecommendationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreateShopRecommendation
        fields = "__all__"
        extra_kwargs = {
            'user_id' : {
                'write_only': True
            }
        }
