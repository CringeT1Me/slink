from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    custom_domain = False


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = False

class PublicAvatarStorage(S3Boto3Storage):
    location = 'media/avatars'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = False

class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False