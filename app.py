from flask import Flask  #Flask 사용할 수 있도록 import
app = Flask(__name__)  #Flask 인스턴스 생성

@app.route('/') #웹페이지 경로에 접속했을 때 동작할 내용 정의 
def mainPage(): #위 경로(/) 에 접속했을 때 동작할 함수
    return render_template('index.html') #index.html 반환
    
if __name__ == '__main__': #직접 실행시켰을 때,
    app.run()              #웹서버 실행