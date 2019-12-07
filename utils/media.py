"""
Signal handlers for file fields for renaming, updating, and auto-deletion of related files.
------------------------------------------------------------------------------------------

Depends on FileStorage and uses save, exists, delete

Sample code:
for model in models_with_file_upload:
    pre_save.connect(delete_old_model_files, sender=model)
    post_save.connect(rename_model_files_from_field_verbose_name, sender=model)
    post_delete.connect(delete_model_files, sender=model)
"""
import os
import pathlib

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.text import slugify

# package sorl-thumbnail contains a compatible Imagefield which is dynamically supported.
try:
    from sorl import thumbnail
except ImportError:
    thumbnail = None

# REQUIRES settings.MEDIA_ROOT to
# be the full valid path of
# uploads root.
#################################

if not os.path.isabs(settings.MEDIA_ROOT):
    raise ValueError('Media root should contain absolute path.')

django_file_fields = [models.FileField, models.ImageField]
FILE_FIELD_TYPES = tuple(django_file_fields + [thumbnail.ImageField] if thumbnail else django_file_fields)

def database_file_upload_path(instance, filename=''):
    """
    Return upload file paths in the format:
    parent_dir/(slugified)model verbose name plural/pk/filename
    """
    PARENT_DIR_FOR_DB_UPLOADS = settings.DB_UPLOAD_MEDIA_PATH

    instance_type = type(instance)
    return os.path.join(PARENT_DIR_FOR_DB_UPLOADS, str(slugify(instance_type._meta.verbose_name_plural)),
                        str(instance.pk),
                        filename)


def rename_model_files_from_field_verbose_name(sender, instance, *args, **kwargs):
    """
    post_save Signal receiver for models to rename files
    into their corresponding field's (slugified)verbose_names.
    Maintains FileField and ImageField.

    Some storages (Boto3 for instance) do not support path or listdir. Those attributes are not used at all.
    """
    # Field types having file uploads
    concerned_field_types = FILE_FIELD_TYPES

    # all file fields of the model:
    field_name_list = tuple(f.name for f in sender._meta.get_fields() if type(f) in concerned_field_types)
    field_instance_list = tuple(getattr(instance, field_name) for field_name in field_name_list)

    # Remove empty fields.
    # (If the file field is initially empty, field.name would also be empty.
    # Which would result in pointing to the uploads dir instead of the( non-existent) file.)
    field_instance_list = tuple(i for i in field_instance_list if i.name)
    instance_changed = False

    # rename all files to unified file names
    for field_instance in field_instance_list:

        try:
            upload_root = field_instance.field.upload_to(instance, '')
        except TypeError:
            # field.upload_to is not callable
            upload_root = field_instance.field.upload_to

        file_extension = os.path.splitext(field_instance.name)[1]

        standard_filename = os.path.join(upload_root, str(slugify(field_instance.field.verbose_name))) + file_extension

        if os.path.normpath(field_instance.name) != os.path.normpath(standard_filename):
            # incorrect filename.

            if field_instance.storage.exists(field_instance.name):
                # os.rename will raise err if destination exists on nonUnix
                # might wanna use the storage class for the same
                if field_instance.storage.exists(standard_filename):
                    field_instance.storage.delete(standard_filename)
                field_instance.storage.save(standard_filename, field_instance)
                field_instance.storage.delete(field_instance.name)

            field_instance.name = standard_filename
            instance_changed = True

    if instance_changed:
        instance.save()


def delete_model_files(sender, instance, *args, **kwargs):
    """
    post_delete Signal receiver for models to delete associated files
    and their empty parent directories.
    Maintains FileField and ImageField.

    Some storages (Boto3 for instance) do not support path or listdir. Those attributes are not used at all.
    """
    # Field types having file uploads
    concerned_field_types = FILE_FIELD_TYPES

    # all file fields of the model:
    field_name_list = tuple(f.name for f in sender._meta.get_fields() if type(f) in concerned_field_types)
    field_instance_list = tuple(getattr(instance, field_name) for field_name in field_name_list)

    for field_instance in field_instance_list:
        if field_instance.name:
            # TODO If there is a upload root dir left behind empty, delete it.
            # try:
            #     upload_root = field_instance.field.upload_to(instance, '')
            # except TypeError:
            #     # field.upload_to is not callable
            #     upload_root = field_instance.field.upload_to

            # full_upload_root_path = os.path.join(settings.MEDIA_ROOT, upload_root)
            if field_instance.storage.exists(field_instance.name):
                field_instance.storage.delete(field_instance.name)




def delete_old_model_files(sender, instance, *args, **kwargs):
    """
    pre_save Signal receiver for models to delete obsolete files
    if their file fields are being updated.

    Maintains FileField and ImageField.

    Some storages (Boto3 for instance) do not support path or listdir. Those attributes are not used at all.
    """
    # Field types having file uploads
    concerned_field_types = FILE_FIELD_TYPES

    # all file fields of the model:
    field_name_list = tuple(f.name for f in sender._meta.get_fields() if type(f) in concerned_field_types)

    # Since the signal is pre_save the db still has original old entry.
    # If a new entry is being added, will raise DoesNotExist.
    try:
        old_instance = sender.objects.get(id=instance.id)
    except sender.DoesNotExist:
        # Nothing to do since the object is yet to be created.
        return

    new_field_instance_list = tuple(getattr(instance, field_name) for field_name in field_name_list)
    old_field_instance_list = tuple(getattr(old_instance, field_name) for field_name in field_name_list)

    for new_field_instance, old_field_instance in zip(new_field_instance_list, old_field_instance_list):

        # skip if field was previously empty
        if (old_field_instance.name
                and old_field_instance.storage.exists(old_field_instance.name)
                and old_field_instance.name != new_field_instance.name):
            # a new file has been uploaded for the same field.

            # Remove old file if present.
            # Could already be removed.
            if old_field_instance.storage.exists(old_field_instance.name):
                old_field_instance.storage.delete(old_field_instance.name)
