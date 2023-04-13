# app.py
from flask import Flask, render_template
#flask에서 임포트하겠다 Flask랑 render_template
from flask import  request

#Flask객체 인스턴스 생성
app = Flask(__name__) # app이라는 플라스크 인스턴스 생성

@app.route('/main') #접속하는 url
# @ => 데코레이션    
def index(): # 들어오면 실행되는 함수 
    temp1 = request.args.get('uid')  #main?uid=hby&cid=31 get 방식으로 전달
    temp2 = request.args.get('cid')

    print(temp1, temp2) #print 이후
    #화면을 뿌려줌
    return render_template('index.html') # templates 폴더를 자동인식, 절대경로 입력안해줘도됨

@app.route('/test', methods=['GET'])
def testget():
    return render_template('posttest.html')

@app.route('/test', methods=['POST'])
def testpost():
    value = request.form['input']
    print(value)
    return render_template('posttest.html')


@app.route('/login')
def login():
    return render_template('login.html')


if __name__=="__main__": #scipt실행했을때 가장 먼저 실행되는 부분,
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app. run(host=  "127.0.0.1", port="5000", debug=True)