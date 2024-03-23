from django.db import models
from django.db import models

# Create your models here.
class UserLogin(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=50)
    utype = models.CharField(max_length=50)


class user(models.Model):
    user_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    ph_no = models.CharField(max_length=200)


class turf(models.Model):
    truf_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    price = models.CharField(max_length=200)


class booking(models.Model):
    booking_id = models.CharField(max_length=20)
    truf_id = models.CharField(max_length=50)
    booking_date = models.CharField(max_length=200)
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

class payment(models.Model):
    payment_id = models.CharField(max_length=20)
    booking_id = models.CharField(max_length=50)
    payment_date = models.CharField(max_length=200)
    amount = models.CharField(max_length=200)
    status=models.CharField(max_length=20)


class Review(models.Model):
    rid = models.CharField(max_length=20)
    user_id = models.CharField(max_length=50)
    turf_id = models.CharField(max_length=200)
    rating = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    review_date = models.CharField(max_length=200)


