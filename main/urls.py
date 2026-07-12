from django.urls import path

from .views import result_page,voter_dashboard
urlpatterns = [
    # path('admin/', admin.site.urls),
    
    path("results/", result_page, name="result_page"),
    path("dashboard/", voter_dashboard, name="voter_dashboard")
]