import re


def split_into_sentences(text):
    # 문장을 온점(.)을 기준으로 추출하고 공백을 포함하여 나누기
    text_without_patterns = re.sub(r"\[[^\]]*\]", "", text)
    # 문장을 온점(.)을 기준으로 추출하고, 공백이 하나 이상인 경우도 처리
    sentences = re.split(r"(?<=[.!?])\s+", text_without_patterns.replace("\n", " "))
    return sentences


def cc_to_txt(text):
    # [대문자로 시작하는형식] 패턴을 제외한 나머지 부분을 추출
    text_without_patterns = re.sub(r"\[[A-Z][^\]]*\]", "", text)

    # 문장 단위로 나누기
    sentences = split_into_sentences(text_without_patterns)

    # 빈 문장 제거
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    text_result = []
    # 결과 출력
    for _, sentence in enumerate(sentences, start=1):
        # 정규식 패턴을 사용하여 여러 개의 공백을 하나의 공백으로 대체
        corrected_sentence = re.sub(r"\s+", " ", sentence)
        text_result.append(corrected_sentence)
    text_result_str = "".join(text_result)

    # with open('input/output.txt', "w", encoding="utf-8") as f:
    #     f.write(text_result_str)
    return text_result_str
