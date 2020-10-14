from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.utils.http import is_safe_url

import math
import json

from datetime import datetime


from core.decorators import corp_permission, subscription
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.db.models.functions import Greatest

from .models import (
    CorporateStaff, OrgStructure
    )
from .forms import (
    OrgStructureForm, AddStaffForm, StaffSearchForm, AdminTypeForm
)

from AppControl.models import (
    CorporateHR
)

from Profile.models import (
    BriefCareerHistory,
)

from marketplace.models import WorkLocation
from Profile.models import Profile


@login_required()
@corp_permission(1)
def staff_search(request, cor):
    '''Search in the staff_current.html'''
    qs = CorporateStaff.objects.filter(
        Q(corporate__slug=cor) & Q(hide = False) & Q(resigned = False)
        )
    form = StaffSearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = StaffSearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            results = qs.annotate(similarity=Greatest(
                TrigramSimilarity('talent__first_name', query),
                TrigramSimilarity('talent__last_name', query),
                )).filter(similarity__gt=0.3).order_by('-similarity')

    template = 'mod_corporate/staff_search.html'
    context = {'form': form, 'query': query, 'results': results,}
    return render(request, template, context)


@login_required()
@corp_permission(1)
def dashboard_corporate(request):
    usr = request.user
    corp = CorporateStaff.objects.get(talent=usr)
    company = corp.corporate
    current_staff = CorporateStaff.objects.filter(corporate=company).values_list('talent__id',flat=True)
    current_count = current_staff.count()

    potential = BriefCareerHistory.objects.exclude(talent__id__in=current_staff).filter(Q(companybranch__company=company.company) & Q(date_to__isnull=True)).count()

    template = 'mod_corporate/dashboard_corporate.html'
    context = {
        'corp': corp, 'potential': potential, 'current_count': current_count,
        }
    return render(request, template, context)


@login_required()
@corp_permission(1)
def org_structure_view(request):
    '''A view of the levels in the corporate structure'''
    usr = request.user
    corp = CorporateStaff.objects.get(talent=usr)
    structure = OrgStructure.objects.filter(corporate=corp).order_by('parent')

    template = 'mod_corporate/org_structure_view.html'
    context = {'structure': structure, 'corp': corp,}
    return render(request, template, context)


@login_required()
@corp_permission(2)
def org_structure_add(request, cor):
    '''View to capture the company structure - only corporate administrators can edit the structure '''
    corp = get_object_or_404(CorporateHR, slug=cor)

    form = OrgStructureForm(request.POST or None, fil=corp)

    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.corporate = corp
            new.save()
            return redirect(reverse('Corporate:DashCorp'))
        else:
            template = 'mod_corporate/org_structure_add.html'
            context = {'form': form, 'corp': corp,}
            return render(request, template, context)
    else:
        template = 'mod_corporate/org_structure_add.html'
        context = {'form': form, 'corp': corp,}
        return render(request, template, context)

@login_required()
@corp_permission(1)
def staff_manage(request, cor):
    '''View the people who have listed to corporate as an employer, but have not been identified as staff'''
    #logit to test if limited to a companybranch
    staff = CorporateStaff.objects.filter(corporate__slug=cor)

    staff_id = staff.values_list('talent__id', flat=True)
    print(staff_id)

    corp = CorporateHR.objects.get(slug=cor)
    potential = BriefCareerHistory.objects.filter(Q(companybranch__company=corp.company) & Q(date_to__isnull=True)).order_by('talent__last_name')

    type = list(WorkLocation.objects.all().values_list('type', flat=True))

    template = 'mod_corporate/staff_manage.html'
    context = {'potential': potential, 'corp': corp, 'staff': staff, 'type': type, 'staff_id': staff_id,}

    return render(request, template, context)

@login_required()
@corp_permission(1)
def staff_include(request, cor, tlt):
    '''Add people to the comapny staff'''
    corp = get_object_or_404(CorporateHR,slug=cor)
    staff = get_object_or_404(Profile, alias=tlt)


    form = AddStaffForm(request.POST or None)
    template = 'mod_corporate/staff_include.html'
    context = {'form': form, 'staff': staff,}

    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.talent = staff.talent
            new.corporate = corp
            new.save()
            return redirect(reverse('Corporate:StaffManage',kwargs={'cor':cor,}))
        else:
            return render(request, template, context)
    else:
        return render(request, template, context)


