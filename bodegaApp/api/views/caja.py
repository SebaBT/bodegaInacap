from django.http import JsonResponse
from bodegaApp.models import Caja

def cajas_por_locker(request, id):
    cajas = Caja.objects.filter(locker=id).values('id', 'nameTag')  # Get id and nameTag
    return JsonResponse(list(cajas), safe=False)