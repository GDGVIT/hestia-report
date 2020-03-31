from django.db import models


class ReportUser(models.Model):
    user_id = models.CharField(max_length=250)
    reported_by = models.CharField(max_length=250)
    reason = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)




class CreateShopRecommendation(models.Model):
    user_id = models.CharField(max_length=250)
    recommended_for = models.CharField(max_length=250)
    name_of_shop = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    landmark = models.CharField(max_length=100)
    extra_instruction = models.CharField(max_length=250,blank=True)
    description_of_shop = models.CharField(max_length=250)
    read_by_user = models.BooleanField(default=0)

