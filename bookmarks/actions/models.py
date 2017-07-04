from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# model for tracking user actions.


class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True)
    verb = models.CharField(max_length=255)  # describes the action that user has performed.

    # a FK to ContentType model
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj')

    # a +ve integer field to store pk of related object.
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)

    # a generic FK to store the related object, based on combo 2 prev fields.
    # django does not create any field in db for GenericFK.

    """ we cannot have more than one foreign key from a single model associating it to more than one model. 
    The trick here is to use a model which has relations to all the models in the project. 
    If you can point your foreign key to that model which in turn can point to different models, 
    that would solve this issue. This can be done using content types table and generic foreignkey."""

    target = GenericForeignKey('target_ct', 'target_id')

    # Date and time when this action is created.

    # automatically sets the time to current time, when the object is first saved to db.
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)
