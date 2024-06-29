from django import forms
from .station_info import STATION_LIST

choices = [(k,k) for k in STATION_LIST]

class TrainSearchForm(forms.Form):
    departure_station = forms.ChoiceField(choices=choices, label='출발 역')
    arrival_station = forms.ChoiceField(choices=choices, label='도착 역')
    departure_time_from = forms.TimeField(label='출발 시간(시작)')
    departure_time_to = forms.TimeField(label='출발 시간(종료)')
    departure_date = forms.DateField(label='출발 일자')

class SrtAccountForm(forms.Form):
    srt_id = forms.CharField()
    srt_pw = forms.CharField()

