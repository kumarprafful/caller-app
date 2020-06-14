from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny,])
def register(request):
    try:
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'status': 'success', 'data': {'refresh':str(refresh), 'access': str(refresh.access_token)}}, status=200)
        else:
            return Response({'status':'error', 'message':serializer.errors}, status=400)
    except Exception as e:
        return Response({'status':'error', 'message': str(e)}, status=400)
