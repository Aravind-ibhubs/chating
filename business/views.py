# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_list_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from business.models import User, Chat
from twilio.rest import Client


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a homepage or dashboard
            else:
                return redirect('login') # Redirect to Login Page
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html', {"user" : request.user})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        is_admin = request.POST.get("is_admin") == 'on'
            
        user = User.objects.filter(username  = username)
        
        if user.exists():
            messages.info(request, "Username is already taken")
            return redirect('adduser')
            
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            is_staff= not is_admin,
            is_admin = is_admin,
            password=password
        )
            
        user.save()
            
        messages.info(request, "User Created SuccessFully")
        return redirect('viewuser')
    return render(request, 'adduser.html')
 
@login_required       
def view_user(request):
    users = User.objects.all().values()
    
    return render(request, 'users.html', {'users' : users})

@login_required
def display_chat(request):
    chat = Chat.objects.filter(sender_id=request.user).values()
    # if request.method == "GET":
    #     user = request.GET.get("username")
    #     anotherUser = User.objects.filter(username=user).values()
    #     print(anotherUser)
    #     chatOfOther = Chat.objects.filter(sender_id=anotherUser).values()
    #     return render(request, "displaychat.html", {"messages": chatOfOther})
    
    return render(request, "displaychat.html", {"messages": chat})

def display_other_chat(request, user_id):
    chat = Chat.objects.filter(sender_id=user_id).values()
    
    return render(request, "anotherchat.html", {"messages": chat})
    

@login_required
def create_chat(request):
    if request.method == "POST":
        current_user = request.user
        content = request.POST.get("message")
        receiver = request.POST.get("receiver")
        
        account_sid = 'AC089a50721eca956f9c1922e4ba480ef9'
        auth_token = '7b5566d7fd2d7c9788f3c0796a315f6a'
        client = Client(account_sid, auth_token)
        
        from_whatsapp = 'whatsapp:+917997627817'
        to_whatsapp = f'whatsapp:+91{receiver}'
        
        message = client.messages.create(
            body=content,
            from_='whatsapp:+14155238886',
            to=f'whatsapp:+91{receiver}'
        )
        
        print(message)
        
        chat = Chat.objects.create(
            sender_id=current_user,
            content=content,
            msg_receiver=receiver
        )
        
        chat.save()
        
        return redirect('viewchat')
    
    return render(request, "createchat.html")

