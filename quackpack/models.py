from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    STUDENT = '1'
    WARDEN = '2'
     
    EMAIL_TO_USER_TYPE_MAP = {
        'student': STUDENT,
        'warden': WARDEN
    }
    
    user_type_data = ((STUDENT, "student"), (WARDEN, "warden"))
    user_type = models.CharField(choices=user_type_data, max_length=10)

    groups = models.ManyToManyField(
    'auth.Group',
    related_name='customuser_groups',
    blank=True
)
    user_permissions = models.ManyToManyField(
    'auth.Permission',
    related_name='customuser_permissions',
    blank=True
)

    class Meta:
        db_table = "customuser"

class students(models.Model):
    #regno = models.AutoField(primary_key=True)
    regno = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    email = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1)
    block = models.CharField(max_length=1)
    mob = models.IntegerField()

    objects = models.Manager()
    class Meta:
        db_table = "students"

'''class wardens(models.Model):
    regno = models.AutoField(students,on_delete=models.CASCADE)
    email = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    block = models.CharField(max_length=1)
    mob = models.IntegerField(students,on_delete=models.CASCADE)

    objects = models.Manager()
    class Meta:
        db_table = "wardens"'''

class wardens(models.Model):
    #regno = models.ForeignKey(students, on_delete=models.CASCADE, related_name='warden_regno')  # ForeignKey from Students table
    #mob = models.ForeignKey(students, on_delete=models.CASCADE, related_name='warden_mob')  # Another ForeignKey from Students table
    email = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ForeignKey to CustomUser
    hostel = models.CharField(max_length=10, default='Ladies')
    block = models.CharField(max_length=1)

    objects = models.Manager()
    
    class Meta:
        db_table = "wardens"

class req(models.Model):
    requester = models.ForeignKey(CustomUser, related_name="requests", on_delete=models.CASCADE)
    regno = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    otp = models.CharField(max_length=6, blank=True)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="Pending")  # Status can be "Pending", "Accepted", "Completed"
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_by = models.ForeignKey(CustomUser, related_name="deliveries", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Request by {self.requester.email} on {self.date}"
