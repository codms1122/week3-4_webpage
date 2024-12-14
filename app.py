from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# 임시 데이터 저장
posts = []


@app.route('/post')
def post_list():
    return render_template('post.html')


if __name__ == '__main__':
    app.run(debug=True)
