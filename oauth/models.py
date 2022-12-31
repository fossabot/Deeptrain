from django.db import models
from user.models import User


class OAuthModel(models.Model):
    class Meta:
        db_table = "oauth"
        verbose_name = "OAuth"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    oauth_id = models.PositiveIntegerField(default=0)
    oauth_name = models.CharField(max_length=50)  # GitHub: 39

    oauth_app = models.CharField(max_length=12)
