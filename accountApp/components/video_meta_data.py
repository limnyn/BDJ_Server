import json
import requests



def get_video_data(video_id):
    with open('secret.json', 'r') as f:
        data = json.load(f)
    api_key = data['YOUTUBE_API_KEY']
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "id": video_id,
        "key": api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        print(data)
        # Check if the response contains valid data
        if "items" in data and len(data["items"]) > 0:
            title = data["items"][0]["snippet"]["title"]
            channel_name = data["items"][0]["snippet"]["channelTitle"]
            category_id = data["items"][0]["snippet"]["categoryId"]
            thumbnail = data["items"][0]["snippet"]["thumbnails"]["standard"]["url"]
            if "tags" in data["items"][0]["snippet"]:
                tags =  data["items"][0]["snippet"]["tags"]
                return title, channel_name, category_id, tags, thumbnail
            else:
                return title, channel_name, category_id, [], thumbnail
                
        else:
            return "Channel name not found for the provided video ID."

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# 231102
# thumbnail에 maxres 이미지값이 없는 경우도 있어서 thumbnail은 standard화질로 보내는 거로 변경
# standard 이미지 사이즈는 640480 사이즈로 640360이미지에 위 아래로 레터박스가 있는 형태 
# 사용할 때 잘라서 쓰도록



'''
{'kind': 'youtube#videoListResponse', 'etag': 'w9IgM5v6JZDXe0V6A5iDiD6W36k', 'items': [{'kind': 'youtube#video', 'etag': 'YtYgKEu3Rb0czSkZLC9RA0kW1R4', 'id': 'D3QUDebEats', 'snippet': {'publishedAt': '2023-09-25T12:24:55Z', 'channelId': 'UCsJ6RuBiTVWRX156FVbeaGg', 'title': '2030년 세계 GDP 3위, 인도의 야망', 'description': '0:00 ~ 5:18 G20 정상회의를 쥐고 흔든 인도\n5:18 ~ 13:59 인도의 눈치를 보는 글로벌 강국들\n13:59 ~ 화장실 1억 개 설치 완료, 미-중-인도 Big 3 가 간다?\n\n어렵고 딱딱한 경제,시사,금융 이야기를\n쉽고 유쾌하게 풀어내는\n경제/시사/이슈/잡썰 토크방송입니다.\n\n#화장실', 'thumbnails': {'default': {'url': 'https://i.ytimg.com/vi/D3QUDebEats/default.jpg', 'width': 120, 'height': 90}, 'medium': {'url': 'https://i.ytimg.com/vi/D3QUDebEats/mqdefault.jpg', 'width': 320, 'height': 180}, 'high': {'url': 'https://i.ytimg.com/vi/D3QUDebEats/hqdefault.jpg', 'width': 480, 'height': 360}, 'standard': {'url': 'https://i.ytimg.com/vi/D3QUDebEats/sddefault.jpg', 'width': 640, 'height': 480}, 'maxres': {'url': 'https://i.ytimg.com/vi/D3QUDebEats/maxresdefault.jpg', 'width': 1280, 'height': 720}}, 'channelTitle': '슈카월드', 'tags': ['슈카', '슈카월드', '경제', '시사', '이슈', '뉴스', '상식', '면접', '논술', '자소서', '취업', '주식', '증시', '주가', '시장', '자산', '투자', '금리'], 'categoryId': '23', 'liveBroadcastContent': 'none', 'defaultLanguage': 'ko', 'localized': {'title': '2030년 세계 GDP 3위, 인도의 야망', 'description': '0:00 ~ 5:18 G20 정상회의를 쥐고 흔든 인도\n5:18 ~ 13:59 인도의 눈치를 보는 글로벌 강국들\n13:59 ~ 화장실 1억 개 설치 완료, 미-중-인도 Big 3 가 간다?\n\n어렵고 딱딱한 경제,시사,금융 이야기를\n쉽고 유쾌하게 풀어내는\n경제/시사/이슈/잡썰 토크방송입니다.\n\n#화장실'}, 'defaultAudioLanguage': 'ko'}}], 'pageInfo': {'totalResults': 1, 'resultsPerPage': 1}}
'''

'''
태그 한 다섯 여섯개 까지 전달하게 하기?
'''