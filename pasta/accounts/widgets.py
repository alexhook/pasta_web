from django.forms import ClearableFileInput

class PhotoWidget(ClearableFileInput):
    clear_checkbox_label = 'Удалить фото'
    template_name = 'accounts/widgets/photo_input.html'