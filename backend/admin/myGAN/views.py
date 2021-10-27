from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from admin.myGAN.models import AutoencodersGans


@api_view(['GET'])
@parser_classes([JSONParser])
def autoencodersGans_process(request):
    AutoencodersGans().process()
    return JsonResponse({'Autoencoders Gans': 'SUCCESS'})

