from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username=None, first_name=None, last_name=None,
                     email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        if extra_fields.get('is_superuser'):
            user = self.model(
                username=username,
                **extra_fields
            )

        else:
            email = self.normalize_email(email)

            user = self.model(
                username=username,
                first_name=first_name.title(),
                last_name=last_name.title(),
                email=email,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, first_name, last_name, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username=username, first_name=first_name, last_name=last_name,
                                 email=email, password=password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            username=username,
            password=password,
            **extra_fields
        )