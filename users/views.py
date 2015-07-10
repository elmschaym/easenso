from django.shortcuts import render_to_response, RequestContext, HttpResponse
from users import forms
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
from users.models import User
from django.core.mail import EmailMultiAlternatives
import json

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
	try:
		captcha = forms.CaptchaTestForm(request.POST)
		form    = forms.SignupForm(request.POST)
		
		if form.is_valid() and captcha.is_valid():
			if form.cleaned_data['password'] == form.cleaned_data['confirm'] and not User.objects.filter(email__iexact = form.cleaned_data['username']).exists():
				user = User(
					first_name     = form.cleaned_data['firstname'],
					middle_name    = form.cleaned_data['middlename'],
					last_name      = form.cleaned_data['lastname'],
					username       = form.cleaned_data['username'],
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
				html_content = "Hi %s,<br /> Thanks for signing up for Easenso!<br /> Please <a href='http://www.easenso.ph/registration/confirm_email/%s'>click this link</a> to confirm your email address. This means you will be able to reset your password if you forget it later, which is especially important if you have a paid account!<br /> If you can't click the link from your email program, please copy this URL and paste it into your web browser: <br /><br /> http://www.easenso.ph/registration/confirm_email/%s" % (user.first_name, user.email, user.email)
				message      = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
				message.attach_alternative(html_content, "text/html")
				message.send()

				data={
					'system_name' : 'One More Step!',
				}

				return render_to_response('success/confirm.html', data,RequestContext(request),)
			else:
				return HttpResponse('Oops! sorry, username already exists.')
		else:
			return HttpResponse('Oops! sorry, something went wrong. Please fill up the form with all your valid information.')
	except:
		return HttpResponse('Oops! sorry, something went wrong in the process.')

	return HttpResponse('Oops! sorry, error 404')

def check_username_db(request):
	context = RequestContext(request)
	username = request.GET.get('username')
	print username
	print User.objects.filter(username=username).exists()
    
	if username:
		if User.objects.filter(username=username).exists():
			print 'exits'
			data ={ 'exist': True}
			
		else:
			data ={ 'exist': False}
	else:
		data ={ 'exist': False}
	
	json_response = json.dumps(data)
	return HttpResponse(json_response, content_type="application/json")


def check_email_db(request):
	context = RequestContext(request)
	email = request.GET.get('email')
	print email
	print User.objects.filter(email=email).exists()
    
	if email:
		if User.objects.filter(email=email).exists():
			print 'exits'
			data ={ 'exist': True}
			
		else:
			data ={ 'exist': False}
	else:
		data ={ 'exist': False}
	
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