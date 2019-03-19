from django import forms
from django.forms import Form, ModelForm
from app.models import Participant, Country

class ParticipantForm(ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'gender']

class ParticipantFormFinish(ModelForm):
    class Meta:
        model = Participant
        fields = ['email', 'continent', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.none()

        if 'continent' in self.data:
            try:
                continent_id = int(self.data.get('continent'))
                self.fields['country'].queryset = Country.objects.filter(continent_id=continent_id).order_by('country')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['country'].queryset = self.instance.continent.country_set.order_by('country')



