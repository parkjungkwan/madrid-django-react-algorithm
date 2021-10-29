from django.http import JsonResponse
from icecream import ic
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from admin.user.models import User
from admin.user.serializers import UserSerializer

@api_view(['GET','POST','PUT'])
@parser_classes([JSONParser])
def users(request):
    if request.method == 'GET':
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return JsonResponse(data = serializer, safe = False)
    elif request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'result' : f'Welcome, {serializer.data.get("name")}'}, status=201)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':

        return None

@api_view(['DELETE'])
def remove(request, id):
    pass

@api_view(['POST'])
def login(request):
    try:
        loginUser = request.data
        # print(f'{type(loginUser)}') # <class 'dict'>
        ic(loginUser)
        dbUser = User.objects.get(pk = loginUser['username'])
        # print(f'{type(dbUser)}') # <class 'admin.user.models.User'>
        ic(dbUser)
        if loginUser['password'] == dbUser.password:
            print('******** 로그인 성공')
            userSerializer = UserSerializer(dbUser, many=False)
            ic(userSerializer)
            return JsonResponse(data=userSerializer.data, safe=False)
        else:
            print('******** 비밀번호 오류')
            return JsonResponse(data={'result':'PASSWORD-FAIL'}, status=201)

    except User.DoesNotExist:
        print('*' * 50)
        print('******** Username 오류')
        return JsonResponse(data={'result':'USERNAME-FAIL'}, status=201)




