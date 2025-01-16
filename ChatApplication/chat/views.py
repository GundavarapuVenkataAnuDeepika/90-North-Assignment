from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import ChatMessage
from django.contrib.auth.models import User
from django.db.models import Q
def index(request):
    return render(request, 'index.html')

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat_home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# User sign-up view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('chat_home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Chat home view
@login_required
def chat_home(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'chat_home.html', {'users': users})

# Chat interface view
@login_required
def chat_interface(request, username):
    receiver = get_object_or_404(User, username=username)
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(receiver=receiver)) |
        (Q(sender=receiver) & Q(receiver=request.user))
    ).order_by('timestamp')
    return render(request, 'chat_interface.html', {
        'receiver': receiver,
        'messages': messages
    })