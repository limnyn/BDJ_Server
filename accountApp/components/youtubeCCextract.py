
from urllib.parse import urlparse, parse_qs

import re, requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

def extract_channel_name(youtube_url):
    # 파싱된 URL에서 쿼리 파라미터를 추출
    parsed_url = urlparse(youtube_url)
    query_params = parse_qs(parsed_url.query)
    # 'ab_channel' 파라미터를 사용하여 채널명 추출
    channel_name = query_params.get('ab_channel', [None])[0]
    return channel_name



def caption_extract(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("meta", property="og:title")["content"]

    # video_id = '6_cFlt368XM'
    video_id = re.search(r"(?<=v=)[\w-]+", url).group(0)

    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # iterate over all available transcripts
    for transcript in transcript_list:
        # if transcript.language_code == 'ko':
        if transcript.language_code == "en":
            text_list = [line["text"] for line in transcript.fetch()]

        else:
            text_list = [line["text"] for line in transcript.translate("en").fetch()]

    channel_name = extract_channel_name(url)

    return video_id, channel_name, title, "\n".join(text_list)
