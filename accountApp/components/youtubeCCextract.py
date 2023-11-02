
from urllib.parse import urlparse, parse_qs


import re
from youtube_transcript_api import YouTubeTranscriptApi
from accountApp.components.video_meta_data import get_video_data


def caption_extract(url):
    pattern = r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/watch\?.*?v=|youtube\.com/watch\?.*?&v=)([a-zA-Z0-9_-]+)'

    match = re.search(pattern, url)
    if match:
        video_id = match.group(1)
        print(video_id)
    else:
        print(url,"에서 Video ID를 찾을 수 없습니다.")
        return 0, 0, 0, 0, 0, 0

        
    title, channel_name, category_id, tags, thumbnail = get_video_data(video_id)

    # video_id = '6_cFlt368XM'
    # video_id = re.search(r"(?<=v=)[\w-]+", url).group(0)
    
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # iterate over all available transcripts
    for transcript in transcript_list:
        # if transcript.language_code == 'ko':
        if transcript.language_code == "en":
            text_list = [line["text"] for line in transcript.fetch()]

        else:
            text_list = [line["text"] for line in transcript.translate("en").fetch()]

    
    # print(title,video_id, url)
    return video_id, channel_name, title, "\n".join(text_list), category_id, tags, thumbnail


