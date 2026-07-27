import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import SET_NULL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    confirmation_token = models.UUIDField(default=uuid.uuid4)

def validate_image_url(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

    # get rid of any query strings after the file extension
    path = value.split('?')[0].lower()

    if not any(path.endswith(extension) for extension in valid_extensions):
        raise ValidationError("The URL must point to an image file.")

class Author(models.Model):
    name = models.CharField(max_length=150)
    picture = models.CharField(blank=True, validators=[validate_image_url])
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Quote(models.Model):

    class Subject(models.TextChoices):
        RELATIONSHIPS = 'Relationships', 'relationships'
        SUCCESS = 'Success', 'success'
        LUST = 'Lust', 'lust'
        GOD = 'God', 'god'
        PROGRESS = 'Progress', 'progress'
        COMFORT = 'Comfort', 'comfort'
        MONEY = 'Money', 'money'
        DEATH = 'Death', 'death'
        TRUTH = 'Truth', 'truth'
        JOY = 'Joy', 'joy'
        SOCIETY = 'Society', 'society'
        POLITICS = 'Politics', 'politics'

    text = models.TextField()
    derivation = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(
        Author,
        on_delete=SET_NULL,
        null=True,
        related_name='quotes'
    )
    subject = models.CharField(max_length=50, choices=Subject.choices)
    added_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)

    # for security, a User's first post has to be approved
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text[:20]} - {self.author.name}"



