from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from wagtail.documents import urls as wagtaildocs_urls
from coderedcms import admin_urls as coderedadmin_urls
from coderedcms import search_urls as coderedsearch_urls
from coderedcms import urls as codered_urls

from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    # Swagger
    path(r'swagger(format\.json|\.yaml)', schema_view.without_ui(cache_timeout=0),
                      name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Admin
    path('django-admin/', admin.site.urls),
    path('admin/', include(coderedadmin_urls)),

    # Documents
    path('docs/', include(wagtaildocs_urls)),

    # Search
    path('search/', include(coderedsearch_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # the page serving mechanism. This should be the last pattern in
    # the list:
    re_path(r'', include(codered_urls)),

    # Alternatively, if you want CMS pages to be served from a subpath
    # of your site, rather than the site root:
    #    re_path(r"^pages/", include(codered_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
