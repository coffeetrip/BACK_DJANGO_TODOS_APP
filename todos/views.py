from django.shortcuts import render, get_object_or_404
from .models import *
from .serializer import *
from accounts.serializers import *
from django.http import HttpResponse, JsonResponse, request
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAuthenticated])   # 허가: 조건에 맞는 사람들 허가
@authentication_classes([JSONWebTokenAuthentication])  # JWT 방식으로 인증 및 허가 하겠다.
def todo_create(request):
    serializer = TodoSerializer(data=request.POST)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
        # return JsonResponse({'result':'true'})
    return HttpResponse(status=400)