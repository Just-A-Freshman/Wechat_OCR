from pathlib import Path
import argparse
import wcocr
import os
import re




def find_wechatocr_exe() -> str:
    appdata_path = Path(os.getenv("APPDATA", ""))
    if not appdata_path:
        return "src/plugins/ocr/WeChatOCR.exe"
    
    base_path = appdata_path / "Tencent" / "WeChat" / "XPlugin" / "Plugins" / "WeChatOCR"
    version_pattern = re.compile(r'\d+')
    
    try:
        path_temp = list(base_path.iterdir())
    except FileNotFoundError:
        return ""
    
    for temp in path_temp:
        if version_pattern.match(temp.name):
            wechatocr_path = temp / 'extracted' / 'WeChatOCR.exe'
            if wechatocr_path.is_file():
                return str(wechatocr_path)
    return ""


def find_wechat_path() -> str:
    common_paths = Path(r"C:\Program Files\Tencent\WeChat")
    version_pattern = re.compile(r'\[\d+\.\d+\.\d+\.\d+\]')
    try:
        path_temp = list(common_paths.iterdir())
    except FileNotFoundError:
        return ""
    for temp in path_temp:
        if version_pattern.match(temp.name):
            wechat_path = temp
            if wechat_path.is_dir():
                return str(wechat_path)
    return ""


def get_result(image_path: str, wechat_path: str, wechatocr_path: str) -> dict:
    wcocr.init(wechatocr_path, wechat_path)
    results = wcocr.ocr(image_path)["ocr_response"]
    format_results = []
    for result in results:
        format_results.append({
            "text": result["text"],
            "box": [result["left"], result["top"], result["right"], result["bottom"]],
            "rate": result["rate"] 
        })
    return format_results

def get_ocr_results(directory_path: str):
    results = dict()
    image_suffixes = [".jpg", ".png", ".jpeg", ".JPG", ".PNG", ".JPEG"]
    for image_path in Path(directory_path).iterdir():
        if image_path.is_file() and image_path.suffix in image_suffixes:
            results[image_path.name] = get_result(
                str(image_path),
                wechat_path=args.wechat_path,
                wechatocr_path=args.wechatocr_path
            )
    return results


def check_valid_path(wechat_path: str, wechatocr_path: str) -> bool:
    return os.path.isdir(wechatocr_path) and os.path.isfile(wechat_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default="")
    parser.add_argument('--wechat_path', type=str, default=find_wechat_path())
    parser.add_argument('--wechatocr_path', type=str, default=find_wechatocr_exe())
    args: argparse.Namespace = parser.parse_args()
    if args.image_path == "":
        print("Usage: --image_path=[your_image_path_or_directory]")
        print("Options: --wechat_path=[your_wechat_install_path] --wechatocr_path=[path_to_WeChatOCR.exe]")
        print("If the program cannot find your WeChatOCR.exe or WeChat installation path, please specify them.")
    else:
        if check_valid_path(args.wechat_path, args.wechatocr_path):
            print("Error: WeChatOCR.exe or WeChat installation path is invalid!")
        else:
            print(f"Detected WeChatOCR.exe path: {args.wechatocr_path}")
            print(f"Detected WeChat installation path: {args.wechat_path}")
        if os.path.isfile(args.image_path):
            print(get_result(args.image_path, args.wechat_path, args.wechatocr_path))
        elif os.path.isdir(args.image_path):
            print(get_ocr_results(args.image_path))
        elif args.image_path != "":
            print(f"Error: Path '{args.image_path}' does not exist.")

