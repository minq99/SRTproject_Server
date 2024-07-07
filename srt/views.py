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
from celery.result import AsyncResult
from srt.tasks import add, excute_mecro
from .models import MecroMaster
from django.utils import timezone


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
    context = {
        'mecro_cases': MecroMaster.objects.filter(client=request.user)
    }
    return render(request, 'srt/srt_mypage.html', context)





def celerytest(request):
    # 작업 시작 및 작업 ID 저장
    result = add.delay(4, 3)
    task_id = result.id
    
    # 작업의 결과를 즉시 확인하려면(블로킹 방식)
    # result = result.get(timeout=10)  # 10초 안에 작업이 완료되지 않으면 예외 발생
    
    # introduce_data 사전에 작업 ID를 저장
    introduce_data = {'task_id': task_id}
    return render(request, 'srt/celerytest.html', introduce_data)


# task_id만 있으면 확인 가능 [공통]
def check_task_result(request, task_id):
    # 작업 결과 조회
    result = AsyncResult(task_id)
    if result.state == 'SUCCESS':
        introduce_data = {'result': result.result}
    else:
        introduce_data = {'result': '작업이 아직 완료되지 않았습니다.'}
    return render(request, 'srt/celerytest.html', introduce_data)



def do_mecro(request):
    if request.method == 'POST':
        form = SrtAccountForm(request.POST)

        if form.is_valid():
            # DB에 1 건 추가
            Mecro_id = str(request.user) + '_' + str(MecroMaster.objects.filter(client = request.user).count() + 1 ).zfill(6)

            reservation_info = {
                'mecro_id': Mecro_id,
                'srt_id' : form.cleaned_data['srt_id'],
                'srt_pw' : form.cleaned_data['srt_pw'],
                'dep'  : request.session.get('departure_station'),
                'arr'  : request.session.get('arrival_station'),
                'dep_time_from'  : request.session.get('departure_time_from').replace(':','') + '00',
                'dep_time_to'  : request.session.get('departure_time_to').replace(':','') + '00',
                'date'  : request.session.get('departure_date').replace('-',''),
                'receiveNos' : '01029361595',
                }




            # DB에 1 건 추가
            Mecro_id = str(request.user) + '_' + str(MecroMaster.objects.filter(client = request.user).count() + 1 ).zfill(6)
            MecroMaster.objects.create(
                mecro_id = reservation_info['mecro_id'],
                # train_no = '',
                dep= reservation_info['dep'],
                arr = reservation_info['arr'],
                date = reservation_info['date'],
                dep_time_from = reservation_info['dep_time_from'],
                dep_time_to = reservation_info['dep_time_to'],
                # task_ID = task_id,
                first_seat_YN = 'N',
                client = request.user,   # id 로 저장됨 
                status= '1' ,
                )

            # 비동기 처리 시작
            excute_mecro.delay(reservation_info)

            # # MecroMaster DB에 task_id 저장해야 함
            # task_id = TASK.id
            # MecroMaster.objects.filter(mecro_id = Mecro_id).update(task_ID=task_id)


            # introduce_data = {'task_id': task_id}

        return redirect('srt:mypage')




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


