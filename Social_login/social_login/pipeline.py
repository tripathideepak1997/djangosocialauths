from .models import User

DEFAULT_PROFILE_PHOTO_URL = 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fwww.edgehill.ac.uk%2'\
                            'Fhealth%2Ffiles%2F2017%2F12%2Fblank-profile.png&imgrefurl=https%3A%2F%2'\
                            'Fwww.edgehill.ac.uk%2Fhealth%2Fresearch%2Fhealth-and-wellbeing%2Fblank-'\
                            'profile%2F&docid=0pt3XWk8Eh3f5M&tbnid=AEEDePQQ2XIvWM%3A&vet=10ahUKEwiWjdv'\
                            '10JXjAhVeinAKHWdzBJQQMwhoKBMwEw..i&w=500&h=500&bih=575&biw=1366&q=blank%'\
                            '20profile%20picture&ved=0ahUKEwiWjdv10JXjAhVeinAKHWdzBJQQMwhoKBMwEw&iact='\
                            'mrc&uact=8'


def save_profile(backend, user, response, *args, **kwargs):
    if backend.__class__.__name__ == 'GoogleOAuth2' and kwargs['is_new']:
        user.url = response.get('picture', DEFAULT_PROFILE_PHOTO_URL)
        user.cache()
    if backend.__class__.__name__ == "TwitterOAuth" and kwargs['is_new']:
        user.url = response.get("profile_image_url", DEFAULT_PROFILE_PHOTO_URL)
        user.cache()
    if backend.__class__.__name__ == "FacebookOAuth2" and kwargs['is_new']:
        if response.get('id', None):
            user.url = f"http://graph.facebook.com/{response.get('id')}/picture?type=large"
            user.cache()

