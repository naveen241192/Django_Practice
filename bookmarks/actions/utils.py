import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

# short cut to create action in a similar way.

# allows us to add new actions to Activity Stream.

""" when ever this fn is called, saves the action into activity stream"""


def create_action(user, verb, target=None):
    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)

    """
    We need to restrict the duplicate actions in activity streams, like user repeatedly likes and unlikes and likes 
    and unlikes and then likes, 
    we don't have to show the activity of every time he likes that image.
    """
    if not similar_actions:
        # no existing actions found
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True  # if action is created.
    return False  # no action created.
