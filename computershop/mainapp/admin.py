from PIL import Image
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
from django.utils.safestring import mark_safe

from mainapp.models import *

class ValidateImageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        images = ['image_01', 'image_02', 'image_03', 'image_04']
        for image in images:
            self.fields[image].help_text = mark_safe(
                '<span style="color:red;">Минимальное разрешение для изображения {}x{}</span>'.format(
                    *Product.MIN_VALID_RESOLUTION
                )
            )

    def clean_image(self):
        images = ['image_01', 'image_02', 'image_03', 'image_04']
        for image in images:
            cleaned_images = self.cleaned_data[image]
            for cleaned_image in cleaned_images:
                img = Image.open(cleaned_image)
                min_height, min_width = Product.MIN_VALID_RESOLUTION
                max_height, max_width = Product.MAX_VALID_RESOLUTION
                if cleaned_image.size > Product.MAX_VALID_IMAGE_SIZE:
                    raise ValidationError('Размер изображения не должен превышать 3MB!')
                if img.height < min_height or img.width < min_width:
                    raise ValidationError('Изображение не соответствует требованиям!')
                if img.height > max_height or img.width > max_width:
                    raise ValidationError('Изображение не соответствует требованиям!')
                return image


class DesktopAdmin(admin.ModelAdmin):

    form = ValidateImageForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='desktops'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class NotebookAdmin(admin.ModelAdmin):

    form = ValidateImageForm

    def formfield_for_foreignkey(self, db_field, request, ** kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Desktop, DesktopAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)