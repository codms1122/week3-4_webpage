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


@app.route('/post', methods=['GET', 'POST'])
def post():
    #DB연결
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True) 


    #검색조건(post_query) 받아오기
    query_type = request.form.get('query_type')
    query_content = request.form.get('query_content')
    

    #검색조건에 맞게 sql질의
    if query_content:    
        if query_type=="title":
            sql = 'SELECT postId, postTitle, DATE(createdTime) AS createdTime FROM testpost WHERE postTitle LIKE "%' + query_content + '%"'
        elif query_type=="content":
            sql = 'SELECT postId, postTitle, DATE(createdTime) AS createdTime FROM testpost WHERE postContent LIKE "%' + query_content + '%"'
        else:
            sql = 'SELECT postId, postTitle, DATE(createdTime) AS createdTime FROM testpost WHERE postTitle LIKE "%' + query_content + '%" or postContent LIKE "%' + query_content + '%"'
    else:
        sql='select postId, postTitle, date(createdTime) AS createdTime from testpost'
    
    #sql질의 결과 담기
    cursor.execute(sql)  
    sql_select = cursor.fetchall()  #리스트에 데이터 담기, 한 리스트요소 = 딕셔너리
    sql_count = len(sql_select)


    # DB 연결 종료
    cursor.close()
    connection.close()  

    return render_template('post.html', post_cnt=sql_count, post_list=sql_select, query_type=query_type, query_content=query_content)  # HTML 템플릿에 데이터 전달  


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    #DB연결
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    sql = ('SELECT postId, postTitle, postContent, createdTime, lastModifiedTime '
           'FROM testpost WHERE postId = ' + str(post_id))
    cursor.execute(sql)  
    sql_select = cursor.fetchall()
    sql_select = sql_select[0]

    return render_template('post_detail.html', post=sql_select)
    

@app.route('/post/create', methods=['GET', 'POST'])
def post_create():
    #DB연결
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # 작성 글 내용 받아오기
    create_title = request.form.get('create_title')
    create_content = request.form.get('create_content')

    if request.method == 'POST':
        if create_title and create_content:
            state = "create"
            sql = (
                'INSERT INTO testpost (postTitle, postContent) '
                'VALUES ("' + create_title + '", "' + create_content + '");'
            )
            cursor.execute(sql)
            connection.commit()
            return render_template('next.html',state=state)
        else:
            errormsg="emptyFound"
            return render_template('post_create.html',errormsg=errormsg)


    # DB 연결 종료
    cursor.close()
    connection.close()  

    return render_template('post_create.html')







@app.route('/post/update/<int:post_id>', methods=['GET', 'POST'])
def post_update(post_id):
    #DB연결
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    sql = ('SELECT postId, postTitle, postContent, createdTime, lastModifiedTime '
           'FROM testpost WHERE postId = ' + str(post_id))
    cursor.execute(sql)  
    sql_select = cursor.fetchall()
    sql_select = sql_select[0]


    update_title = request.form.get('update_title')
    update_content = request.form.get('update_content')

    if request.method == 'POST':
        if update_title and update_content:
            state = "update"
            sql = ('UPDATE testpost '
                   'SET postTitle = "'+ update_title +'", postContent = "'+ update_content +'", lastModifiedTime = NOW() '
                   'WHERE postId = ' + str(post_id))
            cursor.execute(sql)
            connection.commit()
            return render_template('next.html',state=state)
        else:
            errormsg="emptyFound"
            return render_template('post_update.html', post=sql_select, errormsg=errormsg)
        

    # DB 연결 종료
    cursor.close()
    connection.close()  

    return render_template('post_update.html', post=sql_select)






@app.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
def post_delete(post_id):
    #DB연결
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    state = "delete_check"    

    if request.method == 'POST':
        delete_yn = request.form.get('delete_yn')
        print(delete_yn)
        if delete_yn == "yes":
            state = "delete"
            sql = 'DELETE FROM testpost WHERE postId = ' + str(post_id)
            cursor.execute(sql)  
            connection.commit()
            return render_template('next.html',state=state)


    # DB 연결 종료
    cursor.close()
    connection.close()  

    return render_template('next.html', state=state, post_id=post_id)






if __name__ == '__main__':
    app.run(debug=True)
