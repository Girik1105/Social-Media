from django.shortcuts import render
from django.views.generic import ListView, TemplateView

# Create your views here.
class home(TemplateView):
    template_name = 'index.html'

class thanks(TemplateView):
    template_name = 'thanks.html'
