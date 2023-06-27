from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from testapp1 import views


urlpatterns = [
    path('', views.api_root.as_view(),name = 'home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view.as_view(), name='logout'),
    path('submissions/',views.submissions_list.as_view(), name = 'submissions-list'),
    path('submissions/<int:pk>/highlight/', views.submissions_detail.as_view(), name = 'submission-highlight'),
    #path('submissions/<int:pk>/', views.submissions_detail.as_view(), name = 'submission-detail'),
    path('submissions/<str:R_UserName>/', views.SubmissionsByRecruiterView.as_view(),name='submissions-by-recruiter'),
    path('recruiters/', views.RecruiterListView.as_view(), name='recruiter-list'),
    path('recruiters/<uuid:pk>/', views.RecruiterDetailView.as_view(), name='recruiter-detail'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('success/', views.success_view, name = 'success'),
    ]

urlpatterns = format_suffix_patterns(urlpatterns)