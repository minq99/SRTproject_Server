from django.shortcuts import render
from SRT import SRT
from .forms import TrainSearchForm
# Create your views here.

def index(request):
    if request.method == 'POST':
        form = TrainSearchForm(request.POST)
        print(form.is_valid())

        if form.is_valid():
            departure_station = form.cleaned_data['departure_station']
            arrival_station = form.cleaned_data['arrival_station']
            departure_time_to = form.cleaned_data['departure_time_to'].strftime("%H%M%S")
            departure_time_from = form.cleaned_data['departure_time_from'].strftime("%H%M%S")
            date = form.cleaned_data['date'].strftime("%Y%m%d")
            srt = SRT("2392619471", "Han0128!!") # SRT('id','pw')
            trains = srt.search_train(departure_station, arrival_station, date, departure_time_from, departure_time_to, available_only=False) 
            
            context = {'departure_station': departure_station, 'arrival_station': arrival_station, 'departure_time_from': departure_time_from,  'departure_time_to': departure_time_to, 'date' : date, "trains" : trains}
            print(context)

            return render(request, 'srt/srt_train_list.html', context)

    else:
        form = TrainSearchForm()

    return render(request, 'srt/index.html', {'form': form})



def trainlist(request):
    # 1. 비밀번호 입력
    srt = SRT("2392619471", "Han0128!!") # SRT('id','pw')

    # 2. 출발역과 도착역 입력
    dep = '울산(통도사)'  # 출발역
    arr = '수서'   # 도착역

    # 3. 출발일 설정: : dep_time_from 부터 dep_time_to 사이에 출발합니다.
    date = '20240507'
    dep_time_from = '170000'
    dep_time_to ='191600'

    # 문자 수신인 설정:
    receiveNos = "01029361595"


    return render(request, 'srt/srt_train_list.html')




