from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from icecream import ic

@api_view(['GET'])
@parser_classes([JSONParser])
def housing(request):
    return JsonResponse({'result': 'Housing Success'})
