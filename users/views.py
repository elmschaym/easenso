from django.shortcuts import render_to_response, RequestContext, HttpResponse
from users import forms
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
from users.models import User
from django.core.mail import EmailMultiAlternatives
import json
import re

SYSTEM_NAME = 'Easenso'

def signup_view(request):
	form    = forms.SignupForm()
	captcha = forms.CaptchaTestForm()

	return render_to_response(
		'includes/sign-up.html',
		{
			'system_name' : SYSTEM_NAME + ' Sign-up',
			'form'        : form,
			'captcha'		  : captcha,
		},
		RequestContext(request),
	)

@require_POST
def signup(request):
	#try:
		captcha = forms.CaptchaTestForm(request.POST)
		form    = forms.SignupForm(request.POST)

		if form.is_valid() and captcha.is_valid():

			if form.cleaned_data['password'] == form.cleaned_data['confirm'] and not User.objects.filter(email__iexact = form.cleaned_data['username']).exists() and is_characters(form.cleaned_data['username']):
				user = User(
					first_name     = form.cleaned_data['firstname'],
					middle_name    = form.cleaned_data['middlename'],
					last_name      = form.cleaned_data['lastname'],
					username       = form.cleaned_data['username'],
					security_question      = form.cleaned_data['security_questions'],
					security_answer       = form.cleaned_data['security_answer'],
					gender         = [gender for gender in request.POST['gender[]']][0],
					email          = form.cleaned_data['email'],
					password       = make_password(form.cleaned_data['password'], salt=None, hasher='default'),
					address        = form.cleaned_data['city'] + ', ' + form.cleaned_data['province'],
					contact_number = form.cleaned_data['mobile'],
					is_active      = True,
					user_type      = 'B',
					captcha        = captcha.cleaned_data['captcha'],
					date_of_birth  = form.cleaned_data['date_of_birth'],
				)

				user.save()

				subject, from_email, to_email = 'Easenso Account Validation', user.email, user.email
				text_content = ''
				html_content = "Hi %s,<br /> Thanks for signing up for Easenso!<br /> Please <a href='https://www.easenso.ph/registration/confirm_email/%s'>click this link</a> to confirm your email address. This means you will be able to reset your password if you forget it later, <br /> If you can't click the link from your email program, please copy this URL and paste it into your web browser: <br /><br /> http://www.easenso.ph/registration/confirm_email/%s <br/><br/><br/><br/><br/>If you don't want to use easenso, just ignore this message <br/><br/> To Contact Us: <br/><br/> Email: support@easenso.ph <br/><br/> Thanks!" % (user.first_name, user.email, user.email)
				message      = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
				message.attach_alternative(html_content, "text/html")
				message.send()




				data={
					'system_name' : 'One More Step!',
				}

				return render_to_response('success/confirm.html', data,RequestContext(request),)
			else:
				first_name     = form.cleaned_data['firstname']
				middle_name    = form.cleaned_data['middlename']
				last_name      = form.cleaned_data['lastname']
				username       = form.cleaned_data['username']
				gender         = [gender for gender in request.POST['gender[]']][0]
				email          = form.cleaned_data['email']
				password       = form.cleaned_data['password']
				city        = form.cleaned_data['city']
				province = form.cleaned_data['province']
				contact_number = form.cleaned_data['mobile']
				is_active      = True
				date_of_birth  = form.cleaned_data['date_of_birth']
				form    = forms.SignupForm(initial={
					'firstname': first_name,
					'username':username,
					'lastname':last_name,
					'middlename':middle_name,
					'password':password,
					'confirm':password,
					'email':email,
					'mobile':contact_number,
					'city':city,
					'province':province,
					'date_of_birth':date_of_birth,
					})
				captcha = forms.CaptchaTestForm()
				return render_to_response(
					'includes/sign-up.html',
					{
						'system_name' : SYSTEM_NAME + ' Sign-up',
						'form'        : form,
						'captcha'		  : captcha,
					},
					RequestContext(request),
				)
		else:

			first_name     = form.cleaned_data['firstname']
			middle_name    = form.cleaned_data['middlename']
			last_name      = form.cleaned_data['lastname']
			username       = form.cleaned_data['username']
			gender         = [gender for gender in request.POST['gender[]']][0]
			email          = form.cleaned_data['email']
			password       = form.cleaned_data['password']
			city        = form.cleaned_data['city']
			province = form.cleaned_data['province']
			contact_number = form.cleaned_data['mobile']

			date_of_birth  = form.cleaned_data['date_of_birth']
			print date_of_birth
			form    = forms.SignupForm(initial={
				'firstname': first_name,
				'username':username,
				'lastname':last_name,
				'middlename':middle_name,
				'password':password,
				'confirm':password,
				'email':email,
				'mobile':contact_number,
				'city':city,
				'province':province,
				'date_of_birth':date_of_birth,
				})
			captcha = forms.CaptchaTestForm()
			return render_to_response(
				'includes/sign-up.html',
				{
					'system_name' : SYSTEM_NAME + ' Sign-up',
					'form'        : form,
					'captcha'		  : captcha,
				},
				RequestContext(request),
			)

	#except:
	#	return HttpResponse('Oops! sorry, something went wrong in the process.')

#	return HttpResponse('Oops! sorry, error 404')

def check_username_db(request):

	username = request.GET.get('username')
	if is_characters(username):

		if User.objects.filter(username=username).exists():

			data ={ 'exist': 'exist'}
		elif username=="":
			data ={ 'exist': 'empty'}
		else:
			data ={ 'exist': 'available'}
	else:
			data ={ 'exist': 's_character'}


	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")

def is_characters(s):
        if re.match("^[a-z0-9]*$", s):
           	return True
        else:
            return False
def check_email_db(request):

	email = request.GET.get('email')
	if email=="":
		data ={ 'exist': 'none'}
	else:
		if email:
			if User.objects.filter(email=email).exists():
				data ={ 'exist': 'exists'}

			else:
				data ={ 'exist': 'not'}
		else:
			data ={ 'exist': 'not'}


	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")

def confirm_email(request, email):
	user = User.objects.get(email__iexact = email)
	if not user.is_confirmed:
		user.is_confirmed = True
		user.save()
		data={
			'system_name' : 'Congratulations!',
		}
		return render_to_response('success/success.html', data,RequestContext(request),)
	else:
		data={
			'system_name' : 'You Have Already Confirm!',
		}
		return render_to_response('success/already.html', data,RequestContext(request),)

def termsanduse(request):

	return render_to_response(
		'includes/termsanduse.html',
		{
			'system_name' : SYSTEM_NAME + ' Term and Use',
		},
		RequestContext(request),
	)
