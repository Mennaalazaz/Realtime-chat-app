from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Room, Message

# Create your views here.
def home(request):
    return render(request, 'index.html')

def room(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return render(request, 'index.html', {'error': 'Room does not exist'})
    
    return render(request, 'room.html', {
        'room_name': room_name,
        'username': request.GET.get('username')
    })

# helper function to check if the room exists or not, if it exists then redirect to the room else create a new room and redirect to the room
def checkview(request):
    room_name = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room_name).exists():
        return redirect('/' + room_name + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room_name)
        new_room.save()
        return redirect('/' + room_name + '/?username=' + username)
    
# helper function to send message to the database
def sendMessage(request):
    if request.method == "POST":

        message = request.POST.get('message')
        username = request.POST.get('username')
        room_name = request.POST.get('room_name')

        if not message:
            return JsonResponse({'error': 'No message provided'}, status=400)
        
        if not username:
            return JsonResponse({'error': 'No username provided'}, status=400)
        
        if not room_name:
            return JsonResponse({'error': 'No room_name provided'}, status=400)

        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return JsonResponse({'error': 'Room does not exist'}, status=404)

        Message.objects.create(room=room, username=username, content=message)

        return JsonResponse({'status': 'Message sent'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# helper function to get messages from the database
def getMessages(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)
    
    messages = Message.objects.filter(room=room).order_by('timestamp')

    data = []
    for message in messages:
        data.append({
            'username': message.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime("%H:%M")
        })
    return JsonResponse({'messages': data})
