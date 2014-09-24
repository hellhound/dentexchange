# -*- coding:utf-8 -*-
from django.db.models import Q

from haystack import indexes

from celery_haystack.indexes import CelerySearchIndex

from libs.haystack.utils import get_instance_from_identifier
from location.models import ZipCode
from .models import JobPosting


class JobPostingIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # Shitty workaround to the content__contains problem
    contains = indexes.EdgeNgramField(use_template=True,
        template_name='search/indexes/employer/jobposting_text.txt')
    company_name = indexes.CharField(model_attr='praxis__company_name')
    email = indexes.CharField(model_attr='praxis__business__user__email')
    address = indexes.CharField(model_attr='praxis__address')
    zip_code = indexes.DecimalField(model_attr='praxis__zip_code')
    city = indexes.CharField(model_attr='praxis__city')
    state = indexes.CharField(model_attr='praxis__state')
    solo_practitioner = indexes.BooleanField(
        model_attr='praxis__solo_practitioner')
    multi_practitioner = indexes.BooleanField(
        model_attr='praxis__multi_practitioner')
    corporate = indexes.BooleanField(model_attr='praxis__corporate')
    fee_for_service = indexes.BooleanField(
        model_attr='praxis__fee_for_service')
    insurance = indexes.BooleanField(model_attr='praxis__insurance')
    capitation_medicaid = indexes.BooleanField(
        model_attr='praxis__capitation_medicaid')
    position_name = indexes.CharField(model_attr='position_name')
    posting_title = indexes.CharField(model_attr='posting_title')
    job_position = indexes.IntegerField(model_attr='job_position')
    job_position_text = indexes.CharField(model_attr='get_job_position_display')
    schedule_type = indexes.BooleanField(model_attr='schedule_type')
    schedule_type_text = indexes.CharField(
        model_attr='get_schedule_type_display')
    monday_daytime = indexes.BooleanField(model_attr='monday_daytime')
    monday_evening = indexes.BooleanField(model_attr='monday_evening')
    tuesday_daytime = indexes.BooleanField(model_attr='tuesday_daytime')
    tuesday_evening = indexes.BooleanField(model_attr='tuesday_evening')
    wednesday_daytime = indexes.BooleanField(model_attr='wednesday_daytime')
    wednesday_evening = indexes.BooleanField(model_attr='wednesday_evening')
    thursday_daytime = indexes.BooleanField(model_attr='thursday_daytime')
    thursday_evening = indexes.BooleanField(model_attr='thursday_evening')
    friday_daytime = indexes.BooleanField(model_attr='friday_daytime')
    friday_evening = indexes.BooleanField(model_attr='friday_evening')
    saturday_daytime = indexes.BooleanField(model_attr='saturday_daytime')
    saturday_evening = indexes.BooleanField(model_attr='saturday_evening')
    sunday_daytime = indexes.BooleanField(model_attr='sunday_daytime')
    sunday_evening = indexes.BooleanField(model_attr='sunday_evening')
    compensation_type = indexes.BooleanField(model_attr='compensation_type')
    hourly_wage = indexes.IntegerField(model_attr='hourly_wage', null=True)
    hourly_wage_text = indexes.CharField(
        model_attr='get_hourly_wage_display', null=True)
    annualy_wage = indexes.IntegerField(model_attr='annualy_wage', null=True)
    annualy_wage_text = indexes.CharField(
        model_attr='get_annualy_wage_display', null=True)
    production = indexes.BooleanField(model_attr='production')
    collection = indexes.BooleanField(model_attr='collection')
    experience_years = indexes.IntegerField(model_attr='experience_years')
    benefit_1 = indexes.BooleanField(model_attr='benefit_1')
    benefit_2 = indexes.BooleanField(model_attr='benefit_2')
    benefit_3 = indexes.BooleanField(model_attr='benefit_3')
    benefit_4 = indexes.BooleanField(model_attr='benefit_4')
    benefit_5 = indexes.BooleanField(model_attr='benefit_5')
    benefit_6 = indexes.BooleanField(model_attr='benefit_6')
    benefit_other_text = indexes.CharField(model_attr='benefit_other_text')
    visa = indexes.BooleanField(model_attr='visa')
    visa_text = indexes.BooleanField(model_attr='get_visa_display')
    additional_comments = indexes.CharField(model_attr='additional_comments')
    matches = indexes.MultiValueField()
    location = indexes.LocationField()

    def get_model(self):
        return JobPosting

    def _get_default_filter_query(self):
        return Q(is_posted=True)

    def index_queryset(self, using=None):
        return super(JobPostingIndex, self).index_queryset(using=using).filter(
            self._get_default_filter_query())

    def read_queryset(self, using=None):
        return super(JobPostingIndex, self).read_queryset(using=using).filter(
            self._get_default_filter_query())

    def build_queryset(self, using=None, start_date=None, end_date=None):
        return super(JobPostingIndex, self).build_queryset(
            using=using, start_date=start_date, end_date=end_date).filter(
            self._get_default_filter_query())

    def update_object(self, identifier, using=None, **kwargs):
        instance = get_instance_from_identifier(identifier)
        if not instance.is_posted:
            self.remove_object(identifier, using=using, **kwargs)
        super(JobPostingIndex, self).update_object(instance, using=using,
            **kwargs)

    def prepare_matches(self, obj):
        return [match.user.pk for match in obj.matches.all()]

    def get_updated_field(self):
        return 'updated'

    def prepare_location(self, obj):
        try:
            zip_code = ZipCode.objects.get(code=obj.praxis.zip_code)
        except (ZipCode.DoesNotExist, ZipCode.MultipleObjectsReturned):
            return '.0,.0'
        return '%s,%s' % (zip_code.latitude, zip_code.longitude)
