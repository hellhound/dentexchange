# -*- coding:utf-8 -*-
import random
import string
import hashlib
import base64

from django.contrib.auth.models import User

from libs.auth.builder import UserFactory
from libs import constants as libs_constants
from registration.models import UserRegistration
from registration import constants as reg_constants
from employer.models import Business, Praxis, JobPosting
from employer import constants as employer_constants
from employee.models import EmployeeQuestionnaire
from employee import constants as employee_constants
from membership.models import PlanPrice, Membership
from membership.utils import (MembershipExpirationDateAdapter,
    MembershipRestrictionAdapter)
from .utils import (RandomPerson, RandomOpening, RandomProfession,
    RandomExperienceWord, RandomSpecialty, RandomRequirement,
    RandomDentalSchool, CliProgressBar)
from .base import BaseBuilder
from . import constants

bar = CliProgressBar(constants.TOTAL_EMPLOYERS + constants.TOTAL_EMPLOYEES \
    + constants.TOTAL_POSTINGS)


class UserRegistrationBuilder(BaseBuilder):
    model = UserRegistration

    def __init__(self):
        self._user = None

    @property
    def is_employer(self):
        raise NotImplementedError(u'is_employer() should be implemented')

    def get_email(self):
        username = constants.EMPLOYER_EMAIL_USERNAME \
            if self.is_employer else constants.EMPLOYEE_EMAIL_USERNAME
        return '%s%i@%s' % (username, self.tally, constants.EMAIL_DOMAIN)

    @property
    def user(self):
        if self._user is None:
            self._user = UserFactory.create_user(
                self.get_email(), constants.USER_PASSWORD)
        return self._user

    @property
    def build_kwargs(self):
        random_person = RandomPerson()
        return dict(
            user=self.user,
            is_employer=self.is_employer,
            first_name=random_person.first_name,
            last_name=random_person.last_name,
            personal_address=random_person.address,
            personal_zip_code=random_person.zip_code,
            personal_city=random_person.city,
            personal_state=random_person.state)

    def build(self):
        registration = super(UserRegistrationBuilder, self).build()
        MembershipBuilder(self.user).build()
        return registration


class EmployerBuilder(UserRegistrationBuilder):
    def __init__(self):
        super(EmployerBuilder, self).__init__()
        self.reset_remaining_postings()

    @property
    def is_employer(self):
        return reg_constants.USER_REGISTRATION_IS_EMPLOYER_CHOICES.EMPLOYER

    @property
    def remaining_postings(self):
        return self._remaining_postings

    @remaining_postings.setter
    def remaining_postings(self, value):
        self._remaining_postings -= 1

    def reset_remaining_postings(self):
        self._remaining_postings = constants.POSTINGS_PER_EMPLOYER_MAX

    def get_praxes_count(self):
        return random.randint(constants.PRAXIS_PER_EMPLOYER_MIN,
            constants.PRAXIS_PER_EMPLOYER_MAX)

    def build(self):
        employer = bar.update(super(EmployerBuilder, self).build)
        business = BusinessBuilder(employer.user).build()
        praxes = [PraxisBuilder(business).build()
            for _ in xrange(self.get_praxes_count())]
        [JobPostingBuilder.build_batch(praxis, self) for praxis in praxes]
        return employer


class EmployeeBuilder(UserRegistrationBuilder):
    @property
    def is_employer(self):
        return reg_constants.USER_REGISTRATION_IS_EMPLOYER_CHOICES.EMPLOYEE

    def build(self):
        employee = bar.update(super(EmployeeBuilder, self).build)
        EmployeeQuestionnaireBuilder(employee.user).build()
        return employee


class NeedsUserBuilderMixin(object):
    def __init__(self, user, *args, **kwargs):
        super(NeedsUserBuilderMixin, self).__init__(*args, **kwargs)
        self._user = user

    @property
    def user(self):
        return self._user


class MembershipBuilder(NeedsUserBuilderMixin, BaseBuilder):
    model = Membership
    plan_types = list(PlanPrice.objects.all().prefetch_related('plan'))

    @property
    def customer_id(self):
        return 'cus_%s' % base64.b64encode(hashlib.sha512().hexdigest())[:14]

    @property
    def cc_last4(self):
        return str(random.randint(1000, 9999))

    @property
    def plan_type(self):
        return random.choice(self.plan_types)

    @property
    def build_kwargs(self):
        random_person = RandomPerson()
        return dict(
            user=self.user,
            customer_id=self.customer_id,
            cc_last4=self.cc_last4,
            plan_type=self.plan_type,
            first_name=random_person.first_name,
            last_name=random_person.last_name,
            email=random_person.email,
            address=random_person.address,
            zip_code=random_person.zip_code,
            city=random_person.city,
            state=random_person.state,
            country=random_person.country)

    def build(self):
        membership = super(MembershipBuilder, self).build()
        MembershipRestrictionAdapter(membership).reset_restrictions()
        MembershipExpirationDateAdapter(membership).save_end_date()
        return membership


