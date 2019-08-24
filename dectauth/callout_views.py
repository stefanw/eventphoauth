from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

from .models import Challenge, KEY_LENGTH
from .utils import solve_challenge


def start_call(challenge):
    account_sid = settings.TWILIO_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    url = reverse('dectauth:challenge-callout', kwargs={
        'challenge_uuid': str(challenge.uuid)
    })
    call = client.calls.create(
        url='{host}{url}'.format(
            host=settings.SITE_URL, url=url
        ),
        to=settings.EVENTPHONE_BASE_NUMBER + challenge.username,
        from_=settings.CALLOUT_FROM
    )
    return call


@csrf_exempt
def challenge_voice_response(request, challenge_uuid):
    challenge = get_object_or_404(Challenge, uuid=challenge_uuid)

    """Respond to incoming phone calls with a menu of options"""
    # Start our TwiML response
    resp = VoiceResponse()

    # Start our <Gather> verb
    url = reverse('dectauth:challenge-callout-gather', kwargs={
        'challenge_uuid': str(challenge.uuid)
    })
    gather = Gather(num_digits=KEY_LENGTH, action=url)
    gather.say('Please enter the six digit code that is displayed.')
    resp.append(gather)

    url = reverse('dectauth:challenge-callout', kwargs={
        'challenge_uuid': str(challenge.uuid)
    })
    resp.redirect(url)

    return HttpResponse(str(resp))


@csrf_exempt
def challenge_gather_input(request, challenge_uuid):
    """Processes results from the <Gather> prompt in /voice"""

    challenge = get_object_or_404(Challenge, uuid=challenge_uuid)
    # Start our TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    digits = request.POST.get('Digits')

    if digits is not None:
        if digits == challenge.key:
            solve_challenge(challenge)
            resp.say('Correct. Thank you and have a safe ride.')
            return HttpResponse(str(resp))

    resp.say("Incorrect. Try again.")
    url = reverse('dectauth:challenge-callout', kwargs={
        'challenge_uuid': str(challenge.uuid)
    })
    resp.redirect(url)

    return HttpResponse(str(resp))
