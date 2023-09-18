FROM python:3.11.4

# 작업 디렉토리 설정
WORKDIR /

# 필요한 패키지 설치
COPY requirements.txt .
RUN pip install -r requirements.txt

# 소스 코드를 컨테이너로 복사
COPY . .

# 서버 실행 명령어 설정
CMD ["python", "manage.py", "runserver", "0.0.0.0:8765"]
