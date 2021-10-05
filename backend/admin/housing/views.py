from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from admin.housing.models import HousingService
from icecream import ic
import matplotlib.pyplot as plt
@api_view(['GET'])
@parser_classes([JSONParser])
def housing(request):
    hs = HousingService()
    h = hs.new_model()
    ic(h.head(3))
    ic(h.tail(3))
    ic(h.info())
    ic(h.describe())
    h.hist(bins = 50, figsize=(20,15))
    plt.savefig('admin/housing/image/housing-hist.png')
    return JsonResponse({'result': 'Housing Success'})
