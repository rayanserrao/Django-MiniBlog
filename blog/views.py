from django.shortcuts import render,HttpResponseRedirect,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm
from blog.forms import SignupForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from blog.models import Post,BlogComment
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    posts = Post.objects.all()  # to get all the post in home page
    return render(request,'home.html',{'posts':posts})

def bloghome(request):
    posts = Post.objects.all()
    return render(request,'bloghome.html',{'posts':posts})

def blogs(request,blogid):
    posts= Post.objects.get(id=blogid)
    comment = BlogComment.objects.filter(post=posts)
    return render(request,'blogs.html',{'posts':posts,'comment':comment})

#comments
def postcomment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment') 
        user = request.user
        postid  = request.POST.get('postid')
        post = Post.objects.get(id=postid)
        # parent

        comment = BlogComment(comment=comment,user=user,post=post)
        comment.save()
        messages.success(request,"comment added succesfully")
    
    return redirect(f'/blogs/{post.id}')


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
    return HttpResponseRedirect('/')
    

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

def search(request):
    query = request.GET['query']
    if len(query)>40:
        posts = Post.objects.none()
    else:

        poststitle = Post.objects.filter(title__icontains=query)
        postdesc = Post.objects.filter(desc__icontains=query)
        posts=poststitle.union(postdesc)

    if posts.count() == 0:
       messages.warning(request,"Please search for correct keyword")

    return render(request,'search.html',{'posts':posts,'query':query})

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

