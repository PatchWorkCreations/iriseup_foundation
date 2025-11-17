from django.shortcuts import render

def home(request):
    return render(request, 'myApp/home.html')

def about(request):
    return render(request, 'myApp/about.html')

def core_beliefs(request):
    return render(request, 'myApp/core_beliefs.html')

def what_we_do(request):
    return render(request, 'myApp/what_we_do.html')

def events(request):
    return render(request, 'myApp/events.html')

def mission_accomplished(request):
    return render(request, 'myApp/mission_accomplished.html')

def donate(request):
    return render(request, 'myApp/donate.html')

def contact(request):
    return render(request, 'myApp/contact.html')
