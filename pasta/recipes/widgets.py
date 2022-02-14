from django_select2 import forms as s2forms
from accounts.widgets import PhotoWidget

class RecipeIngredientWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]

class ImageWidget(PhotoWidget):
    clear_checkbox_label = 'Удалить'