from django.core.urlresolvers import reverse
from django.db import models


class Bookmark(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField('url', unique=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('bookmark:BookmarkDV')
