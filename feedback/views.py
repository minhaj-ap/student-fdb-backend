from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackListCreateView(generics.ListCreateAPIView):
    
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Feedback.objects.all().order_by('-created_at')
        
        return Feedback.objects.filter(user = self.request.user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Feedback.objects.all()
        return Feedback.objects.filter(user = self.request.user)
    
    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(status='pending')
        else:
            serializer.save()