# project/views.py
import datetime
from django.shortcuts import render 
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication



from accountApp.components.cc_to_text import cc_to_txt

from accountApp.components.youtubeCCextract import caption_extract
from summarizer import Summarizer

import time

from accountApp.models import Summary

@api_view(['POST'])  # POST 요청만 허용
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTTokenUserAuthentication,))
def summary_from_url(request):
    if request.method == 'POST':

        post_email = request.data.get('email')
        print(f"summary요청 from {post_email}")
        # 사용자로부터 받은 데이터 (예시)
        url_link = request.data.get('url')

        #여기에 자막다운로드 기능 추가하기
        video_id, channel_name, title, text , categoryId, tags= caption_extract(url_link)
        
        subtitles = cc_to_txt(text)

        start_time = time.time()
        model = Summarizer()
        result = model(subtitles, min_length=60)
        full = "".join(result)
        end_time = time.time()
        bert_time = round(end_time - start_time, 1)        

        summary_obj = Summary(user_email=post_email, video_id=video_id, channel_name=channel_name, title=title, summary=full, created_at =datetime.datetime.now())
        summary_obj.save()
        print(f'summary fin!, 요약 소요 시간 : {bert_time}초')

        # 응답 처리
        return JsonResponse({'message': 'Data sent and response received successfully', 'channel_name':channel_name, 'title':title, 'summary': full, 'video_id': video_id, 'categoryId': categoryId, 'tags':tags, 'bert_time': bert_time})


    return JsonResponse({'message': 'POST method required'}, status=400)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTTokenUserAuthentication,))
def summary_from_text(request):
    if request.method == 'POST':
        # 사용자로부터 받은 데이터 (예시)
        text = request.data.get('source_text')


        start_time = time.time()
        model = Summarizer()
        result = model(text, min_length=60)
        end_time = time.time()
        bert_time = round(end_time - start_time, 1)
        
        print(f'summary fin!, 요약 소요 시간 : {bert_time}초')

        # 응답 처리
        return JsonResponse({'message': 'Data sent and response received successfully', 'summary': result, 'bert_time': bert_time})


    return JsonResponse({'message': 'POST method required'}, status=400)


@api_view(['GET'])  # POST 요청만 허용
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTTokenUserAuthentication,))
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
                'created_at': summary.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            summaries_data.append(summary_data)
        print("recent_summary 전송완료!")
        return JsonResponse({'summary_len' : len(summaries_data), 'summaries' :summaries_data})
            
        
        