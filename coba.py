from decouple import config

SECRET_KEY = config('SECRET')

print(SECRET_KEY)
