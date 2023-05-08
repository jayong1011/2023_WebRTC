# **github** #  
https://github.com/jayong1011/2023_WebRTC/tree/main/Webrtc_Cam

# 실습결과 및 평가서 제출
- 이메일: 20181612@edu.hanbat.ac.kr 
- 파일이름: 학번_이름_평가지

# **프로젝트 소개** #
2023 캡스톤 작품을 활용한 실습 및 아이디어 논의


# [개인] 실습(환경세팅) #
1. 터미널 접속 후 명령어 입력 git clone https://github.com/jayong1011/2023_WebRTC
   
   1. ![terminal](/image/img1.png) 옆에 그림에서 cd Desktop 입력
   2. ![terminal](image/img2.png ) 왼쪽 그림처럼 바탕화면 경로에서 git clone 명령어 실행
   

2. Visual Studio Code 접속
   
3. 복제한 git repository 불러오기
   1. 폴더 열기 클릭 후 복제한 Repository 불러오기 
    
4. Visual Studio Code에서 터미널 - 새 터미널 클릭

5. python -m venv venv 명령어 입력
   - .\venv\Scripts\activate 입력
    - cd Webrtc_cam
    - pip install -r requirements.txt
    - python signaling.py 
  


# 실습[서버 동작 및 결과예시] #
1. 서버 동작확인
  - 크롬에서 주소창에 localhost:8080 입력 
  - Status : ok 나오면 정상 실행 
- 
1. 실습 진행
   - signaling.py 파일에 표시한 부분 코드 작성
   - template/sample.html 파일에서 예시 그림처럼 나올 수 있도록 조건문 알고리즘 작성
   - 2000년대 이후 입학한 학생들의 학번 출력
   -  ![result](image/img5.png)
 
# [조별]아이디어 논의 
1. ## 최대 동시접속자 1000명을 수용할 수 있는 실시간 스트리밍 서비스를 만들고 싶다. 
   1. ### 위의 제시한 서비스를 만들기 위해 서버에서 고려해야 할 것
   2. ### 이 서비스를 만들기 위해 생기게 되는 문제점과 해결방안
   
