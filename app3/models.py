from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class blockk(models.Model):
    panchayatname = models.CharField(max_length=100)
    wards = models.CharField(max_length=100)
    def __str__(self) -> str:
        return f'{self.panchayatname}'


class usersignup(models.Model):
    panchayatchoices = (
        ('Puthenvelikkara','Puthenvelikkara'),
        ('Chengamanadu','Chengamanadu'),
        ('Nedumbassery','Nedumbassery'),
        ('Parakkadavu','Parakkadavu'),
        ('Kunnukara','Kunnukara'),
    )
    panchayat = models.CharField(max_length=100,default='Nedumbassery',choices=panchayatchoices)
    ward = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.CharField(null=True,max_length=50)
    image = models.ImageField(null=True,upload_to='profile',default='img/noprofile.jpg')
    proof = models.ImageField(null=True,upload_to='proof')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ap = (
        ('Pending','Pending'),
        ('Approved','Approved')
    )
    approval = models.CharField(max_length=1000,choices=ap,default='Pending')
    address=models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.name}-{self.status}-{self.ward}-{self.panchayat}'
    
class complaint(models.Model):
    usr = models.ForeignKey(usersignup,on_delete=models.CASCADE)
    subject = models.CharField(max_length=1000)
    details = models.CharField(max_length=1000)
    cmplstatus = (
        ('Pending','Pending'),
        ('Action Taken','Action Taken'),
        ('Solved','Solved')
    )
    complaintstatus = models.CharField(max_length=150,choices=cmplstatus,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    smailp=models.IntegerField(default=0)
    smailact=models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f'{self.usr}'
    
class complaintimages(models.Model):
    cmp = models.ForeignKey(complaint,on_delete=models.CASCADE)
    complaintimages = models.ImageField(null=True,upload_to='complaintimages')
    
    def __str__(self) -> str:
        return f'{self.usr}'
    
class complaintmessage(models.Model):
    cmp = models.ForeignKey(complaint,on_delete=models.CASCADE)
    message = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.cmp.usr.name}-{self.cmp.usr.ward}-{self.cmp.usr.panchayat}'
    
class PasswordReset(models.Model):
    user=models.ForeignKey(usersignup,on_delete=models.CASCADE)
    token=models.CharField(max_length=100,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)