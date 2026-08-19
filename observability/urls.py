from django.urls import path
from .views import metrics_view,MeetingListCreateView, MessageListCreateView

urlpatterns = [
    path("metrics/",metrics_view,name="metrics_root"),
    path('meetings/', MeetingListCreateView.as_view(), name='meetings'),
    path('messages/', MessageListCreateView.as_view(), name='messages'),
]
