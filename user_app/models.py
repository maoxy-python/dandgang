from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='邮箱')
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False, verbose_name='用户是否确认')

    class Meta:
        ordering = ['c_time']


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)
