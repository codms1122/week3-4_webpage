from flask import Flask, render_template, request, redirect
import mysql.connector
from config import Config #DB 정보 저장된 파일일

app = Flask(__name__)

app.config.from_object(Config)

#DB연결 함수
def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['HOST'],       
        database=app.config['DB'],    
        user=app.config['DB_USER'],       
        password=app.config['DB_PASSWORD'] 
        
    )
    return connection



# 임시 데이터 저장
posts = []


@app.route('/post')
def post_list():
    connection = get_db_connection()  # DB 연결
    cursor = connection.cursor(dictionary=True)  # dictionary 형식으로 결과 반환

    sql='SELECT * FROM testpost' ##### ❗❗❗❗ DB명 변경 ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    cursor.execute(sql)  # testpost 테이블의 모든 데이터 가져오기
    posts = cursor.fetchall()  # 데이터 모두 가져오기

    cursor.close()
    connection.close()  # DB 연결 종료

    return render_template('post.html', post_list_data=posts)  # HTML 템플릿에 데이터 전달




if __name__ == '__main__':
    app.run(debug=True)
