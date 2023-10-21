from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# utils
from .utils import recipe_picture_dir_path

# third party
import uuid


class RecipeCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Category Name"))
    slug = models.SlugField(
        max_length=120, null=False, blank=True, unique=True, editable=False, db_index=True
    )

    class Meta:
        verbose_name = _('Recipe Category')
        verbose_name_plural = _('Recipe Categories')

    def __str__(self) -> str:
        return f'{self.id}-{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def get_default_recipe_category():

    return RecipeCategory.objects.get_or_create(name='Others')[0]


class Recipe(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="recipes", on_delete=models.CASCADE)
    category = models.ManyToManyField(
        RecipeCategory, blank=True)
    picture = models.ImageField(upload_to=recipe_picture_dir_path)
    title = models.CharField(max_length=200)
    description = models.CharField(
        max_length=200, verbose_name=_('description'))
    cook_time = models.TimeField()
    ingredients = models.TextField()
    procedure = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.id}-{self.author.username}-{self.title}'

    @property
    def get_total_like(self):
        return RecipeLike.objects.filter(recipe=self, value='Like').count()

    @property
    def get_total_unlike(self):
        return RecipeLike.objects.filter(recipe=self, value='Unlike').count()

    @property
    def get_total_bookmark(self):
        return self.bookmarked.count()


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class RecipeLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.CharField(
        choices=LIKE_CHOICES, default='Like', max_length=8)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} {self.value} {self.recipe}'
