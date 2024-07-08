from rest_framework.permissions import BasePermission
from django.conf import settings

class AllowSpecificIP(BasePermission):
    def has_permission(self, request, view):
        allowed_ips = getattr(settings, 'ALLOWED_JUDGE_SERVER_IP', '')
        ip_addr = request.META.get('REMOTE_ADDR')
        return ip_addr == allowed_ips
