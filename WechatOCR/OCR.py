'''
使用python 3.10以上的版本，因为wcocr.pyd是用这个版本编译的
'''
from src import wcocr


def wechat_ocr(image_path):
    wcocr.init(r"src/WeChatOCR.exe", "src")
    result = wcocr.ocr(image_path)
    for temp in result['ocr_response']:
        print(temp['text'])


if __name__ == '__main__':
    image_path = r"D:\Users\pbl\Desktop\superFolder\input\12.png"
    wechat_ocr(image_path)
