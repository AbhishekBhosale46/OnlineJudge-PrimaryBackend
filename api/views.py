import requests
from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import get_object_or_404
from core.models import *
from api.serializers import *
from .permissions import AllowSpecificIP


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
                callback_url = f"{settings.CALLBACK_URL}/{testcase_result.id}"
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


class UserSubmissionDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class UserSubmissionsListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubmissionSerializer

    def get_queryset(self):
        user = self.request.user
        problem_id = self.kwargs['id']
        return Submission.objects.filter(user=user, problem_id=problem_id)


class WebhookHandlerView(views.APIView):
    authentication_classes = []
    permission_classes = [AllowSpecificIP]
    def post(self, request, id):
        test_case_result = get_object_or_404(TestCaseResult, id=id)
        judge_server_status =  request.data.get("status", "PENDING")
        test_case_result.status = judge_server_status
        test_case_result.save()
        return Response({"message": "Webhook received!"}, status=status.HTTP_200_OK)