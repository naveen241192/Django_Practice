from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse


# model used to store images bookmarks from diff sites.
class Image(models.Model):

    # user that bookmarked this image. FK, bcoz one user, many images.
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)

    # original URL of image.
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)

    # index will be created for this field,
    # time will be automatically added to db.
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    # stores the users that like an image. (many users can like many images)
    # so when you want to retrieve this field from USER_MODEL perspective
    # AUTH_USER_MODEL.images_liked (reason for related_name).
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)

    total_likes = models.PositiveIntegerField(db_index=True, default=0)  # to get no of likes in image.

    def __str__(self):
        return self.title

    # overriding the save method to automatically, generate the slug field
    # based on the title field.
    # slugify automatically generates the slug, for the given title, if no slug is provided.
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    """" common pattern to provide canonical url for the objects is to define
         this method in Model"""
    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])