import requests
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
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


class SubmissionView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            submission = serializer.save(user=self.request.user)
            language = submission.language.file_extension
            time_limit = submission.problem.time_limit
            memory_limit = submission.problem.memory_limit
            src_code = submission.code
            test_cases = TestCase.objects.filter(problem=submission.problem)
            for test_case in test_cases:
                with test_case.std_input.open('r') as file:
                    std_input = file.read()
                with test_case.expected_output.open('r') as file:
                    expected_out = file.read()
                testcase_result = TestCaseResult.objects.create(
                    submission=submission,
                    test_case=test_case
                )
                callback_url = f"/evaluate-testcase-result/{testcase_result.id}"
                post_data = {
                    "language": language,
                    "time_limit": time_limit,
                    "memory_limit": memory_limit,
                    "src_code": src_code,
                    "std_in": std_input,
                    "expected_out": expected_out,
                    "callback_url": callback_url
                }
                # requests.post(settings.JUDGE_SERVER_SUBMIT_URL, json=post_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)