from celery import shared_task
import requests
from SRT import SRT
from SRT import SeatType
from .forms import TrainSearchForm, SrtAccountForm
import json
import requests




@shared_task
def add(x, y):
    return x + y



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





@shared_task
def excute_mecro(reservation_info):
            
            srt_id = reservation_info['srt_id']
            srt_pw = reservation_info['srt_pw']
            dep = reservation_info['dep']
            arr = reservation_info['arr']
            dep_time_from = reservation_info['dep_time_from']
            dep_time_to = reservation_info['dep_time_to']
            date = reservation_info['date']
            receiveNos = reservation_info['receiveNos']

            srt = SRT(srt_id, srt_pw)

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
            print('매크로가  종료되었습니다!')