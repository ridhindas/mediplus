from django.shortcuts import render,redirect
from . models import *


# Create your views here.

def index(request):
    return render(request,'index.html')

def home(request):
    return render(request,'index.html')

def services(request):
    return render(request,'services.html')

def contact(request):
    return render(request,'contact.html')


    
# registration
def user_register(request):
    if request.method=="POST":
      userphoto=request.FILES["userphoto"]
      username=request.POST.get("username") 
      useremail=request.POST.get("useremail")
      userphone=request.POST.get("userphone")
      userpassword=request.POST.get("userpassword")
      data=user_details(userphoto=userphoto ,username=username,useremail=useremail,userphone=userphone,userpassword=userpassword)
      data.save()
      return redirect(login) 
    return render(request,'user_register.html')




# logout form
 


def logout(request):
   session_keys = list(request.session.keys())
   for key in session_keys:
          del request.session[key]
   return redirect(index)

   
  


 