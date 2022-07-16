from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Was activated?')

    def get_initial(self):
        return self.username.upper()[:2]

    class Meta(AbstractUser.Meta):
        pass


class SimpleUrl(models.Model):
    original_url = models.URLField(default='', db_index=True, verbose_name='URL to simplify')
    simple_url_id = models.CharField(default='', db_index=True, verbose_name='Simple URL id', max_length=10)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Creator')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created')

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'
        ordering = ['-created_at']
