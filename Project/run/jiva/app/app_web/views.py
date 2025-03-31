from django.shortcuts import render

app_name = 'app_web'
# Create your views here.
def welcome(request):
    
    context = {
        'page': 'welcome',
    }
    template_file = f"{app_name}/welcome/welcome.html"
    return render(request, template_file, context)