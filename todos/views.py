from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from accounts.serializers import *
from django.http import HttpResponse, JsonResponse, request
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])   # 허가: 조건에 맞는 사람들 허가
@authentication_classes([JSONWebTokenAuthentication])  # JWT 방식으로 인증 및 허가 하겠다.
def todo_create(request):
    if request.method == 'GET':
        userdata = User.objects.all()
        userid = 0
        for i in range(len(userdata)):
            if userdata[i] == request.user:
                userid = i
                break    
        userid += 1
        todo = Todo.objects.filter(user_id=userid)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data)
            # return JsonResponse({'result':'true'})
        return HttpResponse(status=400)

        # title = request.data['title']
        # user = request.user
        # todo = Todo.objects.create(title=title, user=user)
        # todo.save()
        # return JsonResponse({'result':'true'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def todo_detail(request, id):
    todo = get_object_or_404(Todo, id=id)
    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data)
        return HttpResponse(status=400)
    elif request.method == 'DELETE':
        todo.delete()
        return JsonResponse({'msg': '삭제되었습니다.'})
        # return HttpResponse(status=204)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def user_detail(req, id):
    user = get_object_or_404(User, id=id)

    if req.user != user:
        return HttpResponse(status=403)

    if req.method == 'GET':
        serializer = UserSeriralizer(user)
        return JsonResponse(serializer.data)
    else:
        if request.user == user:
            if request.method == 'PUT':
                serializer = UserChangeSerializer(user, request.data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    serializer = UserSerializer(user)
                    return JsonResponse(serializer.data)
            else:
                username = user.username
                user.delete()
                return JsonResponse({'message': f'그동안 감사했습니다. {username}님. 다시 만나기를 기대하겠습니다.'})
    return HttpResponse('잘못된 접근입니다.', status=403)