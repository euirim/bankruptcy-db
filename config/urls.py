from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from rest_framework.routers import DefaultRouter

from bankruptcy.cases.views import CaseViewSet, DocketEntryViewSet, DocumentViewSet, SearchViewSet

router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'docket-entries', DocketEntryViewSet, basename='docket_entry')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'search', SearchViewSet, basename='search')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

urlpatterns += [
    re_path(r"^(?P<path>.*)/$", TemplateView.as_view(template_name="build/index.html")),
    path("", TemplateView.as_view(template_name="build/index.html"), name="home"),
]
