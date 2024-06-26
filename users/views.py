from django.shortcuts import render ,redirect
from .forms import NewUserForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


def  register(request):

    if request.method=="POST":
        form=NewUserForm(request.POST)
        # validation
        if form.is_valid():
            user = form.save()
            return redirect('/myapp/products')

    form=NewUserForm()
    context={
        "form":form,
    }
    return render(request,"temp/register.html",context)
    


@login_required
def profile(request):

    return render(request,"temp/profile.html")

    



def create_profile(request):


    if request.method=="POST":
        image = request.FILES['upload']
        contact_number=request.POST.get("contact_number")
        # currently logged-in user
        user= request.user
        # Add DB
        profile = Profile(user =user,contact_number=contact_number,image=image)
        profile.save()
        return redirect("/users/profile")
        
    return render(request,"temp/create_profile.html")


# seller >> user !
def seller_profile(request, id):
    seller = User.objects.get(id=id)
    context={
        "seller":seller
    }
    
    return render(request,"temp/sellerprofile.html",context)