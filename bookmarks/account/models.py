from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


# intermediary model from user to user itself.(i.e the relation model in a many to many relation).

# uer to user relation, so user_from and user_to (since relation is between two users.
class Contact(models.Model):
    user_from = models.ForeignKey(User,related_name='rel_from_set')  # fk for the user that creates relationship.
    user_to = models.ForeignKey(User, related_name='rel_to_set')  # user being followed.
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


"""  doesnot make any change in db to User model, just adds it to object
 by default symetrical = True in many to many, , i.e if i follow, you follow me, so symmetrical = False. (this false is only when you add
 many to many relation to model itself.
  add_to_class is not a recommended way to add fields to class,"""

# Add following field to User dynamically,

""" when you create intermediary model for a many to many relation, 
 manager methods such as add, save, remove are disabled, instead you need to create yourself"""

User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))