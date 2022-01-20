from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.template.response import SimpleTemplateResponse
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        """
        Creates and saves a User with the given email and password.
        """

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('адрес электронной почты', max_length=255, unique=True)
    first_name = models.CharField('имя', max_length=150, null=True, blank=False)
    last_name = models.CharField('фамилия', max_length=150, null=True, blank=False)
    photo = models.ImageField('фото', upload_to='users/', null=True, blank=False)
    favorites = models.ManyToManyField('recipes.Recipe')
    date_joined = models.DateTimeField('дата регистрации', default=timezone.now)

    is_active = models.BooleanField('активный', default=False, help_text='Только активные пользователи могут проходить авторизацию.')
    is_admin = models.BooleanField('администратор', default=False, help_text='Дает право доступа к панели администратора.')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class ActivationMessage(SimpleTemplateResponse):
    def __init__(self, msg: str, **kwargs):
        template = 'accounts/activation_message.html'
        super().__init__(template, **kwargs)
        self.context_data = {
            'msg': msg, 
        }