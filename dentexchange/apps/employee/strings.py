# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _


# EmployeeQuestionnaire's strings

EMPLOYEE_QUESTIONNAIRE_USER = _(u'User')
### Personal Info
EMPLOYEE_QUESTIONNAIRE_FIRST_NAME = _(u'First Name')
EMPLOYEE_QUESTIONNAIRE_LAST_NAME = _(u'Last Name')
EMPLOYEE_QUESTIONNAIRE_PERSONAL_ADDRESS = _(u'Street')
EMPLOYEE_QUESTIONNAIRE_ZIP_CODE = _(u'Zip Code')
EMPLOYEE_QUESTIONNAIRE_CITY = _(u'City')
EMPLOYEE_QUESTIONNAIRE_STATE = _(u'State')
### Job Position you're looking for
EMPLOYEE_QUESTIONNAIRE_JOB_POSITION = _(u'Job Position')
### Type of Practice
EMPLOYEE_QUESTIONNAIRE_SOLO_PRACTITIONER = _(u'Solo Practitioner')
EMPLOYEE_QUESTIONNAIRE_MULTI_PRACTITIONER = _(u'Multi-Practitioner')
EMPLOYEE_QUESTIONNAIRE_CORPORATE = _(u'Corporate')
### Patients' Method of Payment
EMPLOYEE_QUESTIONNAIRE_FEE_FOR_SERVICE = _(u'Fee for Service')
EMPLOYEE_QUESTIONNAIRE_INSURANCE = _(u'Insurance')
EMPLOYEE_QUESTIONNAIRE_CAPITATION_MEDICAID = _(u'Capitation/Medicaid')
### Location
EMPLOYEE_QUESTIONNAIRE_DISTANCE = _(u'Distance you will travel')
EMPLOYEE_QUESTIONNAIRE_SCHEDULE_TYPE = _(u'Type of schedule required')
EMPLOYEE_QUESTIONNAIRE_MONDAY_DAYTIME = _(u'Monday Daytime')
EMPLOYEE_QUESTIONNAIRE_MONDAY_EVENING = _(u'Monday Evening')
EMPLOYEE_QUESTIONNAIRE_TUESDAY_DAYTIME = _(u'Tuesday Daytime')
EMPLOYEE_QUESTIONNAIRE_TUESDAY_EVENING = _(u'Tuesday Evening')
EMPLOYEE_QUESTIONNAIRE_WEDNESDAY_DAYTIME = _(u'Wednesday Daytime')
EMPLOYEE_QUESTIONNAIRE_WEDNESDAY_EVENING = _(u'Wednesday Evening')
EMPLOYEE_QUESTIONNAIRE_THURSDAY_DAYTIME = _(u'Thursday Daytime')
EMPLOYEE_QUESTIONNAIRE_THURSDAY_EVENING = _(u'Thursday Evening')
EMPLOYEE_QUESTIONNAIRE_FRIDAY_DAYTIME = _(u'Friday Daytime')
EMPLOYEE_QUESTIONNAIRE_FRIDAY_EVENING = _(u'Friday Evening')
EMPLOYEE_QUESTIONNAIRE_SATURDAY_DAYTIME = _(u'Saturday Daytime')
EMPLOYEE_QUESTIONNAIRE_SATURDAY_EVENING = _(u'Saturday Evening')
EMPLOYEE_QUESTIONNAIRE_SUNDAY_DAYTIME = _(u'Sunday Daytime')
EMPLOYEE_QUESTIONNAIRE_SUNDAY_EVENING = _(u'Sunday Evening')
### Compensation
EMPLOYEE_QUESTIONNAIRE_COMPENSATION_TYPE = _(u'Compensation')
EMPLOYEE_QUESTIONNAIRE_HOURLY_WAGE = _(u'Hourly Wage')
EMPLOYEE_QUESTIONNAIRE_ANNUALY_WAGE = _(u'Annualy Wage')
EMPLOYEE_QUESTIONNAIRE_PRODUCTION = _(u'Production')
EMPLOYEE_QUESTIONNAIRE_COLLECTION = _(u'Colleciton')
### Experience
EMPLOYEE_QUESTIONNAIRE_EXPERIENCE_YEARS = _(u'Years of Experience')
### Education
EMPLOYEE_QUESTIONNAIRE_DENTAL_SCHOOL = _(u'Dental School attended')
EMPLOYEE_QUESTIONNAIRE_GRADUATION_YEAR = _(u'Year of Graduation')
### Visa
EMPLOYEE_QUESTIONNAIRE_VISA = _(u'Do you have a US visa?')
### Specific Strengths
EMPLOYEE_QUESTIONNAIRE_SPECIFIC_STRENGTHS = _(u'Please list specific strengths')
### Visibility
EMPLOYEE_QUESTIONNAIRE_IS_PRIVATE = _(u'Make questionnaire private')
EMPLOYEE_QUESTIONNAIRE_IS_PRIVATE_HELP_TEXT = _(
    u'Selecting this option will '
    u'hide your questionnaire from public view and it be only accesible by you.'
)
EMPLOYEE_QUESTIONNAIRE_VERBOSE_NAME = _(u'Employee Questionnaire')
EMPLOYEE_QUESTIONNAIRE_VERBOSE_NAME_PLURAL = _(u'Employee Questionnaires')

