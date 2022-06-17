from django import forms
from .models import Protocol, Process
from durationwidget.widgets import TimeDurationWidget
 
 
class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ('title', 'abst')

class ProcessForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub'].widget = forms.HiddenInput()
        self.fields['rank'].widget = forms.HiddenInput()
    class Meta:
        model = Process
        fields = ('title','content','time','sub','rank')
        widgets = {'time': TimeDurationWidget(show_days=True, 
                                              show_hours=True, 
                                              show_minutes=True, 
                                              show_seconds=False)}
