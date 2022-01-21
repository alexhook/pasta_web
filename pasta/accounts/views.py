from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, ChangeUserPersonalInfoModelForm
from .models import ActivationMessage
from django.http import Http404, HttpRequest, JsonResponse
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import render
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from recipes.views import RecipeListView
from django.contrib.auth.mixins import LoginRequiredMixin
from recipes.models import Recipe
from .forms import MyRecipesFilterForm
from utils.func import is_ajax


def index(request: HttpRequest):
    return render(
        request,
        'accounts/profile_index.html',
    )

def signup(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            domain = current_site.domain
            protocol = 'https' if request.is_secure() else 'http'
            subject = f'Активация Вашего аккаунта на {domain}.'
            message = render_to_string('accounts/account_active_email.html', {
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
    return render(request, 'accounts/signup.html', {'form': form})

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

@login_required
def change_user_personal_info(request: HttpRequest):
    user = request.user
    if request.method == 'POST':
        form = ChangeUserPersonalInfoModelForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены!')
    else:
        form = ChangeUserPersonalInfoModelForm(instance=user)
    return render(
        request,
        'accounts/change_personal_info.html',
        context={
            'form': form,
        }
    )

@login_required
def password_change(request: HttpRequest):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request,
        'accounts/password_change.html',
        context={
            'form': form,
        },
    )


class FavoritesListView(LoginRequiredMixin, RecipeListView):
    template_name = 'accounts/favorites_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class MyRecipesListView(LoginRequiredMixin, RecipeListView):
    template_name = 'accounts/myrecipes_list.html'

    def get_queryset(self):
        queryset = Recipe.objects.filter(author=self.request.user).select_related('author', 'menu', 'cuisine')
        if queryset.exists():
            if self.request.GET:
                form = MyRecipesFilterForm(self.request.GET)
                if form.is_valid():
                    is_published = form.cleaned_data.get('is_published')
                    menu = form.cleaned_data.get('menu')
                    cuisine = form.cleaned_data.get('cuisine')
                    if not is_published == '':
                        queryset = queryset.filter(is_published=is_published)
                    if menu:
                        queryset = queryset.filter(menu=menu)
                    if cuisine:
                        queryset = queryset.filter(cuisine=cuisine)
        return queryset
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        is_published = self.request.GET.get('is_published')
        menu = self.request.GET.get('menu', 0)
        cuisine = self.request.GET.get('cuisine', 0)
        context_data['form'] = MyRecipesFilterForm(
            initial={
                'is_published': is_published,
                'menu': menu,
                'cuisine': cuisine
            },
        )
        return context_data

@login_required
def favorites_update(request: HttpRequest, slug):
    if request.method == 'POST' and is_ajax(request):
        recipe = Recipe.objects.filter(slug=slug)
        if not recipe.exists():
            error = 'Рецепт не найден.'
            return JsonResponse({'errors': error}, status=400)
        recipe = recipe[0]
        if recipe.author == request.user:
            error = 'Невозможно добавить собственный рецепт в избранное.'
            return JsonResponse({'errors': error}, status=400)
        favorites = request.user.favorites
        if favorites.filter(slug=slug).exists():
            favorites.remove(recipe)
        else:
            favorites.add(recipe)
        return JsonResponse({}, status=200)
    else:
        raise Http404