# EmployeeQuestionnaire.distance choices
DISTANCE_CHOICES_1 = _(U'Any distance')
DISTANCE_CHOICES_2 = _(U'Up to 5 miles')
DISTANCE_CHOICES_3 = _(U'Up to 10 miles')
DISTANCE_CHOICES_4 = _(U'Up to 20 miles')
DISTANCE_CHOICES_5 = _(U'Up to 30 miles')
DISTANCE_CHOICES_6 = _(U'Up to 40 miles')
DISTANCE_CHOICES_7 = _(U'Up to 50 miles')
DISTANCE_CHOICES_8 = _(U'Up to 60 miles')
DISTANCE_CHOICES_9 = _(U'Up to 75 miles')
DISTANCE_CHOICES_10 = _(U'Up to 100 miles')
DISTANCE_CHOICES_11 = _(U'Up to 150 miles')
DISTANCE_CHOICES_12 = _(U'Up to 200 miles')

# EmployeeQuestionnaire.schedule_type choices
SCHEDULE_TYPE_CHOICES_PART_TIME = _(u'Part Time')
SCHEDULE_TYPE_CHOICES_FULL_TIME = _(u'Full Time')

# EmployeeQuestionnaire.hourly_wage choices
HOURLY_WAGE_CHOICES_1 = _(u'$10-15')
HOURLY_WAGE_CHOICES_2 = _(u'$16-25')
HOURLY_WAGE_CHOICES_3 = _(u'$26-35')
HOURLY_WAGE_CHOICES_4 = _(u'$36-45')
HOURLY_WAGE_CHOICES_5 = _(u'$46-55')
HOURLY_WAGE_CHOICES_6 = _(u'$56-65')
HOURLY_WAGE_CHOICES_7 = _(u'$66-75')
HOURLY_WAGE_CHOICES_8 = _(u'$76-85')
HOURLY_WAGE_CHOICES_9 = _(u'$86-95')
HOURLY_WAGE_CHOICES_10 = _(u'$95-100')
HOURLY_WAGE_CHOICES_11 = _(u'>$100')

# EmployeeQuestionnaire.annualy_wage choices
ANNUALY_WAGE_CHOICES_1 = _(u'$0-10,000 / year')
ANNUALY_WAGE_CHOICES_2 = _(u'$10,000-20,000 / year')
ANNUALY_WAGE_CHOICES_3 = _(u'$20,000-30,000 / year')
ANNUALY_WAGE_CHOICES_4 = _(u'$30,000-40,000 / year')
ANNUALY_WAGE_CHOICES_5 = _(u'$40,000-50,000 / year')
ANNUALY_WAGE_CHOICES_6 = _(u'$50,000-60,000 / year')
ANNUALY_WAGE_CHOICES_7 = _(u'$60,000-70,000 / year')
ANNUALY_WAGE_CHOICES_8 = _(u'$70,000-80,000 / year')
ANNUALY_WAGE_CHOICES_9 = _(u'$80,000-90,000 / year')
ANNUALY_WAGE_CHOICES_10 = _(u'$90,000-100,000 / year')
ANNUALY_WAGE_CHOICES_11 = _(u'>$100,000 / year')

# EmployeeQuestionnaire.compensation_type choices
COMPENSATION_TYPE_CHOICES_HOURLY = _(u'Hourly Wage')
COMPENSATION_TYPE_CHOICES_SALARY = _(u'Salary')

