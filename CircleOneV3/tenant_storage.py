from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from tenant_schemas.storage import TenantStorageMixin


# class S3BotoStorageWithAwsProfile(TenantStorageMixin, S3Boto3Storage):
#
#     @property
#     def connection(self):
#         connection = getattr(self._connections, 'connection', None)
#         if connection is None:
#             # modified to use aws profile for credentials
#             session = boto3.session.Session(settings.AWS_PROFILE_NAME)
#             self._connections.connection = session.resource(
#                 's3',
#                 aws_access_key_id=self.access_key,
#                 aws_secret_access_key=self.secret_key,
#                 aws_session_token=self.security_token,
#                 region_name=self.region_name,
#                 use_ssl=self.use_ssl,
#                 endpoint_url=self.endpoint_url,
#                 config=self.config,
#                 verify=self.verify,
#             )
#         return self._connections.connection


class S3MediaStorage(TenantStorageMixin, S3Boto3Storage):
    location = 'media'
    bucket_name = settings.STORAGE_S3_BUCKET_NAME
    custom_domain = f'{bucket_name}.s3.amazonaws.com'


class S3StaticStorage(TenantStorageMixin, S3Boto3Storage):
    location = 'static'
    bucket_name = settings.STORAGE_S3_BUCKET_NAME
    custom_domain = f'{bucket_name}.s3.amazonaws.com'
