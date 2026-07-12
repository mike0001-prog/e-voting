from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.views import LoginView
from .utils import compute_ip_hash,validate_device
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import VoteForm
from .models import Election,Vote,Candidate,Position,Student
from django.utils import timezone
import datetime
from django.db.models import Count
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

"""
compute user ip address and use username as key
"""
# @validate_device
@login_required
def voter_dashboard(request):
    election = Election.objects.last()
    print(election.scheduled_date)
    # datetime.datetime().now()
    print(election.scheduled_date < timezone.now())
    if election.scheduled_date < timezone.now():
        pass
    else:
        return redirect("")
    
    user = request.user
    if request.method == "POST":
        voted = get_object_or_404(Vote,election=election,user=request.user)
        print(request.POST)
    voter_form = VoteForm
    context = {"form":voter_form}
    return render(request,"main/voter-dashboard.html",context)

class CustomLoginView(SuccessMessageMixin,LoginView):
    template_name = "main/login.html"
    success_message = 'Welcome to your profile'


    

@login_required
def result_page(request):
    election = Election.objects.last()
    positions = Position.objects.all()
    candidates = Candidate.objects.filter(election=election).annotate(vote_count=Count("vote"))
    print(candidates)
    for c in candidates:
        print(c.vote_count)
    print(type(request.META["REMOTE_ADDR"]))
    context = {}
    return render(request,"main/result-page.html",context)

def blocked_device(request):
    return render(request,"main/blocked-user.html")

def registration(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            student = get_object_or_404(Student,username=username)
            if student:
                form.save()
                return redirect("user_login")
            else:
                messages.add_message(request,2,"Verification failed your details is wrong or have nor been unboarded")
        pass
    context = {"form":form}
    return render(request,"main/registration.html",context)
