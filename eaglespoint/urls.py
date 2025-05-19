from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from core.views import page_not_found_view

handler404 = page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls', namespace='user')),
    path('', include('core.urls', namespace='core')),
    path('listing/', include('listing.urls', namespace='listing')),
    path('messaging/', include('messaging.urls', namespace='messaging')),
    path('adminv2/', include('adminv2.urls', namespace='adminv2')),
    
    path("components/", include("django_components.urls")),
]

# if settings.DEBUG:  # Serve media files during development
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
