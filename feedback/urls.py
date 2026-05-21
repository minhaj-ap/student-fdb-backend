from django.urls import path
from .views import FeedbackListCreateView, FeedbackDetailView

urlpatterns = [
    path('feedbacks/', FeedbackListCreateView.as_view()),
    path('feedbacks/<int:pk>/', FeedbackDetailView.as_view()),
]