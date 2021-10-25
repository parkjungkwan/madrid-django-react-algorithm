from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from admin.iris.models import Iris
from models import Imdb


@api_view(['GET'])
@parser_classes([JSONParser])
def imdb_process(request):
    Imdb().imdb_process()
    return JsonResponse({'Imdb Process': 'SUCCESS'})
