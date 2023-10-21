from django.conf import settings
from datetime import datetime
import os

from profiles.utils import get_random_code


def recipe_picture_dir_path(instance, filename):
    dt = str(datetime.today()).split()[0]
    recipe_path = f'recipes/user_{instance.user.id}/{dt}/{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, recipe_path)

    is_exist = os.path.exists(full_path)
    while is_exist:
        random = get_random_code()
        recipe_path = f'recipes/user_{instance.user.id}/{dt}/{random}{filename}'
        full_path = os.path.join(settings.MEDIA_ROOT, recipe_path)
        is_exist = os.path.exists(full_path)

    return recipe_path
