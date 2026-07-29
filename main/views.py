from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.http import JsonResponse
from .utils import compute_ip_hash,validate_device,validate_matric_number
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from .models import RegisteredUser
from .forms import VoteForm,CustomUserCreationForm,CandidateCreationForm
from .models import Election,Vote,Candidate,Position,Student
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import CreateView 
from django.urls import reverse

# from .forms import 

"""
compute user ip address and use username as key
"""
# @validate_device
@login_required
def voter_dashboard(request):
    election = Election.objects.last()
    print(timezone.now() > election.scheduled_date)
    print(timezone.now() < election.end_date)
    if  timezone.now() > election.scheduled_date and timezone.now() < election.end_date :
        election.status = "VOTING"
        election.save()
        print("voting ....") 
    print(election.status)
    positions = Position.objects.all()
    candidates = Candidate.objects.filter(election=election)
    voted_posts = Vote.objects.filter(election=election,user=request.user).values_list("position_id")
    if len(voted_posts) > 0:
        positions = Position.objects.exclude(id__in=voted_posts)
    election_time_exceeded = False
    if timezone.now() <= election.scheduled_date or timezone.now() >= election.end_date:
        print("closing election")
        election_time_exceeded = True
        # election.status = "CLOSED"
        # election.save()
    is_registered = False
    is_registered_candidate = False
    try:
        registered_user = RegisteredUser.objects.get(election=election,user=request.user)
        is_registered = True
    except:
        pass
    try:
        full_name = f"{request.user.last_name} {request.user.first_name}"
        c = Candidate.objects.get(election=election,name_of_candidate=full_name)
        print(c)
        is_registered_candidate = True
    except Exception:
        print("error occured")
        pass
    context = {
               "election":election,
               "election_time_exceeded":election_time_exceeded,
               "positions":positions,"candidate_creation_form":CandidateCreationForm,
               "candidates":candidates,"is_registered":is_registered,
               "is_registered_candidate":is_registered_candidate}
    return render(request,"main/voter-dashboard.html",context)

class CustomLoginView(SuccessMessageMixin,LoginView):
    template_name = "main/login.html"
    success_message = 'Welcome to your profile'


    

@login_required
def result_page(request):
    election = Election.objects.last()
    positions = Position.objects.all()
    
    results_data = []
    for p in positions:
        candidates = Candidate.objects.filter(election=election,position=p).annotate(vote_count=Count("vote")).values("name_of_candidate","vote_count")

        results_data.append({
            'position': p.position,
            'labels': [c["name_of_candidate"] for c in candidates],
            'votes': [c["vote_count"] for c in candidates],
        })
        print(results_data)
    # print(type(request.META["REMOTE_ADDR"]))
    context = {"results_data":results_data}
    return render(request,"main/result-page.html",context)

def blocked_device(request):
    return render(request,"main/blocked-user.html")

def registration(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            matric_number = form.cleaned_data["username"]
            if  validate_matric_number(matric_number):
                try:
                    student = Student.objects.get(matric_number=matric_number)
                except:
                    messages.error(request,"Verification failed your details is wrong or have not been unboarded")
                    return redirect("user_register")
                form.save()
                messages.success(request,"Registraion successful proceed to login")
                return redirect("user_login")
            else:
                messages.error(request,"Invalid matric number format ")
                return redirect("user_register")
    context = {"form":form}
    return render(request,"main/registration.html",context)

@require_POST
def create_candidate(request):
    election = Election.objects.last()
    form = CandidateCreationForm(request.POST,request.FILES)
    print(form.is_valid())
    if form.is_valid():
        pre_save = form.save(commit=False)
        pre_save.election = election
        pre_save.name_of_candidate = f"{request.user.last_name} {request.user.first_name}"
        pre_save.save()
        print("redirecting to dashboard")
    return redirect("voter_dashboard") 
    # return redirect()

@require_POST
def register_election(request):
    election = Election.objects.last()
    user = request.user
    registered_user = RegisteredUser.objects.create(user=user,election=election)
    return redirect("voter_dashboard")

@require_POST
def cast_vote(request):
    election = Election.objects.last()
    voter_form = VoteForm(request.POST)
    if request.method == "POST":
        print(voter_form.is_valid())
        if voter_form.is_valid():
            if election.status == "VOTING":
                print("form validation")
                print(voter_form.cleaned_data["candidate"])
                cand = Candidate.objects.get(id=voter_form.cleaned_data["candidate"])
                post = Position.objects.get(id=cand.position.id)
                try:
                    Vote.objects.get(election=election,user=request.user,candidate=cand)
                    return JsonResponse({"success":False,"msg":"You have voted already"})
                except:
                    Vote.objects.create(election=election,user=request.user,candidate=cand,position=post)
                    return JsonResponse({"success":True,"msg":"vote submitted sucessfully"})
        return JsonResponse({"success":False,"msg":"election closed"})


class CandidateCreateView(CreateView):
    model = Candidate
    template_name = "main/candidate_registration.html"
    form_class = CandidateCreationForm
    success_url = "voter_dashboard"



class CustomPasswordChangeView(PasswordChangeView):
	template_name = "main/change_password.html"
	def get_success_url(self):
		messages.success(self.request,"password change success")
		return reverse("voter_dashboard")
		

def redirect_login(request):
    return redirect("user_login")