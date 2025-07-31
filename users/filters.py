import django_filters
from .models import UserProfile

class UserProfileFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    is_verified = django_filters.BooleanFilter()
    is_admin = django_filters.BooleanFilter()
    address = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = UserProfile
        fields = ['username', 'is_verified', 'is_admin', 'address']
