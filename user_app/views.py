from django.shortcuts import render,redirect
from mediplus . models import user_details
from mediplus . models import doctor_details
from . models import *
# Create your views here.

# login
def bookapp(request):
    userid=request.session['uid']  
    docdet=doctor_details.objects.all()  
    if request.method=="POST":
        patientname=request.POST.get("patientname")
        patientage=request.POST.get("patientage")
        patientemail=request.POST.get("patientemail")
        patientphone=request.POST.get("patientphone")
        docname=request.POST.get("docname")
        bookingdate=request.POST.get("bookingdate")
        patientproblem=request.POST.get("patientproblem")
        data=appointment_details(userid=userid,patientname=patientname,patientage=patientage,patientemail=patientemail,patientphone=patientphone,docname=docname,bookingdate=bookingdate,patientproblem=patientproblem)
        data.save()
    return render(request,'appointment.html',{'result':docdet})
    
# profile
def userprofile(request):
    userid=request.session['uid']
    data=user_details.objects.get(pk=userid)
    return render(request,'userprofile.html',{'result':data})

def appointment_view(request):
    userid=request.session['uid']
    data=appointment_details.objects.filter(userid=userid)
    return render(request,'appointment_view.html',{'result':data})

def appointdelete(request,id):
    data=appointment_details.objects.get(pk=id)
    data.delete()
    return redirect(bookapp)

