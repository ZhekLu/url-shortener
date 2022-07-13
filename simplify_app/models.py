from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Was activated?')

    def get_initial(self):
        return self.username.upper()[:2]

    class Meta(AbstractUser.Meta):
        pass


class SimpleUrl(models.Model):
    original_url = models.URLField(default='https://example.com', db_index=True, verbose_name='URL to simplify')
    simple_url = models.URLField(default='https://simple_url', verbose_name='Simple URL')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Creator')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published')

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'
        ordering = ['-created_at']
