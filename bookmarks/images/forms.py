from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        """
        users are not going to enter image url directly in form., rather they are going to 
        use javascript tool to choose an image from external site.
        """
        widgets = {
            'url': forms.HiddenInput,
        }

    """
    this fn is used to check the url given has an image or not.
    """
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']

        # split the url to get file extention.
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    """
    Instead of model saving the image into db, we would rather over-ride
    save method of ModelForm class. to save the image into db.
    
    ModelForm's save method allows to save the current instance of the model into db and return the object.
    """
    def save(self, force_insert=False, force_update=False, commit=True):

        # creating an instance but not saving into the database.
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),
                                    image_url.rsplit('.', 1)[1].lower())

        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)

        """" tells if the image has to be persisted into the database.
         if false it will return an object of ModelForm instance,
         but will not save image into db."""
        if commit:
            image.save()
        return image
