from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken import views
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, TaskSerializer, StatsSerializer
from .models import Task


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]


class UserLogin(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        if not created:
            token.delete()
            token = Token.objects.create(user=user)

        token = Token.objects.get(key=token)
        update_last_login(None, user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, ]


class StatsView(views.APIView):
    def get(self, request):
        queryset = Task.objects.all()
        serializer = StatsSerializer(queryset)
        return Response(serializer.data)
