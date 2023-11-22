from django.shortcuts import render
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
import random
import time
from django.shortcuts import render, get_object_or_404
from pets.models import Application
from users.models import Users
from django.contrib.auth.decorators import login_required


# Create your views here.

def getToken(request):
    appId = 'c9d9fc4d712643ba9a27b8f8527ba659'
    appCertificate = 'a21099f6841c4b7c848eec13139a050f'
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token, 'uid':uid}, safe=False)

@login_required
def lobby(request, applicationId):
    application = get_object_or_404(Application, applicationId=applicationId)
    return render(request, 'videochat/lobby.html', {'application': application})

@login_required
def room(request):
    return render(request, 'videochat/room.html')