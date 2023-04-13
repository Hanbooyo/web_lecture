# app.py
from flask import Flask, render_template
#flask에서 임포트하겠다 Flask랑 render_template
from flask import  request

import pymysql

# DB연동
db_conn = pymysql.connect(
          host= 'localhost',
          port= 3306,
          user= 'root',
          passwd= '1234',
          db='test',
          charset='UTF8'
)

print(db_conn)


#Flask객체 인스턴스 생성
app = Flask(__name__) # app이라는 플라스크 인스턴스 생성

@app.route('/') #접속하는 url
# @ => 데코레이션    
def index(): # 들어오면 실행되는 함수 
    temp1 = request.args.get('uid')  #main?uid=hby&cid=31 get 방식으로 전달
    temp2 = request.args.get('cid')

    print(temp1, temp2) #print 이후
    #화면을 뿌려줌
    return render_template('index.html') # templates 폴더를 자동인식, 절대경로 입력안해줘도됨

@app.route('/test', methods=['GET']) #기본이 get방식 
def testget():
    return render_template('posttest.html')

@app.route('/test', methods=['POST'])
def testpost():
    value = request.form['input'] #'input 이라는 이름의 값을 받음
    print(value)
    return render_template('posttest.html')

@app.route('/sqltest')
def sqltest():
        # 커서 객체 생성
    cursor = db_conn.cursor()

    query = "select * from player"

    cursor.execute(query) #query 실행

    result = []

    for i in cursor: #커서가 받아온 정보를 출력
        temp = {'player_id':i[0], 'player_name':i[1]} #받아온 자료들의 인덱스를 이용해서 담음
        result.append(temp)

    return render_template('sqltest.html', result_table = result)

@app.route('/detail')
def detailtest():
    temp = request.args.get('id')
    temp1 = request.args.get('name')
        # 커서 객체 생성
    cursor = db_conn.cursor()

    query = "select * from player where player_id = {} and player_name like '{}'".format(temp,temp1)

    cursor.execute(query) #query 실행

    result = []

    for i in cursor: #커서가 받아온 정보를 출력
        temp = {'player_id':i[0], 'player_name':i[1], 'team_name':i[2], 'height':i[-2], 'weight':i[-1]} #받아온 자료들의 인덱스를 이용해서 담음
        result.append(temp)

    return render_template('detail.html', result_table = result)



@app.route('/login')
def login():
    return render_template('login.html')


if __name__=="__main__": #scipt실행했을때 가장 먼저 실행되는 부분,
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app. run(host=  "127.0.0.1", port="5000", debug=True)