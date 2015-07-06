from django.shortcuts import render
from pis_system.forms import *
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, render_to_response, redirect, RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib import auth
from helpers.helpers import *
from finance.forms import voucherForm
from pis_system.models import (
    Vouchers,
    ExpensesType, Employee
  )


   

SYSTEM_NAME = 'Finance'

def search_voucher(request):
    type_filter = request.GET.get('voucher_search_filter')
    search = request.GET.get('search_voucher')
    print type_filter
    print search
    if type_filter == 'id_num':
        vouchers = Vouchers.objects.filter(voucher_id__contains=search)
    elif type_filter =='n_claimant':
        vouchers = Vouchers.objects.filter(name_of_claimant__istartswith=search)
    elif type_filter == 'purpose':
        vouchers = Vouchers.objects.filter(purpose_expenditures__contains=search)

   
    queries_without_page = request.GET.copy()
    if queries_without_page.has_key('page'):
        del queries_without_page['page']
    
    paginator = Paginator(vouchers, 10)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        vouchers = paginator.page(page)
    except (InvalidPage, EmptyPage):
        vouchers = paginator.page(paginator.num_pages)
    data ={
      'vouchers':vouchers,
      'query_params':queries_without_page,
      'system_name' : SYSTEM_NAME
    }
    return render(request,'./finance/index.html', data)

def index(request):
  vouchers = Vouchers.objects.all()
  queries_without_page = request.GET.copy()
  if queries_without_page.has_key('page'):
      del queries_without_page['page']
  
  paginator = Paginator(vouchers, 10)
  try: page = int(request.GET.get("page", '1'))
  except ValueError: page = 1

  try:
      vouchers = paginator.page(page)
  except (InvalidPage, EmptyPage):
      vouchers = paginator.page(paginator.num_pages)
  data ={
    'vouchers':vouchers,
    'query_params':queries_without_page,
    'system_name' : SYSTEM_NAME
  }
  return render(request,'./finance/index.html', data)

def login(request):
    form=LogInForm()
    user = request.session.get('user')
    redirect_to = '/dashboard'
    system = 'Finance Module'
    names = {
      '/dashboard':'Dashboard', 
      '/billing/student':'Billing',
      '/billing/':'Billing'
      
      }
    if user is not None and hasAccess(user['id'], 'transaction'):
          return index(request)


    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            employee = auth.authenticate(username=form.cleaned_data['userID'], password=form.cleaned_data['password'])
          
            if employee is not None and employee.is_active and hasAccess(employee.id, 'transaction'):
                request.session.set_test_cookie()
                auth.login(request,employee)
                request.session['or_number'] = 0
                request.session['user'] = {'id':employee.id, 'userID': employee.username, 'firstname':employee.first_name, 'lastname':employee.last_name}
                
                
                return index(request)
            else:
                return HttpResponseRedirect('/finance?valid=ok&has_access=no')
        else:
            return HttpResponseRedirect('/finance?valid=ok&has_access=no')        
    # if 'next' in request.GET:
    #   redirect_to = request.GET.get('next')
    #   system = names[redirect_to]
      
    return render(
                  request,
                  'login.html',
                  {
                      #'action_url': '/finance',
                      'form': form,
                      'system_name': system,
                      'valid': request.GET.get('valid', 'none'),
                      'has_access': request.GET.get('has_access', 'none')
                      
                  }
                )

def add_voucher(request):
  vForm = voucherForm()
  return render(request,'./finance/add_voucher.html', {'system_name': SYSTEM_NAME, 'vForm':vForm})

def save_voucher(request):
  vForm = voucherForm()
  voucher_id = request.GET.get('_voucher_id')
  claimant = request.GET.get('_claimant')
  purpose = request.GET.get('_purpose')
  dept = request.GET.get('_dept')
  ex_type = request.GET.get('_expense_type')
  amount = request.GET.get('_amount')
  date_now = request.GET.get('_date_now')
  user = request.user.id
  employee= Employee.objects.get(user_id=user)
  if not Vouchers.objects.filter(voucher_id=voucher_id).exists():
      voucher = Vouchers(voucher_id=voucher_id, finance_id=employee.id,name_of_claimant=claimant, purpose_expenditures=purpose, amount=amount,date_created=date_now,department=dept,expense_type_id=int(ex_type), spent=amount)
      voucher.save()

  vouchers = Vouchers.objects.get(voucher_id=voucher_id)
  expense_all = ExpensesType.objects.all()
  return render(request,'./finance/view_voucher_ajax.html', {'system_name': SYSTEM_NAME, 'vouchers':vouchers, 'expense_all':expense_all})

def delete_voucher(request):
  voucher_id = request.GET.get('_voucher_id')
  if Vouchers.objects.filter(voucher_id=voucher_id).exists():
      Vouchers.objects.get(voucher_id=voucher_id).delete()

  vouchers = Vouchers.objects.all()
  queries_without_page = request.GET.copy()
  if queries_without_page.has_key('page'):
      del queries_without_page['page']
  
  paginator = Paginator(vouchers, 10)
  try: page = int(request.GET.get("page", '1'))
  except ValueError: page = 1

  try:
      vouchers = paginator.page(page)
  except (InvalidPage, EmptyPage):
      vouchers = paginator.page(paginator.num_pages)
  data ={
    'vouchers':vouchers,
    'query_params':queries_without_page
  }
  return render(request,'./finance/index_ajax.html', data)

def get_voucher(request):
  
  voucher_id = request.GET.get('_voucher_id')
  print voucher_id

  vouchers = Vouchers.objects.get(voucher_id=voucher_id)
  expense_all = ExpensesType.objects.all()
  return render(request,'./finance/view_voucher_ajax.html', {'system_name': SYSTEM_NAME, 'vouchers':vouchers, 'expense_all':expense_all})

