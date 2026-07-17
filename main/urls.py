from django.urls import path
from .views import result_page,voter_dashboard,CandidateCreateView,create_candidate,register_election
urlpatterns = [
    path("results/", result_page, name="result_page"),
    path("dashboard/", voter_dashboard, name="voter_dashboard"),
    # path("candidate_registration/", CandidateCreateView.as_view(), name="candidate_registration"),
    path("create_candidate/", create_candidate, name="create_candidate"),
    path("register_election/", register_election, name="register_election")
    
]