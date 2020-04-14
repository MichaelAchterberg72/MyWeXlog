from django.urls import path

from .import views

app_name = 'Feedback'

urlpatterns = [
    path('feedback/', views.FeedBackView, name='FeedBack'),
]
