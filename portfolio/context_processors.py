from . import models


def site_context(request):
    """
    Makes site-wide settings and the nav available in every template
    without having to pass them in explicitly from each view.
    """
    return {
        "site_settings": models.SiteSettings.load(),
        "nav_links": models.NavLink.objects.filter(is_visible=True),
    }
