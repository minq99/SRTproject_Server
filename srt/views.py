from django.shortcuts import render, redirect
from SRT import SRT
from .forms import TrainSearchForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import time


# Create your views here.

def index(request):
    now = datetime.now()
    now_af_1hour = now + timedelta(hours=1)  # 현재 시간에 1시간을 추가한 값
    if request.method == 'POST':
        form = TrainSearchForm(request.POST)
        print(form.is_valid())

        if form.is_valid():
            departure_station = form.cleaned_data['departure_station']
            arrival_station = form.cleaned_data['arrival_station']
            departure_time_to = form.cleaned_data['departure_time_to'].strftime("%H%M%S")
            departure_time_from = form.cleaned_data['departure_time_from'].strftime("%H%M%S")
            departure_date = form.cleaned_data['departure_date'].strftime("%Y%m%d")
            srt = SRT("2392619471", "Han0128!!") # SRT('id','pw')
            trains = srt.search_train(departure_station, arrival_station, departure_date, departure_time_from, departure_time_to, available_only=False) 
            
            context = {'departure_station': departure_station, 'arrival_station': arrival_station, 'departure_time_from': departure_time_from,  'departure_time_to': departure_time_to, 'departure_date' : departure_date, "trains" : trains}
            print(context)

            return render(request, 'srt/srt_train_list.html', context)

    else:
        form = TrainSearchForm()

    return render(request, 'srt/index.html', {'form': form, 'now': now, 'now_af_1hour': now_af_1hour})



def beforemecro(request):
    return render(request, 'srt/srt_train_before_mecro.html')


@login_required(login_url='common:login')  # 로그인 안한사람은 함수가 실행되지 않고 login url 타도록.
def mypage(request):
    return render(request, 'srt/srt_mypage.html')


def do_mecro(request):
    time.sleep(5)

    print("매크로 진행중")

        
    return redirect(request, 'srt/srt_mypage.html')


