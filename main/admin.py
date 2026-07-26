from django.contrib import admin
from .models import *
from django.urls import path
from django.db.models import Count

admin.site.site_header = 'E-VOTING Administration'

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    model = Election
    actions = ['go_to_custom_page']



    @admin.action(description='View election details')
    def go_to_custom_page(self, request, queryset):
        print(queryset)
        election = queryset[0]
        print( queryset[0])
        from django.shortcuts import render
        positions = Position.objects.all()
        results_data = []
        for p in positions:
                candidates = Candidate.objects.filter(election=election,position=p).annotate(vote_count=Count("vote")).values("name_of_candidate","vote_count")
                results_data.append({
                    'position': p.position,
                    'labels': [c["name_of_candidate"] for c in candidates],
                    'votes': [c["vote_count"] for c in candidates],
                })
                
        context = {"results_data":results_data}
        return render(request,"main/admin_election_report.html",context)
        



@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    model = Vote

    def has_add_permission(self,request):
        return False

    def has_change_permission(self,request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    model = Candidate

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    model = Position

@admin.register(RegisteredUser)
class RegisteredUserAdmin(admin.ModelAdmin):
    model = RegisteredUser

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    model = Student


