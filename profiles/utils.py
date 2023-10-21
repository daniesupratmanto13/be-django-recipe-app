from django.conf import settings
from uuid import uuid4
import os


def get_random_code():
    return str(uuid4())[:8].replace('-', '').lower()


def profile_avatar_dir_path(instance, filename):
    profile_avatar_name = f'profile_pics/user_{instance.user.id}/avatar_{filename}'
    full_path = os.path.join(settings.MEDIA_ROOT, profile_avatar_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return profile_avatar_name
