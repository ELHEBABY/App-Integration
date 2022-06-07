from django.shortcuts import redirect
from .tasks import integrationTask

def launch_the_integration(request):
    integrationTask()
    return redirect("/integration")


