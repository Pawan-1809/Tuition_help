# Views aur business logic idhar hai bhai

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatThread, Message
from apps.accounts.models import TutorProfile
from django.db.models import Count

@login_required
def chat_inbox(request):
    threads = request.user.chat_threads.all()
    return render(request, 'chat/inbox.html', {'threads': threads})

@login_required
def chat_with_tutor(request, tutor_id):
    tutor_profile = get_object_or_404(TutorProfile, id=tutor_id)
    tutor_user = tutor_profile.user

    thread = ChatThread.objects.annotate(
        c=Count('participants')
    ).filter(c=2).filter(
        participants=request.user
    ).filter(
        participants=tutor_user
    ).first()

    if not thread:
        thread = ChatThread.objects.create()
        thread.participants.add(request.user, tutor_user)

    return redirect('chat:room', thread_id=thread.id)

@login_required
def chat_room(request, thread_id):
    thread = get_object_or_404(request.user.chat_threads, id=thread_id)
    messages = thread.messages.all().order_by('created_at')
    
    other_user = thread.participants.exclude(id=request.user.id).first()

    return render(request, 'chat/room.html', {
        'thread': thread,
        'messages': messages,
        'other_user': other_user
    })
