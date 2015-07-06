from django             import forms
from pis_system.models  import *
from helpers.helpers    import *
from django.utils.encoding import smart_unicode

DEPARTMENT = (  
                ('O', 'Other/Miscellaneous'),
                ('IT', 'Information Technology'),
                ('R',  'Registrar'),
                ('F', 'Finance'),
                ('P', 'Personnel'),
                ('BT', 'Board of Trustees'),
                ('EC', 'Executive Committee'),
                ('U', 'Utility'),
                ('L', 'Library'),
                ('C', 'Clinic'),
                ('E', 'Elementary'),
                ('HS', 'High School'),
                ('PS', 'Pre-School'),
                ('A', 'Arabic'),
                

      )
account_type = (
                    ('PE', 'Personnel Expenses'),
                    ('SA', 'School Activities'),
                    ('AE', 'Administrative Exepenses'),
                    ('GA', 'Grants, Allowances and Subsidy'),
                    ('OC', 'Other Costs')
      )

class AccountTitleChoiceField(forms.ModelChoiceField):
  def label_from_instance(self, obj):
    return smart_unicode(obj.account_title)

class voucherForm(forms.Form):


    voucherid = forms.CharField(max_length=9,
                                widget = forms.TextInput(attrs={
                                    'class'       : 'form-control',
                                    'placeholder' : 'Enter or Generate Voucher ID',
                                    'required' : 'True',
                                }),
                )

    claimant = forms.CharField(max_length=100,required=True,
                widget = forms.TextInput(attrs={
                           'class'       : 'form-control',
                           'placeholder' : 'Enter Claimant Name',
                           'required' : 'True',
                           'id' : 'claimant'
                         }
                ), 
    )
    
    purpose = forms.CharField(max_length=200,required=True,
         widget = forms.Textarea(attrs = {
      'class' : 'form-control',
      'placeholder' : 'Purpose of Expenditures',
      'required' : 'True',
      'id' : 'purpose',
      'style': 'height: 150px; width: 455px; max-height: 150px;min-width: 455px; max-width: 455px'
                  }
         ),
    )

    department = forms.ChoiceField(choices = DEPARTMENT, 
                               widget=forms.Select(attrs={
                                   'class' : 'form-control',
                                   'id' : 'department',
                                   'disabled':""
                                   }),
    )


    expense_type = AccountTitleChoiceField(queryset = ExpensesType.objects.all(), 
                               widget=forms.Select(attrs={
                                   'class' : 'form-control',
                                   'id' : 'expense_type'
                                   }),
    )

    amount = forms.CharField(max_length=100,
                          widget = forms.NumberInput(attrs={
                                     'class' : 'form-control',
                                     'required'    : 'True',
                                     'id' : 'amount',
                                     'disabled':""
                                   }), 
    )

    change = forms.CharField(max_length=100,
                          widget = forms.NumberInput(attrs={
                                     'class' : 'form-control',
                                     'required'    : 'True',
                                   }
                          ), 
    )    
    
