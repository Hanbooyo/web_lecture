from flask import Flask, render_template, request, jsonify
import openai

# 발급받은 API 키 설정
OPENAI_API_KEY = "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" # 발급받은 api 키 작성

# openai API 키 인증
openai.api_key = OPENAI_API_KEY

# 모델 - GPT 3.5 Turbo 선택
model = "gpt-3.5-turbo"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.form['chat_input']

    # 질문 작성하기
    messages = [
        {
            "role": "user", #
            "content": message
        }
    ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['text']

    return jsonify({'message': answer})

@app.route('/get-response', methods=['POST'])
def get_bot_response():
    chat_input = request.form['chat_input']

    # 메시지 설정하기
    messages = [
        {"role": "system", "content": "You are a helpful assistant. You speak only in Korean. and you never speak with codebox or Hyper Text Language or something. only just text."},
        {"role": "user", "content": chat_input}      
        ]

    # ChatGPT API 호출하기
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    print(response)
    answer = response['choices'][0]['message']['content']
    print(answer)
    return jsonify({'bot_response': answer})


if __name__ == '__main__':
    app.run(debug=True)

