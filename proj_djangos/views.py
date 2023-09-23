from django.shortcuts import render
from .models import Topic, Entry
from.forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    """página principal do proj_django"""
    return render(request, 'proj_djangos/index.html')

@login_required
def topics(request):
    """Mostra os dados do banco de dados"""
    topics= Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'proj_djangos/topics.html', context)

@login_required
def topic(request, topic_id):
    """mostra um único tópico"""

    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'proj_djangos/topic.html', context)

@login_required
def new_topic(request):
    """Novo tópico"""
    if request.method != 'POST':
        #Nenhum dado = formulário em branco
        form = TopicForm( )
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))
    
    context = {'form': form}
    return render(request, 'proj_djangos/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Insere um assunto em um tópico"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #Nenhum dado = formulário em branco
        form = EntryForm( )
    else:
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
    
    context = {'topic':topic, 'form': form}
    return render(request, 'proj_djangos/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """edita um tópico existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'proj_djangos/edit_entry.html', context)
