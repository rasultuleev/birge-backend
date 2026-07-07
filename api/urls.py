from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check),
    path('send-code/', views.send_sms_code),
    path('verify-code/', views.verify_code),
    path('profile/', views.get_profile),
    path('profile/update/', views.update_profile),
    path('register-event/', views.register_event),
    path('events/', views.event_list),
    path('register-organization/', views.register_organization),
    path('import-students/', views.import_students),
]
