import os

from .exceptions import ScormException


def tahoe_scorm_storage(xblock):
    """
    Multi-tenant SCORM storage backend for overhangio/openedx-scorm-xblock. The
    following function returns a custom Django storages backend in which the
    location is determined based on a combination of a settings and,
    by default, the course_org_filter site settings.
    The Tahoe default file storage backend is S3Boto3Storage, so is the one this
    function will return.
    """
    from django.conf import settings
    from django.core.files.storage import get_storage_class
    from openedx.core.djangoapps.appsembler.api.sites import get_site_for_course

    # in Tahoe we use 'storages.backends.s3boto3.S3Boto3Storage'
    storage_class = get_storage_class(settings.DEFAULT_FILE_STORAGE)

    # the root dir inside the S3 bucket, configurable in global settings
    scorm_sub_folder = getattr(settings, "TAHOE_SCORM_XBLOCK_ROOT_DIR", None)

    if not scorm_sub_folder:
        raise ScormException(
            'TAHOE_SCORM_XBLOCK_ROOT_DIR is not defined in Django settings. '
            'Please fix it so tahoe_scorm_storage works.'
        )

    # in order to allow CORS restrictions in the browser we need to use a custom
    # domain for the storage. Then in Nginx we have a proxy for the location,
    # but again, in order to allow CORS issues, if we browsing the content in
    # the LMS, the file must come from the LMS, and in Studio from Studio.
    # We cannot simply rely on settings for LMS and Studio URLs, because we need
    # to keep custom domains inside the ecuation.
    s3_custom_domain = settings.SITE_NAME

    if getattr(settings, "TAHOE_SCORM_USE_COURSE_ORG_FOR_DOMAIN", True):
        # retrieve the site based on the course site id, it will work in the LMS and Studio as well.
        current_site = get_site_for_course(xblock.course_id)

        # we use course organization id filter as customer SCORM folder
        site_scorm_folder = str(xblock.course_id.org)
        storage_location = os.path.join(scorm_sub_folder, site_scorm_folder)

        if settings.SERVICE_VARIANT == "lms":
            s3_custom_domain = current_site.domain
    else:
        storage_location = scorm_sub_folder

    return storage_class(
        location=storage_location,
        default_acl='public-read',
        custom_domain=s3_custom_domain
    )
