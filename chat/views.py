from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from pets.models import Application

# Create your views here.

@login_required
def home(request, applicationId):
    application = get_object_or_404(Application, applicationId=applicationId)

    if request.user.is_authenticated:
        user = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

    return render(request, 'chat/home.html', {'application':application, 'user':user})

@login_required
def room(request, room):
    username = request.GET.get('username')
    room_details = get_object_or_404(Room, name=room)
    return render(request, 'chat/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

@login_required
def checkview(request, applicationId):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

@login_required
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

@login_required
def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})