from .forms import UserCreationForm
from .models import ActivationMessage
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def index(request: HttpRequest):
    pass

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            domain = current_site.domain
            protocol = 'https' if request.is_secure() else 'http'
            subject = f'Активация Вашего аккаунта на {domain}.'
            message = render_to_string('c_auth/account_active_email.html', {
                'user': user,
                'protocol': protocol,
                'domain': domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return ActivationMessage('Пожалуйста, подтвердите Ваш email по ссылке, отправленной на указанный Вами адрес электронной почты.')
    else:
        form = UserCreationForm()
    return render(request, 'c_auth/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return ActivationMessage('Активация аккаунта завершена. Добро пожаловать!')
    else:
        return ActivationMessage('Ссылка недействительна. Попробуйте снова.')