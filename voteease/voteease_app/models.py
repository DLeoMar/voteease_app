from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class CustomUser(AbstractUser):
    STUDENT = 'student'
    ADMIN = 'admin'
    USER_TYPE_CHOICES = [
        (STUDENT, 'Student'),
        (ADMIN, 'Admin'),
    ]
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=STUDENT,
    )

    def __str__(self):
        return self.username

class Position(models.Model):
    position_name = models.CharField(max_length=255)
    vote_count = models.IntegerField()

    def __str__(self):
        return self.position_name

class Candidate(models.Model):
    STRAND = [('STEM', 'STEM'),
                ('HUMSS', 'HUMSS'),
                ('TVL', 'TVL'),
                ('ABM', 'ABM'),]

    SEX = [('Male', 'Male'),
              ('Female', 'Female'),]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=100, choices=SEX, null=True)
    strand = models.CharField(max_length=100, choices=STRAND, null=True)
    ps_image = models.ImageField(null=True, blank=True, upload_to='ps_images/')
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    vote_count = models.IntegerField(default=0)

# Education Model
class Education(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='educations')
    institution_name = models.CharField(max_length=255)
    start_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(9999)])
    end_year = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1900), MaxValueValidator(9999)])
    description = models.TextField(blank=True, null=True)  # Optional details like degree or program

    def __str__(self):
        return f"{self.institution_name} ({self.start_year} - {self.end_year if self.end_year else 'Present'})"

# Leadership Experience Model
class LeadershipExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='leadership_experiences')
    position = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    start_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(9999)])
    end_year = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1900), MaxValueValidator(9999)])
    description = models.TextField()

    def __str__(self):
        return f"{self.position} at {self.organization} ({self.start_year} - {self.end_year if self.end_year else 'Present'})"

# Award Model
class Award(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='awards')
    award_name = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1900), MaxValueValidator(9999)]) # Year the award was received
    description = models.TextField()

    def __str__(self):
        return f"{self.award_name} ({self.year})"

class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'position']