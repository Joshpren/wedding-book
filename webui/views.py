from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from webui.core import InputOutputSelector
from webui.models import Entry
from . import htmlfactory
import json 


selector = InputOutputSelector.InputOutputSelector()
selector.load()

def index(request):
    devices = selector.devices()
    dropdown = htmlfactory.dropdown(devices)
    entries = Entry.objects.all()
    recordingTable = htmlfactory.table(["Zeitpunkt", "Aufnahme", "Transkription", "Dauer"], [(entry.timestamp, entry.audio_file, entry.transcription, entry.seconds) for entry in entries])
    context = {
        'dropdown': dropdown,
        'recordingTable': recordingTable
    }

    return render(request, 'index.html', context=context)

@csrf_exempt
def selectDevice(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    id = body['id']
    selector.save(id)
    return HttpResponse("")