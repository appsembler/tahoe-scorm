import os

from exceptions import ScormException


def tahoe_scorm_storage(xblock):
    """
    Multi-tenant SCORM storage backend for overhangio/openedx-scorm-xblock .
    """
    from django.conf import settings
    from django.core.files.storage import get_storage_class
    from openedx.core.djangoapps.appsembler.api.sites import get_site_for_course
    from openedx.core.djangoapps.site_configuration.models import SiteConfiguration

    current_site = get_site_for_course(xblock.course_id)
    site_config = SiteConfiguration.objects.get(site=current_site)
    scorm_sub_folder = getattr(settings, "TAHOE_SCORM_XBLOCK_ROOT_DIR", False)
    site_scorm_folder = site_config.get_value('course_org_filter', False)
    if not scorm_sub_folder:
        raise ScormException(
            'TAHOE_SCORM_XBLOCK_ROOT_DIR is not defined in Django settings. Please fix it so tahoe_scorm_storage works.'
        )
    if not site_scorm_folder:
        raise ScormException(
            'course_org_filter is not defined in SiteConfiguration. Please fix it so tahoe_scorm_storage works.'
        )

    storage_class = get_storage_class(settings.DEFAULT_FILE_STORAGE)
    storage_location = os.path.join(scorm_sub_folder, "test-site") # replace with TAHOE_SCORM_XBLOCK_ROOT_DIR and course_org_filter
    if settings.SERVICE_VARIANT == "lms":
        s3_custom_domain = current_site.domain
    else:
        s3_custom_domain = settings.SITE_NAME

    return storage_class(
        location=storage_location,
        default_acl='public-read',
        custom_domain=s3_custom_domain
    )
