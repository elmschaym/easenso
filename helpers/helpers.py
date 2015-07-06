import random
import time
from datetime import date, datetime
from django.db import connection
from django.contrib.auth.models import *

'''
 generate employee username
'''

def getTodaysdate():
    return time.strftime("%Y-%m-%d")

def genEmpUsername():
    id = time.strftime("%y") + '%s' %str(random.randint(100, 999))
    return id

def genStudId():
    id = time.strftime("%Y") + '%s' %str(random.randint(1000, 9999))
    return id

def getRequest(request, name):
    if request.method=='GET':
        return request.GET.get(name)
    if request.method=='POST':
        return request.POST.get(name)

'''
pagination limit offset update
'''    

def upload_file(destination, f):
    with open(destination + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def prev_offset(of, lm):
    if of-lm<0:
        return of
    else:
        return of-lm

def next_offset(of, lm, size):
    if of+lm>size:
        return of
    else:
        return of+lm


def get_offsets(total_rows, limit):
    offset_list = []
    pages = 0
    if total_rows%limit>0:
        pages = (total_rows//limit) + 1
    else:
        pages = (total_rows//limit)
    offset = 0
    for i in range(pages):
        offset_list.append({'page_num': (i+1),
                            'offset'  : offset})
        offset = offset + limit
    return offset_list
        
'''
user access validattion script
'''
def hasAccess(user_id, model_table):
    user = User.objects.get(id=user_id)
    print user
    if user.is_superuser:
        return True
    else:
        cursor = connection.cursor()
        cursor.execute('''SELECT auth_group.* FROM auth_group, auth_user_groups WHERE 
        auth_group.id = auth_user_groups.group_id  AND 
        auth_user_groups.user_id=%s''', [user_id])
        user_groups = cursor.fetchall()
        for grp in user_groups:
            cursor.execute('''SELECT COUNT(*) FROM group_perms_view gpv
            WHERE gpv.model=%s AND gpv.group_id=%s''',[model_table, grp[0]])
            if cursor.fetchone()[0]>0:
                return True
        return False


'''
generating cellphone prefixes
'''
def prefix(num): 
    if num<10: 
        return '09%s%s' %(0,num) 
    else:
        return '09%s' %num
        
def cell_prefixes(): 
    prefixes = []
    for x in range(5, 100):
        prefixes.append((prefix(x), prefix(x)))
    return tuple(prefixes)

def getAllowedGrades():
    grades = []
    for grade in range(75, 100):
        grades.append((grade, grade))
    return tuple(grades)

def getCurSchYear():
    today = date.today()
    return '%s-%s' %(today.year, today.year+1)

def getAllowedSchYear():
    today = date.today()
    school_year_list = []
    if today.month < 6:
        school_year_list.append('%s - %s' %(today.year-1, today.year))
        school_year_list.append('Summer %s' %(today.year))
    else:
        school_year_list.append('%s - %s' %(today.year, today.year+1))
    return school_year_list


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def getCurrSchYear():
    curr_month = int(datetime.today().month)
    curr_year = int(datetime.today().year)
    if curr_month>=5:
        return str(curr_year) + '-' + str(curr_year+1)
    else:
        return str(curr_year-1) + '-' + str(curr_year)

		
		
#quarter for old curriculum
def getCurGradingQuarter():
    month = datetime.today().month
    if month<=10 and month>=6:
        return 1
    elif month>10 and month<=1:
        return 2
    elif month>1 and month<=3:
        return 3
    else:
        return 4

def numify(val):
    if val is None:
        return 0
    else:
        return val


def getPayrollMonthStr(month, year):
    month_str = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8:'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    return "%s %s" %(month_str[month], year)


def month_format(n):
    if n<10:
        return '0'+str(n)
    else:
        return n



def getCurriculum(year_level):
    '''
    level_type is year level
    '''
    old_cur = [4, 5, 6, 7, 8, 14, 15]
    new_cur = [1, 2, 3, 9, 10, 11, 12, 13]
    '''
    if year_level in old_cur:
        return [1, 3]
    elif year_level in new_cur:
        return [2, 3]
    '''
    return [1, 2, 3]
