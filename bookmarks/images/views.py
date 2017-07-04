from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from common.decorators import ajax_required
from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action  # To create action to display activity stream (user likes or bookmarked image)


@login_required
def image_create(request):
    """
    View for creating an Image using the JavaScript Bookmarklet.
    """
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            new_item.save()

            """
            creates an action saying this user has bookmarked this image to display in activity stream.
            """
            create_action(request.user, 'bookmarked image', new_item)

            messages.success(request, 'Image added successfully')
            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images',
                                                        'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images',
                                                        'image': image})


@ajax_required  # custom decorator, to allow only ajax requests.
@login_required  # requires login
@require_POST  # (requires the request to be POST, does not allow GET requests.)
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')  # action can be like or unlike.
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)  # add objects to related object set, this add avoids duplication

                """creates an action that user liked this image to show in activity stream,"""

                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)  # removes the object from related object set.
            return JsonResponse({'status': 'ok'})  # returning JsonResponse, converting given object into json response
        except:
            pass
    return JsonResponse({'status': 'ko'})


"""
Allows the users to view all bookmarked images.

This fn allows the users to view images in a standard way
and by JAX way with pagination of infinite scrolling.

i.e when user scrolls to bottom of page, we load next page of items via AJAX.
"""


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                   {'section': 'images', 'images': images})