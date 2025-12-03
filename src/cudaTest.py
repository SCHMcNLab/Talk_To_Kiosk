import torch
print(torch.cuda.is_available())  # True가 떠야 정상
print(torch.cuda.get_device_name(0))  # GPU 이름 출력
