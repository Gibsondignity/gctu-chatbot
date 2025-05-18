from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import Chat
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
import numpy as np
import uuid
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

from django.views.decorators.csrf import csrf_exempt
from chatbot import ask_bot  # import from your chatbot.py
import json

from django.core.paginator import Paginator
from django.utils.decorators import method_decorator



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')




def landing(request):
    return render(request, 'landing.html')




def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in right after registering
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})



@login_required
def index(request):
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'index.html', {'chats': chats})



@csrf_exempt
def response(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user_question = body.get("message")
        if not user_question:
            return JsonResponse({"error": "No message provided"}, status=400)

        answer = ask_bot(user_question)

        # Save to database
        if request.user.is_authenticated:
            Chat.objects.create(user=request.user, message=user_question, response=answer)

        return JsonResponse({"response": answer})
    

@csrf_exempt
@login_required
def fetch_chats(request):
    page_number = int(request.GET.get("page", 1))
    page_size = 10  # Number of messages per scroll load

    chats = Chat.objects.filter(user=request.user).order_by("created_at")
    paginator = Paginator(chats, page_size)
    page = paginator.get_page(page_number)

    data = [
        {"message": chat.message, "response": chat.response, "created_at": chat.created_at.isoformat()}
        for chat in page
    ]
    return JsonResponse({
        "chats": data,
        "has_next": page.has_next()
    })