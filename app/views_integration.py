


from django.shortcuts import redirect
from .tasks import test_func

def launch_the_integration(request):
    test_func()
    return redirect("/integration")


