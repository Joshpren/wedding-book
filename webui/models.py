from django.db import models

class Entry(models.Model):
    audio_file = models.FileField(upload_to='recordings/', verbose_name='Recordings', null=True, blank=True)
    transcription = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    seconds = models.IntegerField(null=True, blank=True)

