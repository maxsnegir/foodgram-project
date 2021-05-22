from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views

handler404 = "recipes.views.page_not_found"  # noqa
handler500 = "recipes.views.server_error"  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('user/', include('users.urls', namespace='users')),
    path('about-us/', views.flatpage, {'url': '/about-us/'},
         name='about'),
    path('tech/', views.flatpage, {'url': '/tech/'},
         name='tech'),
    path('', include('recipes.urls', namespace='recipes')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
