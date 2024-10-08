from django.contrib.auth.tokens import default_token_generator
from djoser.email import ActivationEmail, BaseDjoserEmail, ConfirmationEmail, PasswordResetEmail, \
    PasswordChangedConfirmationEmail, UsernameChangedConfirmationEmail
from djoser import utils
from djoser.conf import settings

class EmailChange(BaseDjoserEmail):
    template_name = "emails/email_change.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context['user']
        new_email = self.context.get('new_email')
        token = self.context.get('token')
        uid = utils.encode_uid(user.pk)

        # Формируем ссылку
        context["url"] = settings.EMAIL.change_email_confirmation_url.format(uid=uid, token=token, new_email=new_email)
        return context

class CustomActivationEmail(ActivationEmail):
    template_name = "emails/activation.html"
    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["first_name"] = user.first_name
        context["last_name"] = user.last_name
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        print(context)
        return context

class CustomConfirmationEmail(ConfirmationEmail):
    template_name = "emails/confirmation.html"

class CustomPasswordResetEmail(PasswordResetEmail):
    template_name = "emails/change_email.html"

class CustomPasswordChangedConfirmationEmail(PasswordChangedConfirmationEmail):
    template_name = "emails/change_email.html"

class CustomUsernameChangedConfirmationEmail(UsernameChangedConfirmationEmail):
    template_name = "emails/change_email.html"
