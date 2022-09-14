from django.core.mail import send_mail
from .models import Contact

def send_confirmation_email(email,activation_code):
    code = activation_code
    full_link = f'http://localhost:8000/api/v1/account/activate/{code}/'
    to_email = email
    send_mail(
        'Здравствуйте активирует ваш аккаунт !!!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке {full_link}',
        'babaevermek72@gmail.com',
        [to_email,],
        fail_silently=False

        )

def send_reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail('Восстановление',
    f'Код востановления: {code}',
    'from@example.com',
    [to_email,],
    fail_silently=False
)

def send_notification(email,id):
    full_link = f'http://localhost:8000/api/v1/music/{id}/'
    for users in Contact.objects.all():
        send_mail(
            'Новое уведомление',
            f'Новый трек от {email} по сслыке: {full_link}',
            'babaevermek72@gmail.com',
            [users.email],
            fail_silently=False,

        )
