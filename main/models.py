from django.db import models


class ReportUser(models.Model):
    user_id = models.CharField(max_length=255)
    reported_by = models.CharField(max_length=255)
    reason = models.CharField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)




class CreateShopRecommendation(models.Model):
    user_id = models.CharField(max_length=255)
    recommended_for = models.CharField(max_length=255)
    name_of_shop = models.CharField(max_length=100)
    item = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True)
    landmark = models.CharField(max_length=20)
    extra_instruction = models.TextField(blank=True)
    description_of_shop = models.TextField()
    read_by_user = models.BooleanField(default=0)

