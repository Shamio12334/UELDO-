from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import dashboard, event_detail, register_event, view_pass, lobby, payment_page

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Google Login
    path('accounts/', include('allauth.urls')),
    
    # App Pages
    path('', dashboard, name='dashboard'),
    path('event/<int:event_id>/', event_detail, name='event_detail'),
    path('register/<int:event_id>/', register_event, name='register_event'),
    path('payment/<int:registration_id>/', payment_page, name='payment_page'),
    path('my-pass/<str:pass_id>/', view_pass, name='view_pass'),
    path('lobby/<int:event_id>/', lobby, name='lobby'),
]

# 👇 Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)