# EmployeeQuestionnaire.experience_years choices
EXPERIENCE_YEARS_CHOICES_1 = _(u'Less than one year')
EXPERIENCE_YEARS_CHOICES_2 = _(u'1 year')
EXPERIENCE_YEARS_CHOICES_3 = _(u'2 years')
EXPERIENCE_YEARS_CHOICES_4 = _(u'3 years')
EXPERIENCE_YEARS_CHOICES_5 = _(u'4 years')
EXPERIENCE_YEARS_CHOICES_6 = _(u'5 years')
EXPERIENCE_YEARS_CHOICES_7 = _(u'6 years')
EXPERIENCE_YEARS_CHOICES_8 = _(u'7 years')
EXPERIENCE_YEARS_CHOICES_9 = _(u'8 years')
EXPERIENCE_YEARS_CHOICES_10 = _(u'9 years')
EXPERIENCE_YEARS_CHOICES_11 = _(u'10 years')
EXPERIENCE_YEARS_CHOICES_12 = _(u'10 - 15 years')
EXPERIENCE_YEARS_CHOICES_13 = _(u'15 - 20 years')
EXPERIENCE_YEARS_CHOICES_14 = _(u'> 20 years')

# EmployeeQuestionnaire.graduation_year choices
GRADUATION_YEAR_CHOICES_1 = _(u'1990')
GRADUATION_YEAR_CHOICES_2 = _(u'1991')
GRADUATION_YEAR_CHOICES_3 = _(u'1992')
GRADUATION_YEAR_CHOICES_4 = _(u'1993')
GRADUATION_YEAR_CHOICES_5 = _(u'1994')
GRADUATION_YEAR_CHOICES_6 = _(u'1995')
GRADUATION_YEAR_CHOICES_7 = _(u'1996')
GRADUATION_YEAR_CHOICES_8 = _(u'1997')
GRADUATION_YEAR_CHOICES_9 = _(u'1998')

# EmployeeQuestionnaire.job_position
JOB_POSITION_CHOICES_1 = _(u'Dentist')
JOB_POSITION_CHOICES_2 = _(u'Dental Hygienist')
JOB_POSITION_CHOICES_3 = _(u'Dental Assistant')
JOB_POSITION_CHOICES_4 = _(u'Office Manager')
JOB_POSITION_CHOICES_5 = _(u'Office Personnel')
JOB_POSITION_CHOICES_6 = _(u'Lab Technician')

# Resume's strings
RESUME_USER = _(u'User')
RESUME_CV_FILE = _(u'Please upload your résumé here')
RESUME_CV_FILE_HELP_TEXT = _(u'Allowed formats: DOC, DOCX, PDF. '
    u'Files cannot exceed 1MB in size.')
RESUME_VERBOSE_NAME = _(u'Résumé')
RESUME_VERBOSE_NAME_PLURAL = _(u'Résumés')

# Admin strings
ADMIN_PERSONAL_INFO = _(u'Personal Info')
ADMIN_JOB_POSITION = _(u'Job Position you\'re looking for')
ADMIN_PRACTICE_TYPE = _(u'Type of Practice')
ADMIN_PATIENTS_PAYMENT_METHOD = _(u'Patients\' Method of Payment')
ADMIN_LOCATION = _(u'Location')
ADMIN_SCHEDULE_TYPE = _(u'Type of schedule required')
ADMIN_COMPENSATION = _(u'Compensation')
ADMIN_EXPERIENCE = _(u'Experience')
ADMIN_EDUCATION = _(u'Education')
ADMIN_VISA = _(u'Visa')
ADMIN_SPECIFIC_STRENGTHS = _(u'Specific Strengths')
ADMIN_VISIBILITY = _(u'Visibility')

# QuestionnaireForm Errors
QUESTIONNAIRE_FORM_HOURLY_WAGE_ERROR = _(u'Please select an hourly wage.')
QUESTIONNAIRE_FORM_ANNUALY_WAGE_ERROR = _(u'Please select an annualy wage.')
QUESTIONNAIRE_FORM_INCOMPLETE_FORM_ERROR = _(u'You have not filled out all ' \
    u'the fields yet. For more accurate Job results please fill out all the ' \
    u'fields. You can also do so later in your profile page.')

# Employee's contact message subject
EMPLOYEE_CONTACT_SUBJECT = _(u'Interested in your Job Posting')
