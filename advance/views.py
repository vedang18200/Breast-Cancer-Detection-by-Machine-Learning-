from django.shortcuts import render

# Create your views here.
def advance_page(request):
    return render(request, 'advance.html')
