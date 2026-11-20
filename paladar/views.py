from django.shortcuts import HttpResponse


def health(request):

    return HttpResponse("OK")