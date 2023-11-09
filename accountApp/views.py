# project/views.py
import datetime
from django.shortcuts import render 
from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication



from accountApp.components.cc_to_text import cc_to_txt
from accountApp.components.youtubeCCextract import caption_extract
from summarizer import Summarizer

import time, sqlite3, json, openai, urllib.parse

from accountApp.models import Summary

@api_view(['POST'])  # POST 요청만 허용
@permission_classes(([]))
@authentication_classes(([]))
def summary_from_url(request):
    if request.method == 'POST':
        request_time = datetime.datetime.now()
        post_email = request.data.get('email')
        url_link = request.data.get('url')
        print(f"summary요청 from {post_email}: {url_link}")
        try:
            # URL을 파싱하고, 파싱이 실패하면 ValueError가 발생합니다.
            urllib.parse.urlparse(url_link)
        except ValueError:
            return Response({'error': '유효하지 않은 URL'}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자로부터 받은 데이터 (예시)
        #여기에 자막다운로드 기능 추가하기
        video_id, channel_name, title, text , categoryId, tags, thumbnail = caption_extract(url_link)
        if video_id == 0:
            return JsonResponse({'message': 'videoid not exsist', 'channel_name':0, 'title':0, 'summary': 0, 'video_id': 0, 'categoryId': 0, 'tags':0, 'bert_time': 0, 'thumbnail': 0})
            
        else:
            # video_id가 0이 아닌 경우, db.sqlite3에서 해당 video_id에 해당하는 레코드를 찾아서 출력
            conn = sqlite3.connect('db.sqlite3')

            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accountApp_summary WHERE video_id = ?", (video_id,))
            record = cursor.fetchone()
            conn.close()

            if record:
                # 레코드를 찾았을 경우 출력
                print(f"Summary record for video_id {video_id}: {record}")
                video_id = record[2]
                channel_name = record[3]
                title = record[4]
                result = record[5]
                return JsonResponse({'message': '이미 요약된 링크입니다', 'channel_name':channel_name, 'title':title, 'summary': result, 'video_id': video_id, 'categoryId': categoryId, 'tags':tags, 'bert_time': 0, 'thumbnail':thumbnail,'created_at':request_time})
                
            else:
                # 레코드를 찾지 못했을 경우 메시지 출력
                print(f"No summary record found for video_id {video_id}")
        subtitles = cc_to_txt(text)
        # print(subtitles)
        start_time = time.time()
        model = Summarizer()
        full = "".join(subtitles)
        
        if len(full) > 1200:
            result = model(full, min_length=60)
            quest = (
                f"User: {title}라는 제목을 가진 영상의 요약 내용인 다음 글\n[{result}]\n를 읽고 이 영상에 대한 내용을 한국어로 보고서를 작성해서 출력해줘"
            )
        else:
            result = full
            quest = (
                f"User: {title}라는 제목을 가진 영상의 스크립트 내용인 다음 글\n[{result}]\n를 읽고 이 영상에 대한 내용을 한국어로 보고서를 작성해서 출력해줘"
            )
        
        end_time = time.time()
        if len(full) == 0:
            print("bert 요약불가 링크")
        else:
            bert_time = round(end_time - start_time, 1)        

            print(f'summary fin!, 요약 소요 시간 : {bert_time}초')

            with open('secret.json', 'r') as f:
                data = json.load(f)
            openai.api_key = data['GPT_KEY']

            messages = [{"role": "user", "content": quest}]

            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)


            chat_response = completion.choices[0].message["content"].strip()
            # print(f"보고서: {chat_response}") 
            bert_time = round(end_time - start_time, 1)        
            full = chat_response
            summary_obj = Summary(user_email=post_email, video_id=video_id, channel_name=channel_name, title=title, summary=full, tags=','.join(tags), thumbnail=thumbnail, created_at =request_time)
            summary_obj.save()
            



        # 응답 처리
        return JsonResponse({'message': 'Data sent and response received successfully', 'channel_name':channel_name, 'title':title, 'summary': full, 'video_id': video_id, 'categoryId': categoryId, 'tags':tags, 'bert_time': bert_time, 'thumbnail':thumbnail, 'created_at':request_time})


    return JsonResponse({'message': 'POST method required'}, status=400)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTTokenUserAuthentication,))
def summary_from_text(request):
    if request.method == 'POST':
        # 사용자로부터 받은 데이터 (예시)
        text = request.data.get('source_text')
        request_time = datetime.datetime.now()


        start_time = time.time()
        model = Summarizer()
        if len(text) > 1200:
            result = model(text, min_length=60)
            quest = (
                f"User: 발화문을 한번 요약한 아래 스크립트를 읽고 이 발화문이 말하고자 하는 내용을 한국어로 보고서를 작성해서 출력해줘\n{result}"
            )
        else:
            result = text
            quest = (
                f"User: 아래 발화문 스크립트를 읽고 이 발화문이 말하고자 하는 내용을 한국어로 보고서를 작성해서 출력해줘\n{result}"
            )
        
        end_time = time.time()
        bert_time = round(end_time - start_time, 1)
        print(f'summary fin!, 요약 소요 시간 : {bert_time}초')
        if len(result) != 0:
            
            with open('secret.json', 'r') as f:
                data = json.load(f)
            openai.api_key = data['GPT_KEY']

            messages = [{"role": "user", "content": quest}]

            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

            end_time = time.time()
            gpt_time = round(end_time - start_time, 1)
            chat_response = completion.choices[0].message["content"].strip()
            print(f'summary fin!, 요약 소요 시간 : {gpt_time}초')
            
            return JsonResponse({'message': 'Data sent and response received successfully', 'summary': chat_response, 'bert_time': bert_time, 'created_at':request_time })
            # return JsonResponse({'message': 'Data sent and response received successfully', 'summary': result, 'bert_time': bert_time, 'created_at':request_time })
            

        # 응답 처리
        return JsonResponse({'message': '요약이 불가능한 파일입니다. 다른 파일을 선택해주세요.', 'summary': result, 'bert_time': 0})


    return JsonResponse({'message': 'POST method required'}, status=400)


@api_view(['GET'])  # POST 요청만 허용
@permission_classes(([]))
@authentication_classes(([]))
def recent_summary(request):
    if request.method == 'GET':
        
        recent_summaries = Summary.objects.order_by('-created_at')[:20] #-를 붙임 -> 역순
        
        summaries_data  = []
        for summary in recent_summaries:
            summary_data = {
                'video_id': summary.video_id,
                'channel_name' : summary.channel_name,
                'title': summary.title,
                'summary': summary.summary,
                'thumbnail': summary.thumbnail,
                'tags':summary.tags,
                'created_at': summary.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            summaries_data.append(summary_data)
        print("recent_summary 전송완료!")
        return JsonResponse({'summary_len' : len(summaries_data), 'summaries' :summaries_data})
            
        

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTTokenUserAuthentication,))
def user_summaries(request):
    if request.method == 'POST':
        my_email = request.data.get('email')
        my_user_summaries = Summary.objects.filter(user_email=my_email)
        my_summaries = []

        
        for summary in my_user_summaries:
            summary_data = {
                'video_id': summary.video_id,
                'channel_name' : summary.channel_name,
                'title': summary.title,
                'summary': summary.summary,
                'thumbnail': summary.thumbnail,
                'tags':summary.tags,
                'created_at': summary.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            my_summaries.append(summary_data)
        print("recent_summary 전송완료!")
        return JsonResponse({'summary_len' : len(my_summaries), 'summaries' :my_summaries})
            
        
        