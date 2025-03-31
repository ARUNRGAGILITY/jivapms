# your_app/context_processors.py

from django.conf import settings

def get_site_info(request):
    return {
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_NAME': settings.SITE_NAME,
        'CODING_AI': settings.CODING_AI,
        'SITE_CAPTION': settings.SITE_CAPTION,
        'SITE_DESC': settings.SITE_DESC,
        'CONTACT_EMAIL': settings.CONTACT_EMAIL,
        'BUILD_VERSION': settings.BUILD_VERSION,
        'BUILD_DESCRIPTION': settings.BUILD_DESCRIPTION,
        'COPYRIGHT_INFO': settings.COPYRIGHT_INFO,
    }
