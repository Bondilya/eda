from django.template.loader import render_to_string
from django.core.signing import Signer
from eda.settings import ALLOWED_HOSTS

signer = Signer()

def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)


def create_user_id(username):
    id =[]
    numbers = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    for vowels in username:
        if vowels in numbers:
            id.append(vowels)
    index = int(''.join(id))
    return index + 1
