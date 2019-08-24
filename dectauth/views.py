from django.shortcuts import redirect, render, get_object_or_404

from .models import Challenge
from .utils import create_user_and_login
from .forms import StartChallengeForm
from .callout_views import start_call


def start(request):
    if request.method == 'POST':
        form = StartChallengeForm(request.POST)
        if form.is_valid():
            challenge = Challenge.objects.create_challenge(
                username=form.cleaned_data['username'],
                state=request.POST.get('next', '')
            )
            if request.GET.get('callout') is not None:
                start_call(challenge)
            return redirect(challenge)
    else:
        form = StartChallengeForm()

    return render(request, 'dectauth/start.html', {
        'next': request.GET.get('next', ''),
        'form': form
    })


def challenge(request, challenge_uuid):
    challenge = get_object_or_404(Challenge, uuid=challenge_uuid)
    if challenge.solved:
        if not request.user.is_authenticated:
            create_user_and_login(request, challenge)
        if challenge.state:
            return redirect(challenge.state)
    return render(request, 'dectauth/challenge.html', {
        'challenge': challenge
    })
