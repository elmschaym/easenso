from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

class User(AbstractUser):
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    USER_TYPE = [
        ('B', 'Basic'),
        ('P', 'Premium')
    ]
    
    security_questions = (
        ('first_kissed', 'What is the first name of the person you first kissed?'),
        ('failing_grade', 'What is the last name of the teacher who gave you your first failing grade?'),
        ('wedding_reception', 'What is the name of the place your wedding reception was held?'),
        ('primary_school', 'What was the name of your elementary / primary school?'),
        ('sibling_live', 'In what city or town does your nearest sibling live?'),
        ('time_born','What time of the day were you born? (hh:mm)'),
        ('pets_name','What is your pet'+"'"+'s name?'),
        ('father_born', 'In what year was your father born?'),
        ('favorite', 'What is your favorite _____?')
    )

    middle_name          = models.CharField(max_length = 30)
    gender               = models.CharField(max_length = 1, choices = GENDER)
    date_of_birth        = models.DateField(null = True)
    address              = models.CharField(max_length = 200)
    contact_number       = models.CharField(max_length = 200)
    profile_picture      = models.FileField(upload_to ='user/profile_pictures', null = True, blank = True)
    profile_background   = models.FileField(upload_to ='user/profile_background', null = True, blank = True)
    cover_photo          = models.FileField(upload_to ='user/cover_photo', null = True, blank = True)
    captcha              = models.CharField(max_length = 500)
    security_question    = models.CharField(max_length = 30, choices = security_questions)
    security_answer      = models.CharField(max_length = 100)
    user_type_expiration = models.DateTimeField(null = True)
    user_type            = models.CharField(max_length = 1, choices = USER_TYPE)
    is_confirmed         = models.BooleanField(default = False)

class Follow(models.Model):
    following     = models.ForeignKey(User, related_name = 'following')
    follower      = models.ForeignKey(User, related_name = 'follower')
    date_followed = models.DateTimeField(auto_now_add = True)

class User_Post(models.Model):
    message          = models.CharField(max_length = 500)
    sender           = models.ForeignKey(User, related_name = 'sender')
    recipient        = models.ForeignKey(User, related_name = 'recipient')
    sender_delete    = models.BooleanField(default = False)
    recipient_delete = models.BooleanField(default = False)
    sender_hide      = models.BooleanField(default = False)
    recipient_hide   = models.BooleanField(default = False)
    date_sent        = models.DateTimeField(auto_now_add = True)