from django.shortcuts import render, redirect
import json
from SRT import SRT
from SRT import SeatType
from .forms import TrainSearchForm, SrtAccountForm
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import time
from .station_info import STATION_LIST
import requests
# Create your views here.

from srt.tasks import add


def celerytest(request):
    result = add.delay(4, 3)
    introduce_data = {'result': result}
    return render(request, 'srt/celerytest.html', introduce_data)




def index(request):

    now = datetime.now()
    now_af_1hour = now + timedelta(hours=1)  # 현재 시간에 1시간을 추가한 값
    if request.method == 'POST':
        form = TrainSearchForm(request.POST)
        print(form.is_valid())

        if form.is_valid():
            request.session['departure_station'] = request.POST['departure_station']
            request.session['arrival_station'] = request.POST['arrival_station']
            request.session['departure_time_to'] = request.POST['departure_time_to']
            request.session['departure_time_from'] = request.POST['departure_time_from']
            request.session['departure_date'] = request.POST['departure_date']

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

    return render(request, 'srt/index.html', {'form': form, 'now': now, 'now_af_1hour': now_af_1hour, "station_list": STATION_LIST})



def beforemecro(request):
    return render(request, 'srt/srt_train_before_mecro.html')


@login_required(login_url='common:login')  # 로그인 안한사람은 함수가 실행되지 않고 login url 타도록.
def mypage(request):
    return render(request, 'srt/srt_mypage.html')


def do_mecro(request):

    if request.method == 'POST':
        form = SrtAccountForm(request.POST)


        if form.is_valid():
            srt_id = form.cleaned_data['srt_id']
            srt_pw = form.cleaned_data['srt_pw']
            print(srt_id, srt_pw)


            dep = request.session.get('departure_station')
            arr = request.session.get('arrival_station')
            dep_time_from = request.session.get('departure_time_from').replace(':','') + '00'
            dep_time_to = request.session.get('departure_time_to').replace(':','') + '00'
            date = request.session.get('departure_date').replace('-','')

            # 1. 비밀번호 입력
            srt = SRT(srt_id, srt_pw)
            print(dep," ", arr, " ",dep_time_from ," ",dep_time_to," ", date)
            # date = '20240503'
            # dep_time_from = '170000'
            # dep_time_to ='191600'

            # 문자 수신인 설정:
            receiveNos = "01029361595"


            i = 0
            flag =True
            while(flag):
                if i == 0: sendMSG(f"{dep}-> {arr} : 매크로가 시작되었습니다!", receiveNos)
                i += 1
                print(i, '번째 검색중')
                trains = srt.search_train(dep, arr, date, dep_time_from, dep_time_to, available_only=True) #  trains = srt.search_train(dep, arr, date, time)
                for train in trains:
                    if train.general_seat_state =='예약가능': 
                        try:
                            srt.reserve(train, special_seat=SeatType.GENERAL_ONLY) # 일반실 우선으로 잡기
                            print('예약되었습니다.')
                            sendMSG("[SRT 예약 승인] 10분안에 결제하세요", receiveNos)
                            flag = False
                            break
                        except:
                            print('에러가 발생했습니다.')
                            sendMSG(f"{dep}-> {arr} : 매크로중 오류가 발생하였습니다. 재시작 해주세요!  http://13.209.12.46/", receiveNos)

            # print('매크로가  종료되었습니다!')


    return render(request, 'srt/srt_mypage.html')





def sendMSG(text, receiveNos):

    url = 'https://api.sendm.co.kr/v1/sms/send'

    headers={
        # (http://13.209.12.46/)서버용 api-key: db92eeab6b79469b8cd280b6bb757cd9 -> 배포 올릴때 꼭 이 키를 사용
        "user-id" : "NA_20240415173755",
        "api-key" : "db92eeab6b79469b8cd280b6bb757cd9"
    }

    
    request_data = {
        "callerNo": "01029361595", # 발신자는 고정
        "message": text,
        "receiveNos": receiveNos
    }

    try:
        response = requests.post(url, headers= headers,  json=request_data)
        res_obj = json.loads(response.text)
        if res_obj['code'] == '200':
            print(f'문자전송 성공: {text}')
        else: 
            print(f'문자전송 실패: {res_obj}')
    except:
        print('문자전송 실패: 네트워크 오류')


