# app.py
from flask import Flask, render_template
from flask import request
import torch
from PIL import Image
import torchvision.transforms as transforms

# 랜덤 시드 고정
torch.manual_seed(777)

# torch.nn.Module:  PyTorch의 모든 Neural Network의 Base Class
class CNN(torch.nn.Module):

    def __init__(self):
        super(CNN, self).__init__()
        # 첫번째층
        # ImgIn shape=(?, 28, 28, 1)
        #    Conv     -> (?, 28, 28, 32)
        #    Pool     -> (?, 14, 14, 32)
        self.layer1 = torch.nn.Sequential(
            torch.nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2))

        # 두번째층
        # ImgIn shape=(?, 14, 14, 32)
        #    Conv      ->(?, 14, 14, 64)
        #    Pool      ->(?, 7, 7, 64)
        self.layer2 = torch.nn.Sequential(
            torch.nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=2, stride=2))

        # 전결합층 7x7x64 inputs -> 10 outputs
        self.fc = torch.nn.Linear(7 * 7 * 64, 10, bias=True)

        # 전결합층 한정으로 가중치 초기화
        torch.nn.init.xavier_uniform_(self.fc.weight)

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.view(out.size(0), -1)   # 전결합층을 위해서 Flatten
        out = self.fc(out)
        return out


#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():

  
  return render_template('upload.html')

@app.route('/uploader', methods=[ 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']

        print(f.filename)

        f.save("./images/"+f.filename)

        output = infer("./images/"+f.filename)

        return render_template("CNN_result.html", result = output)


def infer(filename):
   # 다시불러와서 추론 해보기
    model = CNN()
    model.load_state_dict(torch.load("cnn_model.pt", map_location=torch.device('cpu')))  # cpu로 해야해서
    model.eval() #평가 모드로 설정하여야 합니다. 이 과정을 거치지 않으면 일관성 없는 추론 결과가 출력
    # 학습을 진행하지 않을 것이므로 torch.no_grad(), gradient descent를 하지마라고 명령내리는 것
    with torch.no_grad():

        # 이미지 파일 경로 설정
        img = Image.open(filename)
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1), # RGB(3D) -> Gray(2D)
            transforms.Resize((28, 28)), # 모델 인풋에 맞게
            transforms.ToTensor(), # 토치 텐서 타입으로 맞춰줘야함
        ])
        
        img_tensor = transform(img) # [1, 28, 28]
        img_tensor = img_tensor.unsqueeze(0) # [1, 1, 28, 28]

        print(img_tensor.shape)

        prediction = model(img_tensor)
                            # CNN은 10개의 아웃풋으로 각 10개의 클래스에 대한 피처값이 나온다, 이를 axis 1방향으로 max값을 찾는다는 것 
        result = torch.argmax(prediction, 1) #tensor([결과])
        result = result.tolist()[0] # 결과 라고 나오도록
        return result 


if __name__=="__main__":
  app.run(debug=True)
  # host 등을 직접 지정하고 싶다면
  # app.run(host="127.0.0.1", port="5000", debug=True)