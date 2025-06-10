from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
import uuid 

class CustomUser(AbstractUser):
    username=None
    email=models.EmailField(_("email address"), unique=True)
    is_verified_by_admin = models.BooleanField(default=False)

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email   
    
    def is_admin(self):
        return self.is_staff
    
class Permissions(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not Permissions.objects.exists():
            self.code = 100
        else:
            self.code = Permissions.objects.last().code + 1
        super(Permissions, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

class Roles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permissions, related_name="roles")
    status=models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
            
class UserRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.username} - {self.role.id}"
    