def save_edit_voucher(request):
  voucher_id = request.GET.get('_voucher_id')
  claimant = request.GET.get('_claimant')
  purpose = request.GET.get('_purpose')
  dept = request.GET.get('_dept')
  ex_type = request.GET.get('_expense_type')
  amount = request.GET.get('_amount')
  vouchers = Vouchers.objects.get(voucher_id=voucher_id)

  if Vouchers.objects.filter(voucher_id=voucher_id).exists():
      vouchers.name_of_claimant = claimant
      vouchers.purpose_expenditures = purpose
      vouchers.department = dept
      vouchers.expense_type_id = int(ex_type)
      vouchers.amount = float(amount)
      vouchers.spent = float(amount)-float(vouchers.change)

      vouchers.save()
  
  expense_all = ExpensesType.objects.all()
  return render(request,'./finance/view_voucher_ajax.html', {'system_name': SYSTEM_NAME, 'vouchers':vouchers, 'expense_all':expense_all})

def save_add_change(request):
  voucher_id = request.GET.get('_voucher_id')
  change = request.GET.get('_change')
  vouchers = Vouchers.objects.get(voucher_id=voucher_id)
  print change
  print change
  if Vouchers.objects.filter(voucher_id=voucher_id).exists():
      vouchers.change = float(change)
      vouchers.spent = float(vouchers.amount)-float(change)

      vouchers.save()
  
  expense_all = ExpensesType.objects.all()
  return render(request,'./finance/view_voucher_ajax.html', {'system_name': SYSTEM_NAME, 'vouchers':vouchers, 'expense_all':expense_all})

def account_title(request):
  account_titles = ExpensesType.objects.all() 
  queries_without_page = request.GET.copy()
  if queries_without_page.has_key('page'):
      del queries_without_page['page']
  
  paginator = Paginator(account_titles, 10)
  try: page = int(request.GET.get("page", '1'))
  except ValueError: page = 1

  try:
      account_titles = paginator.page(page)
  except (InvalidPage, EmptyPage):
      account_titles = paginator.page(paginator.num_pages)
  data ={
    'account_titles':account_titles,
    'query_params':queries_without_page,
    'system_name' : SYSTEM_NAME
  }
  return render(request,'./finance/account_title.html', data)    

def save_add_account(request):
  account_title = request.GET.get('_account_title')
  expense_type = request.GET.get('_expense_type')

  if not ExpensesType.objects.filter(account_title=account_title, account_type=expense_type):
      exp = ExpensesType(account_title=account_title,account_type=expense_type)
      exp.save()
  else:
      return HttpResponseRedirect('Error')
  account_titles = ExpensesType.objects.all() 
  queries_without_page = request.GET.copy()
  if queries_without_page.has_key('page'):
      del queries_without_page['page']
  
  paginator = Paginator(account_titles, 10)
  try: page = int(request.GET.get("page", '1'))
  except ValueError: page = 1

  try:
      account_titles = paginator.page(page)
  except (InvalidPage, EmptyPage):
      account_titles = paginator.page(paginator.num_pages)
  data ={
    'account_titles':account_titles,
    'query_params':queries_without_page,
    'system_name' : SYSTEM_NAME
  }
  return render(request,'./finance/account_title_ajax.html', data)  


def check_account_title(request):
    account_type = request.GET.get('_account_type')

    print account_type
    print account_type
    expense_all = ExpensesType.objects.filter(account_type=account_type)
    return render(request,'./finance/acc_title_list.html', {'expense_all': expense_all})    

def save_edit_account(request):
    account_title = request.GET.get('_account_title')
    expense_type = request.GET.get('_expense_type')
    account_id = request.GET.get('account_id')

    if ExpensesType.objects.filter(id=account_id):
        exType = ExpensesType.objects.get(id=account_id)
        exType.account_title = account_title
        exType.account_type = expense_type

        exType.save()

    account_titles = ExpensesType.objects.all() 
    queries_without_page = request.GET.copy()
    if queries_without_page.has_key('page'):
        del queries_without_page['page']
    
    paginator = Paginator(account_titles, 10)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        account_titles = paginator.page(page)
    except (InvalidPage, EmptyPage):
        account_titles = paginator.page(paginator.num_pages)
    data ={
      'account_titles':account_titles,
      'query_params':queries_without_page,
      'system_name' : SYSTEM_NAME
    }
    return render(request,'./finance/account_title_ajax.html', data)

def delete_account_title(request):
    
    account_id = request.GET.get('account_id')

    if ExpensesType.objects.filter(id=account_id):
      if not Vouchers.objects.filter(expense_type=account_id):
          ExpensesType.objects.get(id=account_id).delete()
      else:
        return HttpResponseRedirect('Error')
        

    account_titles = ExpensesType.objects.all() 
    queries_without_page = request.GET.copy()
    if queries_without_page.has_key('page'):
        del queries_without_page['page']
    
    paginator = Paginator(account_titles, 10)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        account_titles = paginator.page(page)
    except (InvalidPage, EmptyPage):
        account_titles = paginator.page(paginator.num_pages)
    data ={
      'account_titles':account_titles,
      'query_params':queries_without_page,
      'system_name' : SYSTEM_NAME
    }
    return render(request,'./finance/account_title_ajax.html', data)

def breakdown_of_accounts(request):
    data ={
      'system_name' : SYSTEM_NAME
    }
    return render(request,'./finance/breakdown_accounts_home.html', data)    