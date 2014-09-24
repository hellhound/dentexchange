# -*- coding:utf-8 -*-
from django.db.models import Q

from haystack import indexes

from celery_haystack.indexes import CelerySearchIndex

from location.models import ZipCode
from .models import EmployeeQuestionnaire


class EmployeeQuestionnaireIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # Shitty workaround to the content__contains problem
    contains = indexes.EdgeNgramField(use_template=True,
        template_name='search/indexes/employee/'
        'employeequestionnaire_text.txt')
    first_name = indexes.CharField(
        model_attr='user__userregistration__first_name')
    last_name = indexes.CharField(
        model_attr='user__userregistration__last_name')
    email = indexes.CharField(model_attr='user__email')
    job_position = indexes.IntegerField(model_attr='job_position', null=True)
    job_position_text = indexes.CharField(
        model_attr='get_job_position_display', null=True)
    solo_practitioner = indexes.BooleanField(model_attr='solo_practitioner')
    multi_practitioner = indexes.BooleanField(model_attr='multi_practitioner')
    corporate = indexes.BooleanField(model_attr='corporate')
    fee_for_service = indexes.BooleanField(model_attr='fee_for_service')
    insurance = indexes.BooleanField(model_attr='insurance')
    capitation_medicaid = indexes.BooleanField(model_attr='capitation_medicaid')
    zip_code = indexes.DecimalField(model_attr='zip_code', null=True)
    city = indexes.CharField(model_attr='city', null=True)
    state = indexes.CharField(model_attr='state', null=True)
    distance = indexes.IntegerField(model_attr='distance', null=True)
    distance_text = indexes.CharField(
        model_attr='get_distance_display', null=True)
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
    experience_years = indexes.IntegerField(model_attr='experience_years',
        null=True)
    dental_school = indexes.CharField(model_attr='dental_school')
    graduation_year = indexes.IntegerField(model_attr='graduation_year',
        null=True)
    visa = indexes.BooleanField(model_attr='visa')
    visa_text = indexes.CharField(model_attr='get_visa_display')
    specific_strengths = indexes.CharField(model_attr='specific_strengths')
    matches = indexes.MultiValueField()
    location = indexes.LocationField()

    def get_model(self):
        return EmployeeQuestionnaire

    def _get_default_filter_query(self):
        return Q(is_private=False)

    def index_queryset(self, using=None):
        return super(EmployeeQuestionnaireIndex, self).index_queryset(
            using=using).filter(self._get_default_filter_query())

    def build_queryset(self, using=None, start_date=None, end_date=None):
        return super(EmployeeQuestionnaireIndex, self).build_queryset(
            using=using, start_date=start_date, end_date=end_date).filter(
            self._get_default_filter_query())

    def update_object(self, identifier, using=None, **kwargs):
        instance = get_instance_from_identifier(identifier)
        if not instance.is_private:
            self.remove_object(identifier, using=using, **kwargs)
        super(EmployeeQuestionnaire, self).update_object(instance, using=using,
            **kwargs)

    def prepare_matches(self, obj):
        return [match.user.pk for match in obj.matches.all()]

    def get_updated_field(self):
        return 'updated'

    def prepare_location(self, obj):
        try:
            zip_code = ZipCode.objects.get(code=obj.zip_code)
        except (ZipCode.DoesNotExist, ZipCode.MultipleObjectsReturned):
            return '.0,.0'
        return '%s,%s' % (zip_code.latitude, zip_code.longitude)
