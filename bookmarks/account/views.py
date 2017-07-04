from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm , UserEditForm, ProfileEditForm
from .models import Profile, Contact
from django.contrib.auth.models import User
from common.decorators import ajax_required
from django.views.decorators.http import require_POST

# To create action to display activity stream(user1 follows user2, or user has created a new account)
from actions.utils import create_action

from actions.models import Action


# Create your views here.

"""
#this view is used for two purposes 1. on loading of fresh form. 2. on submission of form
"""


def user_login(request):
    # 1. on submission of form
    if request.method == 'POST':
        # instantiate LoginForm with submitted data to display to the template
        form = LoginForm(request.POST)
        # if the form is valid or not
        if form.is_valid():
            cd = form.cleaned_data               #gets the cleaned dictionary containing fields of form
            user = authenticate(username=cd['username'], password=cd['password'])   # checks in database auth table of django framework.
            # & returns the user object if user has been authenticated successfully or None otherwise..

            if user is not None:
                if user.is_active:                 #an active user or disabled account user.
                    login(request, user)           #setting the user in session by calling login method.
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

"""decorator checks if the current user is authenticated, if the user is authenticated, it executes the decorated view,
                # else redirects to login url, with get parameter next in base.html
                # (so after login, it redirects to the url user is trying to access with next parameter"""


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password']) #encrypts the password & saves it.
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)

            """creates an action that user has created a new account. to show in activity stream,"""
            create_action(new_user, 'has created an account')
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required  # bcoz users have to be authenticated, to edit their profile.
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # django comes with inbuilt messages framework, to display any success, error, warning, info or debug msgs
            # and these messages will be included in request parameter, so we can display them in templates.

            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


@login_required
def dashboard(request):
    # return render(request, 'account/dashboard.html', {'section': 'dashboard'})

    # to display actions performed by users which are followed.

    actions = Action.objects.all().exclude(user=request.user)  # to exclude the current user.
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:

        """ If user is following others, retrieve only their actions, else if he is not following anyone retrieve the latest
        actions performed by other users, and limiting the actions to first 10 actions.
        """

        """
        TODO:  check 3.4 (05:00) for below line.
        """

        # optimized Query. Ouery Set Optimization.
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related(
            'target')
    actions = actions[:10]  # no need to order by since, we have ordered in meta of Actions model

    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'actions': actions})


"""
Lists all the active users.
"""


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section': 'people',
                                                      'users': users})

"""
TO get the active user with the given user name. returns 404 response if no user with given userid is found.
"""


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people',
                                                        'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)

                """creates an action that user is following this user to show in activity stream,"""
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})