import time

from django.http import HttpResponse, JsonResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter
from rest_framework import generics

from .models import Meeting, Message
from .serializers import MeetingSerializer, MessageSerializer

REQUESTS = Counter('example_requests_total', 'Total HTTP requests (example)')


def health_view(request):
    return JsonResponse({"status": "ok"})


def metrics_view(request):
    REQUESTS.inc()
    return HttpResponse(generate_latest(), content_type=CONTENT_TYPE_LATEST)


class MeetingListCreateView(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def get(self, request, *args, **kwargs):
        time.sleep(2)  # simulate slow DB or heavy processing
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        time.sleep(2)
        return super().post(request, *args, **kwargs)


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer