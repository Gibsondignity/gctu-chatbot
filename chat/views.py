from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import Chat, Conversation
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
    conversations = Conversation.objects.filter(user=request.user).order_by('-updated_at')[:10]
    return render(request, 'index.html', {'conversations': conversations})



@csrf_exempt
def response(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user_question = body.get("message")
        conversation_id = body.get("conversation_id")
        if not user_question:
            return JsonResponse({"error": "No message provided"}, status=400)

        answer = ask_bot(user_question)

        # Save to database
        if request.user.is_authenticated:
            if conversation_id:
                try:
                    conversation = Conversation.objects.get(id=conversation_id, user=request.user)
                except Conversation.DoesNotExist:
                    return JsonResponse({"error": "Conversation not found"}, status=404)
            else:
                # Create new conversation
                conversation = Conversation.objects.create(
                    user=request.user,
                    title=user_question[:50] + "..." if len(user_question) > 50 else user_question
                )

            # Save the chat message
            Chat.objects.create(
                conversation=conversation,
                message=user_question,
                response=answer
            )

            # Update conversation timestamp
            conversation.save()

        return JsonResponse({
            "response": answer,
            "conversation_id": str(conversation.id) if 'conversation' in locals() else None
        })
    

@csrf_exempt
@login_required
def fetch_chats(request):
    conversation_id = request.GET.get("conversation_id")
    page_number = int(request.GET.get("page", 1))
    page_size = 10  # Number of messages per scroll load

    if conversation_id:
        chats = Chat.objects.filter(
            conversation_id=conversation_id,
            conversation__user=request.user
        ).order_by("created_at")
    else:
        chats = Chat.objects.filter(conversation__user=request.user).order_by("-created_at")[:page_size]

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

@login_required
def get_conversations(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-updated_at')
    print("Printing conversation: ", conversations)
    data = [
        {
            "id": str(conv.id),
            "title": conv.title,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat()
        }
        for conv in conversations
    ]
    return JsonResponse({"conversations": data})