@login_required()
@corp_permission(1)
def staff_remove(request, cstf):
    '''Remove people from the company staff'''
    staff_qs = CorporateStaff.objects.get(slug=cstf)
    cor = staff_qs.corporate.slug
    if request.method == 'POST':

        staff_qs.resigned=True
        staff_qs.hide=True
        staff_qs.status=False
        staff_qs.save()

        return redirect(reverse('Corporate:StaffAdmn', kwargs={'cor': cor,}))


@login_required()
@corp_permission(1)
def staff_current(request, cor):
    '''Lists the current staff members'''
    corp = get_object_or_404(CorporateHR, slug=cor)
    staff = CorporateStaff.objects.filter(corporate__slug=cor).filter(Q(hide=False) | Q(resigned=False)).order_by('talent__last_name')
    staff_id = staff.values_list('talent__id')
    staff_c = staff.count()

    current = BriefCareerHistory.objects.filter(Q(companybranch__company=corp.company) & Q(talent__id__in=staff_id) & Q(date_to__isnull=True)).order_by('talent__last_name')

    template = 'mod_corporate/staff_current.html'
    context = {'current': current, 'corp': corp, 'staff_c': staff_c,}
    return render(request, template, context)


@login_required()
@corp_permission(2)
def staff_makeadmin(request, cstf):
    staff_qs = CorporateStaff.objects.get(slug=cstf)
    cor = staff_qs.corporate.slug

    if request.method == 'POST':

        staff_qs.status=True
        staff_qs.save()

        return redirect(reverse('Corporate:StaffAdmn', kwargs={'cor': cor,}))


@login_required()
@corp_permission(1)
def staff_admin(request, cor):
    '''Manages the staff (make admin, remove from staff, etc.)'''
    tlt = request.user

    staff_qs = CorporateStaff.objects.filter(corporate__slug=cor).filter(Q(hide=False) | Q(resigned=False)).order_by('talent__last_name')

    l2 = staff_qs.get(talent = tlt)

    if l2.corp_access >= 2:
        perm = 'granted'
    else:
        perm = 'denied'

    locked = staff_qs.filter(unlocked=False)

    today = timezone.now().date()
    '''at least 1 month billed for each added user'''
    for ind in locked:
        age = (today - ind.date_add).days
        if age > 32:
            ind.unlocked = True
            ind.save()
        else:
            pass

    template = 'mod_corporate/staff_admin.html'
    context = {'staff_qs':staff_qs, 'access': perm,}
    return render(request, template, context)


@login_required()
@corp_permission(1)
def admin_staff(request, cor):
    staff_qs = CorporateStaff.objects.filter(Q(corporate__slug=cor) & Q(resigned=False) & Q(hide = False)).order_by('talent__last_name')
    staff_c = staff_qs.count()
    usr = request.user
    usr_permission = staff_qs.get(talent=usr).corp_access
    #number of administrators determined by number of staff
    if staff_c <= 100:
        no_admin = 2
        no_cont = 1
    elif staff_c > 100 and staff_c < 2000:
        no_admin = 3
        no_cont = 2
    elif staff_c >=2000:
        no_admin = 2 + math.floor((staff_c-2000) / 5000)
        no_cont = 2 + math.floor((staff_c-2000) / 1500)
        if no_admin > 5:
            no_admin = 5
        if no_cont > 20:
            no_cont = 20

    admin_qs = staff_qs.filter(status=True)
    admin_c = admin_qs.filter(corp_access = 2).count()
    cont_c = admin_qs.filter(corp_access = 1).count()

    template = 'mod_corporate/admin_manage.html'
    context = {
        'admin_qs': admin_qs, 'admin_c': admin_c, 'cont_c': cont_c, 'no_admin': no_admin, 'no_cont': no_cont, 'staff_c': staff_c, 'usr_permission': usr_permission,
        }
    return render(request, template, context)


@login_required()
def admin_permission(request):

    data = json.loads(request.body)
    staffSlug = data['staffSlug']
    action = data['action']

    staff = CorporateStaff.objects.get(slug=staffSlug)

    if action == 'up':
        if staff.corp_access < 2:
            staff.corp_access += 1

    elif action == 'down':
        if staff.corp_access > 0:
            staff.corp_access -= 1

    elif action == 'remove':
        staff.corp_access = 0
        staff.status = False

    staff.save()

    return JsonResponse('Action Processed', safe=False)
