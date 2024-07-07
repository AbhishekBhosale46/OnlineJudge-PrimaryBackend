from rest_framework import serializers
from core.models import *


class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'title', 'difficulty']


class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ['id', 'title', 'description', 'difficulty']


class LanguageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class TestCaseListSerializer(serializers.ModelSerializer):
    std_in = serializers.SerializerMethodField()
    expected_out = serializers.SerializerMethodField()

    class Meta:
        model = TestCase
        fields = ['id', 'std_in', 'expected_out']

    def get_std_in(self, testcase):
        with testcase.std_input.open('r') as file:
            return file.read()

    def get_expected_out(self, testcase):
        with testcase.expected_output.open('r') as file:
            return file.read()


class SubmissionSerializer(serializers.ModelSerializer):
    submission_status = serializers.SerializerMethodField()
    testcase_results = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ['id', 'problem', 'language', 'code', 'submission_status', 'created_at', 'testcase_results']
        read_only = ['id', 'submission_status', 'created_at', 'testcase_results']
        extra_kwargs = {
            'language': {'write_only': True},
            'code': {'write_only': True},
        }
    
    def get_submission_status(self, submission):
        return submission.status

    def get_testcase_results(self, submission):
        return "testcase results here"