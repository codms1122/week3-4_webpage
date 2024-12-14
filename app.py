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
sql_select = []
#posts_cnt = []


@app.route('/post', methods=['GET', 'POST'])
def post_list():
    #DB연결
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # dictionary로 결과 반환하도록

    #검색조건(post_query) 받아오기
    query_type = request.form.get('query_type') 
    query_content = request.form.get('query_content')

    if query_content:
        if query_type=="title":
            sql = 'SELECT postId, postTitle, DATE(createdTime) AS createdTime FROM testpost WHERE postTitle LIKE "' + query_content + '"'
            
    else:
        print("검색어 없음")

    #전체 리스트 조회
    sql='select postId, postTitle, date(createdTime) AS createdTime from testpost' ##### ❗❗❗❗ DB명 변경 ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    cursor.execute(sql)  # testpost 테이블의 모든 데이터 가져오기
    sql_select = cursor.fetchall()  # posts 리스트에 데이터 담기

    #개수세기
    sql='select count(*) AS count from testpost' ### ❗❗❗❗ DB명 변경 ⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
    cursor.execute(sql)
    sql_count = cursor.fetchall()
    sql_count = sql_count[0]['count']
    
    
    # DB 연결 종료
    cursor.close()
    connection.close()  


    print("========================\n")
    print("log!! \n")
    print("Fetched posts data from DB:")
    print(sql)
    print(sql_select)
    print(sql_count)  
    print(query_type,query_content)
    print("\n========================")


    return render_template('post.html', post_cnt=sql_count, post_list=sql_select)  # HTML 템플릿에 데이터 전달  




if __name__ == '__main__':
    app.run(debug=True)
