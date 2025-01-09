from django.shortcuts import HttpResponse , render, redirect
from .models import Contact
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from blog.models import Blog

# Create your views here.
def home(request):

      top_posts = Blog.objects.all().order_by('-views')[:3]
      context = {'top_posts':top_posts}
      return render(request, 'home/home.html', context)
def about(request):
     return render(request, 'home/about.html')


def contact(request):
    if request.method=="POST":
        name = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,  "fill valid details")
        else:
           contact = Contact(name=name, phone=phone, email=email, content=content )
           contact.save()
        messages.success(request,  " your content upload successfully")
        
       
        
    return render(request, 'home/contact.html')
       
        
   

def search(request):
    query=request.GET['query']
    if len(query)>78:
         allPosts = []
    else:    
        allPosttitle= Blog.objects.filter(title__icontains=query)
        allPostcontent= Blog.objects.filter(content__icontains=query)
        allPostauthor= Blog.objects.filter(author__icontains=query)

        allPosts = allPosttitle.union(allPostcontent,allPostauthor)

    if allPosts.count()==0:
         messages.warning(request, "No search result found please refind your query")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

def handlesignup(request):
     if request.method=='POST':
         username = request.POST['username']
         email=request.POST['email']
         fname=request.POST['fname']
         lname=request.POST['lname']
         pass1=request.POST['pass1']
         pass2=request.POST['pass2']
         
         if len(username)<3:
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('home')

         if not username.isalnum():
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('home')
         if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('home')


         myuser = User.objects.create_user( username, email, pass1)
         myuser.first_name = fname
         myuser.last_name = lname
         myuser.save()
         messages.success(request,  " Your iCoder has been successfully created")
         return redirect('home')
     else:
        return HttpResponse("404 - Not found")
     
     

def handlelogin(request):
 if request.method == 'POST':
     loginusername = request.POST['loginusername']
     loginpass = request.POST['loginpassword']
     User = authenticate(username=loginusername, password=loginpass)

     if User is not None:
         login(request, User)
         messages.success(request, "login is successfully")
         return redirect('home')
     else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

     return HttpResponse("404- Not found")
    
def handlelogout(request):
     logout(request)
     messages.success(request, "logout successfully")
     return redirect("home")
     

