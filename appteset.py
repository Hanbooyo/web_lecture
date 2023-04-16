from flask import Flask, render_template, request, jsonify
import openai

# 발급받은 API 키 설정
OPENAI_API_KEY = "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" # 발급받은 api 키 작성

# openai API 키 인증
openai.api_key = OPENAI_API_KEY

# 모델 - GPT 3.5 Turbo 선택
model = "text-davinci-002"

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
            "role": "당신은 친절한 상담사 입니다. 누구와 대화를 나누더라도 친절하고 성실하게 답변합니다.",
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
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"{chat_input}\n",
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = response['choices'][0]['text']
    return jsonify({'bot_response': answer})


if __name__ == '__main__':
    app.run(debug=True)

