import django_filters
from .models import Posts

class PostslFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='exact')
    created_time__gte = django_filters.DateFilter(field_name='created_time', lookup_expr='gte')
    created_time__lte = django_filters.DateFilter(field_name='created_time', lookup_expr='lte')

    class Meta:
        model = Posts
        fields = []