class BusinessBuilder(NeedsUserBuilderMixin, BaseBuilder):
    model = Business

    @property
    def number_offices(self):
        return self.get_random_choice(
            employer_constants.BUSINESS_NUMBER_OFFICES_CHOICES)

    @property
    def is_mso(self):
        return self.get_random_choice(libs_constants.YES_NO_CHOICES)

    @property
    def number_employees(self):
        return self.get_random_choice(
            employer_constants.BUSINESS_NUMBER_EMPLOYEES_CHOICES)

    @property
    def build_kwargs(self):
        return dict(
            user=self.user,
            number_offices=self.number_offices,
            is_mso=self.is_mso,
            number_employees=self.number_employees)


class PraxisBuilder(BaseBuilder):
    model = Praxis

    def __init__(self, business):
        self._business = business

    @property
    def business(self):
        return self._business

    @property
    def build_kwargs(self):
        random_person = RandomPerson()
        return dict(
            business=self.business,
            company_name=random_person.company_name,
            contact_first_name=random_person.first_name,
            contact_last_name=random_person.last_name,
            address=random_person.address,
            zip_code=random_person.zip_code,
            city=random_person.city,
            state=random_person.state,
            solo_practitioner=self.random_bool,
            multi_practitioner=self.random_bool,
            corporate=self.random_bool,
            fee_for_service=self.random_bool,
            insurance=self.random_bool,
            capitation_medicaid=self.random_bool)


class ProfileBuilder(BaseBuilder):
    def __init__(self):
        self._job_position = None

    @property
    def job_position(self):
        if self._job_position is None:
            self._job_position = self.get_random_choice(
                employee_constants.JOB_POSITION_CHOICES)
        return self._job_position

    @property
    def experience_years(self):
        return self.get_random_choice(
            employee_constants.EXPERIENCE_YEARS_CHOICES)

    @property
    def schedule_type(self):
        return self.get_random_choice(employee_constants.SCHEDULE_TYPE_CHOICES)

    @property
    def compensation_type(self):
        return self.get_random_choice(
            employee_constants.COMPENSATION_TYPE_CHOICES)

    @property
    def hourly_wage(self):
        return self.get_random_choice(employee_constants.HOURLY_WAGE_CHOICES)

    @property
    def annualy_wage(self):
        return self.get_random_choice(employee_constants.ANNUALY_WAGE_CHOICES)

    @property
    def description(self):
        total_comments = random.randint(3, 7)
        selector = random.randint(0, 2)
        additional_comments = ''
        if selector == 0:
            additional_comments = '\n'.join(
                self.lorem.get_sentences_list(total_comments))
        elif selector == 1:
            additional_comments = '\n'.join(
                [RandomRequirement() for _ in xrange(total_comments)])
        return additional_comments


