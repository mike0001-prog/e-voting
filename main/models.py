from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
# Create your models here.

class Election(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    scheduled_date  = models.DateTimeField()
    end_date  = models.DateTimeField()
    STATUS = (
    ("REGISTRATION", "Registration"),
    ("VOTING", "Voting"),
    ("CLOSED", "Closed"),
)
    status = models.CharField( max_length=20,choices=STATUS,default="REGISTRATION")
  
    def __str__(self):
        return f"created at {datetime.date(self.created_at)} scheduled for {datetime.date(self.scheduled_date)} ending on {datetime.date(self.end_date)} "


class Position(models.Model):
    position = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.position}"
    

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE,null=True,default=None)
    name_of_candidate = models.CharField( max_length=150,)
    position = models.ForeignKey(Position,  on_delete=models.SET_NULL,null=True)
    candidate_photo = models.ImageField( upload_to="candidate_photos/", null=True, default=None )
    is_approved = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.name_of_candidate}"

class Vote(models.Model):
    election = models.ForeignKey(Election,  on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=("voter"), on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate,  on_delete=models.CASCADE,default=1)
    position = models.ForeignKey(Position, on_delete=models.CASCADE,default=1)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["election", "user", "position"],
                name="one_vote_per_position"
            )
        ]
    def __str__(self):
        return f"#{self.election} election by {self.user}"

class RegisteredUser(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name=("Registered User"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} registered for election #{self.election}"
class Student(models.Model):
    matric_number = models.CharField(max_length=50,unique=True)
    full_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.matric_number}"
    



# status = models.CharField(max_length=20, choices=STATUS)
