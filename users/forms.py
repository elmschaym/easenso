from django import forms
from .models import User
from captcha.fields import CaptchaField
from functools import partial






DateInput = partial(
	forms.DateInput, 
	{
		'class'    : 'form-control',
		'id'       : 'date-of-birth',
		'required' : 'True',
	}
)

class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

class SignupForm(forms.Form):
	security_questions = (
		('first_kissed', 'What is the first name of the person you first kissed?'),
		('failing_grade', 'What is the last name of the teacher who gave you your first failing grade?'),
		('wedding_reception', 'What is the name of the place your wedding reception was held?'),
		('primary_school', 'What was the name of your elementary / primary school?'),
		('sibling_live', 'In what city or town does your nearest sibling live?'),
		('time_born','What time of the day were you born? (hh:mm)'),
		('pets_name','What is your pet'+"'"+'s name?'),
		('father_born', 'In what year was your father born?'),
		('favorite', 'What is your favorite _____?')
	)
	security_questions = forms.ChoiceField(choices = security_questions,
                                   widget = forms.Select(attrs={
                                       'class' : 'form-control',
                                       'id'		: 'sec_quest'
                                   })
    )

	security_answer = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Security Answer',
				'class'       : 'form-control',
				'id' 		 : 'sec_answer',
				'required'    : 'True',
				'maxlength'	: '100'
			}
		),
	)

	firstname = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'First Name',
				'class'       : 'form-control',
				'id' 				  : 'first-name',
				'required'    : 'True',
			}
		),
	)

	middlename = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Middle Name',
				'class'       : 'form-control',
				'id' 		  : 'middle-name',
				'required'    : 'True',
			}
		),
	)

	lastname = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Last Name',
				'class'       : 'form-control',
				'id'			    : 'last-name',
				'required'    : 'True',
			}
		),
	)

	# GENDER = [
	#   ('M', 'Male'),aFi
	#   ('F', 'Female'),
	# ]

	# gender = forms.ChoiceField(
	#   label = '',
	#   choices = GENDER,
	#   widget   = forms.Select(
	#     attrs = {
	#       'placeholder' : 'Address',
	#       'class'       : 'form-control',
	#       'id'          : 'gender',
	#       'maxlength'   : 50,
	#       'type'        : 'text',
	#       'required'    : 'True',
	#       }
	#   ),
	# )

	username = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Username Desired',
				'class'       : 'form-control',
				'id'			    : 'signup-username',
				'required'    : 'True',
			}
		),
	)

	password = forms.CharField(
		widget = forms.PasswordInput(
			attrs = {
				'placeholder' : 'Enter Password',
				'class'       : 'form-control',
				'id'			    : 'signup-password',
				'required'    : 'True',
				'minlength'	: '6',
			}
		),
	)

	confirm = forms.CharField(
		widget = forms.PasswordInput(
			attrs = {
				'placeholder' : 'Re-type Password',
				'class'       : 'form-control',
				'id'			    : 'password-confirm',
				'required'    : 'True',
				'minlength'	: '6',
			}
		),
	)


	email = forms.EmailField(
		label    = '', 
		widget   = forms.TextInput(
			attrs = {
				'placeholder' : 'Email address',
				'class'       : 'form-control',
				'id'          : 'email-address',
				'type'        : 'email',
				'required'    : 'True',
			}
		),
	)

	

	mobile = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Mobile Number',
				'class'       : 'form-control',
				'id'			    : 'mobile-num',
				'required'    : 'True',
				'type'	: 'number',
			}
		),
	)

	city = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'City',
				'class'       : 'form-control',
				'id'			    : 'city',
				'required'    : 'True',
			}
		),
	)

	province = forms.CharField(
		widget = forms.TextInput(
			attrs = {
				'placeholder' : 'Province',
				'class'       : 'form-control',
				'id'			    : 'province',
				'required'    : 'True',
			}
		),
	)

	date_of_birth = forms.DateField(
    widget = forms.DateInput(
			attrs = {
				'class' : 'form-control',
				'required'    : 'True',
				'placeholder': 'Date of Birth (YYYY-MM-DD)',
				'datepicker-popup': '{{format}}',
				'ng-model' : 'dt',
				'is-open'  : 'opened',
				'min-date' : 'minDate',
				'ng-click' : 'open($event)',
				'max-date' : "maxDate",
				'datepicker-options' : 'dateoptions',
				'date-disabled' : 'disabled(date, model)',
				'ng-required'  : 'true',
				'close-text' : 'Close',
				'id' : 'date_of_birth',
			}
    ),
  )
    

	# date_of_birth = forms.DateField(
	# 	widget=DateInput()
	# )