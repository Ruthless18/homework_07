from django.shortcuts import render

from mainapp.models import Computer_system


def main_page(request):
    computer_systems = Computer_system.objects.all()
    context = {
        'computer_systems': computer_systems
    }
    return render(request, 'computersystems/index.html', context = context)