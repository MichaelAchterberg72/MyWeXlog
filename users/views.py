from django.shortcuts import render


from .models import CustomUserSettings
from Profile.models import Profile

from .forms import CustomUserSettingsForm

# Create your views here.
def CustomUserSettingsView(request, user_id=None):
    user_id = request.user
    detail = CustomUserSettings.objects.get(talent=user_id)
    if detail.talent == request.user:
        form = CustomUserSettingsForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                instance=form.save(commit=False)
                instance.save()
                return redirect(reverse('Profile:ProfileView', kwargs={'profile_id':user_id})+'#online')
        else:
            context = {'form': form}
            template = 'users/custom_user_settings.html'
            return render(request, template, context)
    else:
        raise PermissionDenied
