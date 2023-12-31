from django.contrib import admin
from django.urls import path, include
from main.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('', include('testimonials.urls')),
    path('about/', about, name='about'),
    path('admin/', admin.site.urls),
    path('', include('videochat.urls')),
    path('verification/', include('verify_email.urls')),	
    path('', include("users.urls")),
    path('', include("pets.urls")),
    path('', include("staff.urls")),
    path('', include("donation.urls")),
    path('', include("videochat.urls")),
    path('', include('chat.urls')),
    path('', include('reports.urls', namespace='reports')),
]     

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'main.views.error_404'