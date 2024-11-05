# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_list_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from business.models import User, Chat, Jobs
from twilio.rest import Client
from .forms import JobPosts

def home(request):
    jobs = Jobs.objects.all().values()[ :10]
    
    return render(request, 'mainpage.html', {"jobs": jobs})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "You login to website sucessfully")
                return redirect('profile')  # Redirect to a homepage or dashboard
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def registeruser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        department = request.POST.get("department")
        
        print(request.POST)
        user = User.objects.filter(username  = username)
        
        if user.exists():
            messages.error(request, "Username is already taken")
            return redirect('registration')
            
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            is_staff= False,
            is_admin = False,
            departmant = department,
            password=password
        )
        
        user.save()
        messages.success(request, "Registration is successfully completed")
        return redirect('login')
    
    return render(request, 'register.html')

@login_required
def profile(request):
    depart = request.user.departmant
    if (((depart != "Job") or (depart != "Employers")) and request.user.is_admin):
        showUser = True
    else:
        showUser = False
    
    return render(request, 'home.html', {"user" : request.user, "show": showUser})

@login_required
def create_post(request):
    if request.method == "POST":
        post = request.POST.get('post')
        company = request.POST.get('company')
        description = request.POST.get('description')
        rating = request.POST.get('rating')
        
        job = Jobs.objects.create(
            post = post,
            company_name = company,
            description = description,
            rating=rating
        )
        
        job.save()
        messages.success(request, "Job created successfully")
        return redirect('jobs')
        
    return render(request, 'createjob.html')

@login_required
def job_search(request):
    jobs = Jobs.objects.all().values()
    if request.method == "POST":
        search = request.POST.get("searching")
        if search != "":
            jobs = Jobs.objects.filter(post__contains=search)
        else:
            messages.warning(request,"Please type any word")
    
    return render(request, 'jobsearch.html', {"jobs" : jobs})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You logged out from the portal")
    return redirect('home')

@login_required
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        is_admin = request.POST.get("is_admin") == 'on'
        department = request.POST.get("depart")
            
        user = User.objects.filter(username  = username)
        
        if user.exists():
            messages.error(request, "Username is already taken")
            return redirect('adduser')
            
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            is_staff= not is_admin,
            is_admin = is_admin,
            departmant = department,
            password=password
        )
            
        user.save()
            
        messages.info(request, "User Created SuccessFully")
        return redirect('viewuser')
    return render(request, 'adduser.html')
 
@login_required       
def view_user(request):
    if request.user.username == "Admin":
        users = User.objects.exclude(username="Admin")
    else:
        users = User.objects.filter(departmant=request.user.departmant).values().exclude(username="Admin")
    
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
        
        chat = Chat.objects.create(
            sender_id=current_user,
            content=content,
            msg_receiver=receiver
        )
        
        chat.save()
        
        return redirect('viewchat')
    
    return render(request, "createchat.html")

