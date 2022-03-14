from django_select2 import forms as s2forms
from accounts.widgets import PhotoWidget

class ImageWidget(PhotoWidget):
    clear_checkbox_label = 'Удалить'