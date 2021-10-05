from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from admin.housing.models import HousingService
from icecream import ic

@api_view(['GET'])
@parser_classes([JSONParser])
def housing(request):
    h = HousingService()
    ic(h.new_model())
    return JsonResponse({'result': 'Housing Success'})
