from CISCO_DNAC_APP.models import WebhookEvents
import django_filters
from django import forms

class WebhookEventsFilter(django_filters.FilterSet):
    source_ip = django_filters.CharFilter(lookup_expr='icontains')  # input should be case-insensitive and it may match part of the name.
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')
    # https://stackoverflow.com/questions/14456503/how-to-get-a-particular-attribute-from-queryset-in-django-in-view
    severity = django_filters.ModelMultipleChoiceFilter(queryset=WebhookEvents.objects.all().values_list('severity', flat=True).distinct().order_by('severity'),
        widget=forms.CheckboxSelectMultiple, lookup_expr='iexact')
    domain = django_filters.CharFilter(lookup_expr='icontains')
    timestamp_year = django_filters.NumberFilter(field_name='Date', lookup_expr='year')
    day__gte = django_filters.NumberFilter(field_name='Date', lookup_expr='day__gte')
    day__lte = django_filters.NumberFilter(field_name='Date', lookup_expr='day__lte')
    month__gte = django_filters.NumberFilter(field_name='Date', lookup_expr='month__gte')
    month__lte = django_filters.NumberFilter(field_name='Date', lookup_expr='month__lte')
    year__gte = django_filters.NumberFilter(field_name='Date', lookup_expr='year__gte')
    year__lte = django_filters.NumberFilter(field_name='Date', lookup_expr='year__lte')
    issue_description = django_filters.CharFilter(lookup_expr='icontains')
    actual_service_id = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = WebhookEvents
        fields = ['source_ip', 'title', 'category', 'severity', 'domain', 'issue_description', 'actual_service_id',]
