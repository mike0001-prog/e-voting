from django.contrib import admin
from .models import *

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    model = Election



@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    model = Vote

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    model = Candidate

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    model = Position



