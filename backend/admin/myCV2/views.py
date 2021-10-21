from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from admin.myCV2.models import MyCV2


@api_view(['GET'])
@parser_classes([JSONParser])
def lena(request):
    MyCV2().lena()
    return JsonResponse({'MyCV2 LENA': 'SUCCESS'})

@api_view(['GET'])
@parser_classes([JSONParser])
def girl(request):
    MyCV2().girl()
    return JsonResponse({'MyCV2 Girl': 'SUCCESS'})
