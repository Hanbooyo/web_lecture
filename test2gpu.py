# app.py
from flask import Flask, render_template
from flask import request
import torch
from PIL import Image
import torchvision.transforms as transforms

# 랜덤 시드 고정
torch.manual_seed(777)


device = 'cuda' if torch.cuda.is_available() else 'cpu'

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





#Flask객체 인스턴스 생성
app = Flask(__name__) # app이라는 플라스크 인스턴스 생성

@app.route('/') 
def index(): 

    return render_template('upload.html') # templates 폴더를 자동인식, 절대경로 입력안해줘도됨

@app.route('/uploader', methods = ['POST']) 
def uploader_file(): 
    f = request.files['file'] # index.html 에서 file이라는 이름의 요소가 가지고 있는  8.png를  객체로 호출함
    print(f.filename) # f객체에서 filename을 가져옴, 8.png라고 되어있을 것이다.
    f.save("./images/"+f.filename) # f를 현재 작업 디렉토리 images 폴더에 8.png라고 저장
    
    #모델 inference 함수 호출
    model_result = infer("./images/"+f.filename)
    
    return render_template('CNN_result.html', result = model_result) 

def infer(filename):
    with torch.no_grad():
        # 다시불러와서 추론 해보기
        model = CNN().to(device)
        model.load_state_dict(torch.load("cnn_model.pt")) 
        model.eval() #평가 모드로 설정하여야 합니다. 이 과정을 거치지 않으면 일관성 없는 추론 결과가 출력
        # 이미지 파일 경로 설정
        img = Image.open(filename)
        transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1), # RGB(3D) -> Gray(2D)
            transforms.Resize((28, 28)), # 모델 인풋에 맞게
            transforms.ToTensor(), # 토치 텐서 타입으로 맞춰줘야함
        ])
        
        img_tensor = transform(img).to(device) # [1, 28, 28]
        img_tensor = img_tensor.unsqueeze(0) # [1, 1, 28, 28] #모델이 원래 [배치사이즈 가로 세로 등]

        prediction = model(img_tensor)

        result = torch.argmax(prediction, 1).tolist()[0]
        
    return result

if __name__=="__main__": #scipt실행했을때 가장 먼저 실행되는 부분,
    app.run(debug=True)
