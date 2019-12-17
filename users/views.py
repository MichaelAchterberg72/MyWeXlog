from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import CustomUserSettings
from Profile.models import Profile


from .forms import CustomUserSettingsForm, RightToSayNoForm


@login_required
def CustomUserSettingsView(request):
    user_id = request.user
    detail = CustomUserSettings.objects.get(talent=user_id)
    if detail.talent == user_id:
        form = CustomUserSettingsForm(request.POST or None, instance=detail)
        if request.method == 'POST':
            if form.is_valid():
                new = form.save(commit=False)
                new.save()
                return redirect(reverse('Profile:ProfileView', kwargs={'profile_id':user_id})+'#online')
        else:
            context = {'form': form}
            template = 'users/custom_user_settings.html'
            return render(request, template, context)
    else:
        raise PermissionDenied


@login_required
def RightToSayNoView(request):
    user_id = request.user
    detail = CustomUserSettings.objects.get(talent=user_id)
    if detail.talent == user_id:
        form = RightToSayNoForm(request.POST or None, instance=detail)
        if request.method == 'POST':
            if form.is_valid():
                new = form.save(commit=False)
                new.save()
                return redirect(reverse('Profile:ProfileView', kwargs={'profile_id':user_id})+'#online')
        else:
            context = {'form': form}
            template = 'users/right_to_say_no.html'
            return render(request, template, context)
    else:
        raise PermissionDenied
