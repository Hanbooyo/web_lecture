const express = require('express');
const bodyParser = require('body-parser');
const openai = require('openai');

// 발급받은 API 키 설정
const OPENAI_API_KEY = ''; // 발급받은 api 키 작성

// openai API 키 인증
openai.api_key = OPENAI_API_KEY;

// 모델 - GPT 3.5 Turbo 선택
const model = 'gpt-3.5-turbo';

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/chat.html');
});

app.post('/chat', (req, res) => {
  const message = req.body.chat_input;

  // 질문 작성하기
  const messages = [
    {
      role: '당신은 친절한 상담사 입니다. 누구와 대화를 나누더라도 친절하고 성실하게 답변합니다.',
      content: message,
    },
  ];

  // ChatGPT API 호출하기
  openai.Completion.create(
    model: model,
    messages: messages,
  ).then(response => {
    const answer = response.choices[0].text;
    res.json({ message: answer });
  }).catch(error => {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  });
});

app.post('/get-response', (req, res) => {
  const chat_input = req.body.chat_input;

  // 메시지 설정하기
  const messages = [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: chat_input },
  ];

  // ChatGPT API 호출하기
  openai.Completion.create(
    model: model,
    messages: messages,
  ).then(response => {
    const answer = response.choices[0].message.content;
    res.json({ bot_response: answer });
  }).catch(error => {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  });
});

app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
