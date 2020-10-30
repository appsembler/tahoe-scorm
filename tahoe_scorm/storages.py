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
    sub_folder = site_config.get_value('SCORM_DIR', False)
    if not sub_folder:
        raise ScormException(
            'SCORM_DIR is not defined in SiteConfiguration. Please fix it so tahoe_scorm_storage works.'
        )
    storage_location = os.path.join(settings.MEDIA_ROOT, sub_folder)
    storage_class = get_storage_class(settings.DEFAULT_FILE_STORAGE)
    return storage_class(
        location=storage_location,
        base_url='{media_url}/{sub_folder}'.format(
            media_url=settings.MEDIA_URL,
            sub_folder=sub_folder,
        )
    )
