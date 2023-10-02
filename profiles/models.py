from django.db import models
from django.utils.translation import gettext_lazy as _


# models
from recipes.models import Recipe

# Create your models here.


class UserAccountManager(models.Model):
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(_('User must have an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        if not email:
            raise ValueError(_("User must have an email address"))

        email_ = self.normalize_email(email)
        user = self.model(email=email_, **kwargs)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(models.Model):
    email = models.EmailField(
        max_length=100, unique=True, verbose_name=_("Email Address"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserAccountManager()

    def __str__(self) -> str:
        return self.email


class Profile(models.Model):
    pass
