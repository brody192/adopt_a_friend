from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('create_testimonial/', views.create_testimonial, name='create_testimonial'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('testimonials/<int:testimonial_id>/', views.testimonial_detail, name='detail'),
]