from flask import Flask, render_template, request, redirect, jsonify, session, url_for
import mysql.connector
from config import Config #DB 정보 저장된 파일일

app = Flask(__name__)



app.config.from_object(Config)

#세션 시크릿 키 
app.secret_key = app.config['SESSION_KEY']

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
    if session:
        #DB연결
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True) 

        #검색조건(post_query) 받아오기
        query_type = request.form.get('query_type')
        query_content = request.form.get('query_content')
        

        #검색조건에 맞게 sql질의
        if query_content:    
            if query_type=="title":
                sql = 'SELECT postId, postTitle, DATE(createdTime) AS createdTime FROM post WHERE postTitle LIKE "%' + query_content + '%"'
            elif query_type=="content":
                sql = 'SELECT postId, postTitle, DATE(createdTime) AS createdTime FROM post WHERE postContent LIKE "%' + query_content + '%"'
            else:
                sql = 'SELECT postId, postTitle, DATE(createdTime) AS createdTime FROM post WHERE postTitle LIKE "%' + query_content + '%" or postContent LIKE "%' + query_content + '%"'
        else:
            sql='select postId, postTitle, date(createdTime) AS createdTime from post'
        
        #sql질의 결과 담기
        cursor.execute(sql)  
        sql_select = cursor.fetchall()  #리스트에 데이터 담기, 한 리스트요소 = 딕셔너리
        sql_count = len(sql_select)


        # DB 연결 종료
        cursor.close()
        connection.close()  

        return render_template('post.html', post_cnt=sql_count, post_list=sql_select, query_type=query_type, query_content=query_content)  # HTML 템플릿에 데이터 전달  
    else:
        return redirect(url_for('login'))




@app.route('/post/<int:post_id>')
def post_detail(post_id):
    if session:
        #DB연결
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        sql = ('SELECT postId, postTitle, postContent, createdTime, lastModifiedTime '
            'FROM post WHERE postId = ' + str(post_id))
        cursor.execute(sql)  
        sql_select = cursor.fetchall()
        sql_select = sql_select[0]

        return render_template('post_detail.html', post=sql_select)
    else:
        return redirect(url_for('login'))




@app.route('/post/create', methods=['GET', 'POST'])
def post_create():
    if session:
        #DB연결
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # 작성 글 내용 받아오기
        create_title = request.form.get('create_title')
        create_content = request.form.get('create_content')
        user_id = session['user_id']

        if request.method == 'POST':
            if create_title and create_content:
                state = "create"
                sql = (
                    'INSERT INTO post (userId, postTitle, postContent) '
                    'VALUES ("' + user_id + '", "' + create_title + '", "' + create_content + '");'
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
    
    else:
        return redirect(url_for('login'))




@app.route('/post/update/<int:post_id>', methods=['GET', 'POST'])
def post_update(post_id):
    if session:
        #DB연결
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        sql = ('SELECT postId, postTitle, postContent, createdTime, lastModifiedTime '
            'FROM post WHERE postId = ' + str(post_id))
        cursor.execute(sql)  
        sql_select = cursor.fetchall()
        sql_select = sql_select[0]

        update_title = request.form.get('update_title')
        update_content = request.form.get('update_content')

        if request.method == 'POST':
            if update_title and update_content:
                state = "update"
                sql = ('UPDATE post '
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
    
    else:
        return redirect(url_for('login'))




@app.route('/post/delete/<int:post_id>', methods=['GET', 'POST'])
def post_delete(post_id):
    if session:
        #DB연결
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        state = "delete_check"    

        if request.method == 'POST':
            delete_yn = request.form.get('delete_yn')
            print(delete_yn)
            if delete_yn == "yes":
                state = "delete"
                sql = 'DELETE FROM post WHERE postId = ' + str(post_id)
                cursor.execute(sql)  
                connection.commit()
                return render_template('next.html',state=state)

        # DB 연결 종료
        cursor.close()
        connection.close()  

        return render_template('next.html', state=state, post_id=post_id)
    
    else:
        return redirect(url_for('login'))





@app.route('/login', methods=['GET', 'POST'])
def login():
    if session:
        return redirect(url_for('my_page'))
    return render_template('login.html')




@app.route('/login_chk', methods=['POST'])
def login_chk():
    #DB연결
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    user_id = request.form.get('user_id')
    user_pw = request.form.get('user_pw')

    sql = (
        'SELECT count(*) AS cnt FROM user WHERE userId = "' + user_id + '" AND userPw = "' + user_pw + '"'
    )
    cursor.execute(sql)
    sql_cnt = cursor.fetchone()
    sql_cnt = sql_cnt['cnt']

    if sql_cnt == 1:
        session['user_id'] = user_id #세션 만들기
        print("login success")
        print(session['user_id'])
        return jsonify({'login_chk': 'success'})
    else:
        print("login fail")
        return jsonify({'login_chk': 'fail', "login_msg": "아이디 또는 비밀번호가 잘못되었습니다."})





@app.route('/my_page') #, methods=['GET', 'POST'])
def my_page():
    if session:
        return render_template('my_page.html')
    else:
        return redirect(url_for('login'))




@app.route('/logout') #, methods=['GET', 'POST'])
def logout():
    #이미 로그아웃인데, 로그아웃 페이지에 접근한 경우
    if not session['user_id']:
        #홈으로 리다이렉션
        return redirect(url_for('home'))
    session.clear()  # 세션 삭제
    return redirect(url_for('home'))




@app.route('/') #, methods=['GET', 'POST'])
@app.route('/home') #, methods=['GET', 'POST'])
def home():
    return render_template('home.html')





@app.route('/join', methods=['GET', 'POST'])
def join():

    #DB연결
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == 'POST':
        #form 내용 가지고오기
        user_id = request.form.get('user_id')
        user_email = request.form.get('user_email')
        user_name = request.form.get('user_name')
        user_pw = request.form.get('user_pw')
        user_orgn = request.form.get('user_orgn')
        user_major = request.form.get('user_major')

        if all([user_id,user_email,user_name,user_pw,user_orgn,user_major]):
            state = "join"
            sql = (
                'INSERT INTO user (userId, userEmail, userName, userPw, userOrgn, userMajor) '
                'VALUES ("' + user_id + '", "' + user_email + '", "' + user_name + '", "' + user_pw + '", "' + user_orgn + '", "' + user_major + '");'
            )
            cursor.execute(sql)
            connection.commit()
            return render_template('next.html',state=state)

    return render_template('join.html')




@app.route('/id_chk', methods=['POST']) #'GET', 
def id_chk():
    user_id = request.form.get('user_id')

    #DB연결
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    #id 중복 확인 쿼리
    sql = 'SELECT count(*) AS cnt FROM user WHERE userId = "' + user_id + '"'
    cursor.execute(sql)
    sql_cnt = cursor.fetchone()
    sql_cnt = sql_cnt['cnt']

    if sql_cnt == 0:
        return jsonify({'id_chk': 'not_exists', "id_msg": "사용 가능한 아이디입니다."})
    else:
        return jsonify({'id_chk': 'exists', "id_msg": "사용할 수 없는 아이디입니다. 다른 아이디를 입력해 주세요."})




@app.route('/test')
def test():
    state = "join"
    return render_template('next.html',state=state)




if __name__ == '__main__':
    app.run(debug=True)