class JobPostingBuilder(ProfileBuilder):
    model = JobPosting

    def __init__(self, praxis):
        super(JobPostingBuilder, self).__init__()
        self._praxis = praxis

    @property
    def praxis(self):
        return self._praxis

    @property
    def position_name(self):
        return '%s (%s)' % (
            unicode(
            employee_constants.JOB_POSITION_CHOICES[self.job_position - 1][1]),
            random.choice(string.ascii_lowercase.upper()))

    @property
    def posting_title(self):
        with_opening = self.random_bool
        two_specialties = self.random_bool
        specialties = RandomSpecialty()
        if two_specialties:
            specialties += ' and %s' % RandomSpecialty()
        title = '%s with %s in %s' % (
            RandomProfession(), RandomExperienceWord(), specialties)
        if with_opening:
            title = '%s ' % RandomOpening() + title
        return title

    @property
    def benefit_other_text(self):
        total_comments = random.randint(3, 7)
        return '\n'.join(self.lorem.get_sentences(total_comments))

    @property
    def build_kwargs(self):
        schedule_type = self.schedule_type
        compensation_type = self.compensation_type
        benefit_other = self.random_bool
        posting = dict(
            praxis=self.praxis,
            position_name=self.position_name,
            posting_title=self.posting_title,
            job_position=self.job_position,
            schedule_type=schedule_type,
            compensation_type=compensation_type,
            production=self.random_bool,
            collection=self.random_bool,
            experience_years=self.experience_years,
            benefit_1=self.random_bool,
            benefit_2=self.random_bool,
            benefit_3=self.random_bool,
            benefit_4=self.random_bool,
            benefit_5=self.random_bool,
            benefit_6=self.random_bool,
            benefit_other=benefit_other,
            visa=self.random_bool,
            additional_comments=self.description,
            is_posted=self.random_bool)
        if schedule_type == employee_constants.SCHEDULE_TYPE_CHOICES.PART_TIME:
            posting.update(dict(
                monday_daytime=self.random_bool,
                monday_evening=self.random_bool,
                tuesday_daytime=self.random_bool,
                tuesday_evening=self.random_bool,
                wednesday_daytime=self.random_bool,
                wednesday_evening=self.random_bool,
                thursday_daytime=self.random_bool,
                thursday_evening=self.random_bool,
                friday_daytime=self.random_bool,
                friday_evening=self.random_bool,
                saturday_daytime=self.random_bool,
                saturday_evening=self.random_bool,
                sunday_daytime=self.random_bool,
                sunday_evening=self.random_bool))
        if compensation_type \
                == employee_constants.COMPENSATION_TYPE_CHOICES.SALARY:
            posting.update(dict(annualy_wage=self.annualy_wage))
        else:
            posting.update(dict(hourly_wage=self.hourly_wage))
        if benefit_other:
            posting.update(dict(benefit_other_text=self.benefit_other_text))
        return posting

    @classmethod
    def build_batch(cls, praxis, employer_builder):
        remaining_postings = constants.TOTAL_POSTINGS - cls.tally
        remaining_employers = constants.TOTAL_EMPLOYERS - EmployerBuilder.tally
        if remaining_employers > 0:
            if float(remaining_postings) / remaining_employers \
                    <= employer_builder.remaining_postings:
                posting_count = min(remaining_postings,
                    employer_builder.remaining_postings)
            else:
                posting_count = random.randint(
                    constants.POSTINGS_PER_EMPLOYER_MIN,
                    max(constants.POSTINGS_PER_EMPLOYER_MIN,
                    employer_builder.remaining_postings))
            employer_builder.remaining_postings -= posting_count
            return [bar.update(cls(praxis).build)
                for _ in xrange(posting_count)]
        return None


class EmployeeQuestionnaireBuilder(NeedsUserBuilderMixin, ProfileBuilder):
    model = EmployeeQuestionnaire

    @property
    def distance(self):
        return self.get_random_choice(
            employee_constants.DISTANCE_CHOICES)

    @property
    def dental_school(self):
        return RandomDentalSchool()

    @property
    def graduation_year(self):
        return self.get_random_choice(
            employee_constants.GRADUATION_YEAR_CHOICES)

    @property
    def build_kwargs(self):
        random_person = RandomPerson()
        schedule_type = self.schedule_type
        compensation_type = self.compensation_type
        questionnaire = dict(
            user=self.user,
            job_position=self.job_position,
            solo_practitioner=self.random_bool,
            multi_practitioner=self.random_bool,
            corporate=self.random_bool,
            fee_for_service=self.random_bool,
            insurance=self.random_bool,
            capitation_medicaid=self.random_bool,
            zip_code=random_person.zip_code,
            city=random_person.city,
            state=random_person.state,
            distance=self.distance,
            schedule_type=schedule_type,
            compensation_type=compensation_type,
            production=self.random_bool,
            collection=self.random_bool,
            experience_years=self.experience_years,
            dental_school=self.dental_school,
            graduation_year=self.graduation_year,
            visa=self.random_bool,
            specific_strengths=self.description,
            is_private=self.random_bool)
        if schedule_type == employee_constants.SCHEDULE_TYPE_CHOICES.PART_TIME:
            questionnaire.update(dict(
                monday_daytime=self.random_bool,
                monday_evening=self.random_bool,
                tuesday_daytime=self.random_bool,
                tuesday_evening=self.random_bool,
                wednesday_daytime=self.random_bool,
                wednesday_evening=self.random_bool,
                thursday_daytime=self.random_bool,
                thursday_evening=self.random_bool,
                friday_daytime=self.random_bool,
                friday_evening=self.random_bool,
                saturday_daytime=self.random_bool,
                saturday_evening=self.random_bool,
                sunday_daytime=self.random_bool,
                sunday_evening=self.random_bool))
        if compensation_type \
                == employee_constants.COMPENSATION_TYPE_CHOICES.SALARY:
            questionnaire.update(dict(annualy_wage=self.annualy_wage))
        else:
            questionnaire.update(dict(hourly_wage=self.hourly_wage))
        return questionnaire
