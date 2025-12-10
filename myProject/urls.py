from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('myApp.dashboard_urls')),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('core-beliefs/', views.core_beliefs, name='core_beliefs'),
    path('what-we-do/', views.what_we_do, name='what_we_do'),
    path('events/', views.events, name='events'),
    path('mission-accomplished/', views.mission_accomplished, name='mission_accomplished'),
    path('donate/', views.donate, name='donate'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
    path('privacy/', views.privacy, name='privacy'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
