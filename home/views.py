from django.shortcuts import render
import requests

# Create your views here.

def index(request):
    return render(request, 'index.html')

def nodes(request):
    return render(request, 'nodes.html')

def node(request, node_id):
    return render(request, 'node.html')