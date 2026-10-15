from django.shortcuts import render,redirect
from mediplus.models import user_details
from mediplus.models import doctor_details
from user_app.models import appointment_details
# Create your views here.

def userview(request):
    data=user_details.objects.all()
    return render(request,'userview.html',{'userdata':data})



def userupdate(request,id):
    data=user_details.objects.get(pk=id)
    return render(request,'userupdate.html',{'result':data})
    
def userupdates(request, id):
    data = user_details.objects.get(id=id)

    if request.method == "POST":
        data.username = request.POST.get("username")
        data.useremail = request.POST.get("useremail")
        data.userphone = request.POST.get("userphone")
        data.userpassword = request.POST.get("userpassword")

        # Only update photo if a new one is uploaded
        if "userphoto" in request.FILES:
            data.userphoto = request.FILES["userphoto"]

        data.save()
        return redirect(userview)

    return render(request, 'userupdate.html', {"data": data})

# def userupdates(request,id):
#     if request.method=="POST":
#       userphoto=request.FILES["userphoto"]
#       username=request.POST.get("username")
#       useremail=request.POST.get("useremail")
#       userphone=request.POST.get("userphone")
#       userpassword=request.POST.get("userpassword")
#       data=user_details(id=id,userphoto=userphoto,username=username,useremail=useremail,userphone=userphone,userpassword=userpassword)
#       data.save()
#       return redirect(userview)
#     return render(request,'userupdate.html') 

def doctor_register(request):
    if request.method=="POST":
      docphoto=request.FILES["docphoto"]
      docname=request.POST.get("docname")
      docspeciallization=request.POST.get("docspeciallization")
      docpayment=request.POST.get("docpayment")
      doctiming=request.POST.get("doctiming")
      data=doctor_details(docphoto=docphoto,docname=docname,docspeciallization=docspeciallization,docpayment=docpayment,doctiming=doctiming)
      data.save()
    return render(request,'doctor_register.html')

def doctor_view(request):
    data=doctor_details.objects.all()
    return render(request,'doctor_view.html',{'doctordata':data})

def doctordelete(request,id):
    data=doctor_details.objects.get(pk=id)
    data.delete()     
    return redirect(doctor_view)

def doctorupdate(request,id):
    data=doctor_details.objects.get(pk=id)
    return render(request,'doctorupdate.html',{'result':data})

def doctorupdates(request,id):
    if request.method=="POST": 
      docphoto=request.FILES["docphoto"]
      docname=request.POST.get("docname")
      docspeciallization=request.POST.get("docspeciallization")
      docpayment=request.POST.get("docpayment")
      doctiming=request.POST.get("doctiming")
      data=doctor_details(id=id,docphoto=docphoto,docname=docname,docspeciallization=docspeciallization,docpayment=docpayment,doctiming=doctiming)
      data.save()
      return redirect(doctor_view)
    return render(request,'doctorupdate.html')


def adminapp_view(request):
  
    data=appointment_details.objects.all()
    return render(request,'adminapp_view.html',{'result':data})
