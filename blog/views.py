from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from blog.forms import SignupForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from blog.models import Post
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    posts = Post.objects.all()  # to get all the post in home page
    return render(request,'home.html',{'posts':posts})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        # to show the profile of an author in dahshboard page
        user = request.user
        username = user.get_username()
        fullname = user.get_full_name()
        fullname = fullname.capitalize()  # it will combine both firstname and last name
        allgroups = user.groups.all()    # to get the data which group he belongs to

        return render(request,'dashboard.html',{'posts':posts,'fullname':fullname,'allgroups':allgroups,'username':username})
    else:
        return HttpResponseRedirect('/login/')

def user_Logout(request):
    logout(request)
    messages.success(request,'loged out successfully')
    return HttpResponseRedirect('/login/')
    

def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            #adding members to author group
            group = Group.objects.get(name='Author')
            user.groups.add(group)

            messages.success(request,"You have been Signed Up Successfully")
            return HttpResponseRedirect('/login/')
    else:

        form= SignupForm()
    return render(request,'signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:

        if request.method == 'POST':
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Logedin Successfully")
                    return HttpResponseRedirect('/dashboard/')
        else:


            form = LoginForm()
        return render(request,'login.html',{'form':form})

    else:
        return HttpResponseRedirect('/dashboard/')

#CRUD operations
#add new post
def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                author = form.cleaned_data['author']
                desc = form.cleaned_data['desc']
                pst = Post(title=title,author=author,desc=desc)
                pst.save()
                messages.success(request,"Post added successfully")
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
            
            

        return render(request,'addpost.html',{'form':form})

    else:

        return HttpResponseRedirect('/login/')

#Update post
def updatepost(request,editid):
    if request.user.is_authenticated:
        obj = Post.objects.get(id=editid)
        if request.method == 'POST':
            form = PostForm(request.POST,instance=obj) # instace=id if we wont use it willcreate new entry
            if form.is_valid():
                form.save()
                messages.success(request,"data upated succesfully")
                return HttpResponseRedirect('/dashboard/')

        else:
            form = PostForm(instance=obj)

        return render(request,'updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')

#delte post
def deletepost(request,delid):
    if request.user.is_authenticated:
        if request.method == 'POST':
            obj = Post.objects.get(id=delid)
            obj.delete()
            messages.info(request,"Post deleted successfully")
            return HttpResponseRedirect('/dashboard/')

        
    else:
        return HttpResponseRedirect('/login/')

