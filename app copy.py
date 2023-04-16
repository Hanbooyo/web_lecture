# app.py
from flask import Flask, render_template
#flask에서 임포트하겠다 Flask랑 render_template
from flask import  request

import openai

# 발급받은 API 키 설정
OPENAI_API_KEY = "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"

# openai API 키 인증
openai.api_key = OPENAI_API_KEY

# 모델 - GPT 3.5 Turbo 선택
model = "gpt-3.5-turbo"

# 질문 작성하기
query = "영원한 형벌을 받는 시지포스의 모습을 현대사회인에 투영한다면 어떤 모습일까요"

# 메시지 설정하기
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant who is good at detailing."
    },
    {
        "role": "user",
        "content": query
    }
]

# ChatGPT API 호출하기
response = openai.ChatCompletion.create(
    model=model,
    messages=messages
)
answer = response['choices'][0]['message']['content']
print(answer)
z
#Flask객체 인스턴스 생성
app = Flask(__name__) # app이라는 플라스크 인스턴스 생성

@app.route('/') #접속하는 url
# @ => 데코레이션    
def index(): # 들어오면 실행되는 함수 
    print(answer)
    return render_template('chat.html') # templates 폴더를 자동인식, 절대경로 입력안해줘도됨


if __name__=="__main__": #scipt실행했을때 가장 먼저 실행되는 부분,
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app. run(host=  "127.0.0.1", port="5000", debug=True)