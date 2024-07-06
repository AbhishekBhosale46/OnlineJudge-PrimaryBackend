from rest_framework import generics
from rest_framework.decorators import permission_classes, authentication_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from core.models import *
from api.serializers import *


class ProblemList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Problem.objects.all() 
    serializer_class = ProblemListSerializer


class ProblemDetail(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Problem.objects.all() 
    serializer_class = ProblemDetailSerializer


class LanguageList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Language.objects.all() 
    serializer_class = LanguageListSerializer 


class TestCaseList(generics.ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = TestCase.objects.all() 
    serializer_class = TestCaseListSerializer

    def get_queryset(self):
        problem_id = self.kwargs['id']
        return TestCase.objects.filter(problem=problem_id, is_public=True)