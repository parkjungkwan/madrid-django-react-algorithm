from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from admin.iris.models import Iris


@api_view(['GET'])
@parser_classes([JSONParser])
def base(request):
    Iris().base()
    return JsonResponse({'Iris Base': 'SUCCESS'})

@api_view(['GET'])
@parser_classes([JSONParser])
def advanced(request):
    Iris().advanced()
    return JsonResponse({'Iris Advanced': 'SUCCESS'})

@api_view(['GET'])
@parser_classes([JSONParser])
def iris_by_tf(request):
    Iris().iris_by_tf()
    return JsonResponse({'Iris Tensorflow': 'SUCCESS'})