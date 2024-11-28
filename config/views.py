from django.http import JsonResponse

def api_only_view(request):

    return JsonResponse({"detail": "This resource is intended only for API."})
