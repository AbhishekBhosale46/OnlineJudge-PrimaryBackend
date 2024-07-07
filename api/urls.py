from django.urls import path
from .views import *

urlpatterns = [
    path('problems/', ProblemList.as_view(), name='problem-list'),
    path('problems/<int:pk>', ProblemDetail.as_view(), name='problem-detail'),
    path('problems/<int:id>/testcases/', TestCaseList.as_view(), name='testcase-list'),
    path('languages/', LanguageList.as_view(), name='language-list'),
    path('submit/', SubmissionView.as_view(), name='submission'),
]
