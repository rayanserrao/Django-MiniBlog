from django.urls import path
from blog.views import home,about,contact,dashboard,user_login,user_Logout,user_signup,addpost,updatepost,deletepost,bloghome,blogs,search

urlpatterns = [
    path('', home),
    path('about/',about),
    path('bloghome/',bloghome),
    path('blogs/<int:blogid>',blogs),
    path('search/',search),
    path('contact/',contact),
    path('dashboard/',dashboard),
    path('logout/',user_Logout),
    path('signup/',user_signup),
    path('login/',user_login),
    path('addpost/',addpost,name='addpost'),
    path('editpost/<int:editid>',updatepost,name='editpost'),
    path('deletepost/<int:delid>',deletepost,name='deletepost'),
    

    
]