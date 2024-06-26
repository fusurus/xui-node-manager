import logging
import requests
import random
import json
import base64
import uuid
import argparse


class XUIManager:
    def __init__(self, username="tang", password="1002", port='1314'):
        self.username = username
        self.password = password
        self.port = port
        self.session = requests.session()

    def login(self, ip):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

        data = {
            'username': self.username,
            'password': self.password,
        }

        try:
            response = self.session.post(f'http://{ip}:{self.port}/login', headers=headers, data=data, verify=False)
            if response.status_code != 200:
                logging.error(f"{ip} 登录失败")
                return False
            logging.info(f"{ip} 登录成功")
            return True
        except Exception as e:
            logging.error(f"{ip} 登录失败: {e}")
            return False

    def add_inbound(self, ip, remark, client_id, idx=None):
        if idx is None:
            idx = 0  # 设置默认值，例如从0开始
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

        port = str(random.randint(1000, 65535))
        
        data = {
            'up': '0',
            'down': '0',
            'total': '0',
            'remark': f"{remark}{idx}",
            'enable': 'true',
            'expiryTime': '0',
            'listen': '',
            'port': port,
            'protocol': 'vmess',
            'settings': f'{{\n  "clients": [\n    {{\n      "id": "{client_id}",\n      "alterId": 0\n    }}\n  ],\n  "disableInsecureEncryption": false\n}}',
            'streamSettings': '{\n  "network": "tcp",\n  "security": "none",\n  "tcpSettings": {\n    "header": {\n      "type": "none"\n    }\n  }\n}',
            'sniffing': '{\n  "enabled": false,\n  "destOverride": [\n    "http",\n    "tls"\n  ]\n}',
        }

        try:
            response = self.session.post(f'http://{ip}:{self.port}/xui/inbound/add', headers=headers, data=data, verify=False)
            logging.info(f"{ip} 添加节点成功")
            return True
        except Exception as e:
            logging.error(f"{ip} 添加节点失败: {e}")
            return False

    def get_inbounds(self, ip, client_id):
        try:
            response = self.session.post(f'http://{ip}:{self.port}/xui/inbound/list', headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}, verify=False)
            if response.status_code != 200:
                logging.error(f"{ip} 获取节点失败")
                return
            
            logging.info(f"{ip} 获取节点成功")

            result = response.json()["obj"][-1]
            obj = {
                "v": result["id"],
                "ps": result["remark"],
                "add": ip,
                "port": result["port"],
                "id": client_id,
                "aid": 0,
                "net": "tcp",
                "type": "none",
                "host": "",
                "path": "",
                "tls": "none",
            }
            json_str = json.dumps(obj, indent=2)
            byte_str = json_str.encode('utf-8')
            base64_encoded_str = base64.b64encode(byte_str)
            decoded_str = base64_encoded_str.decode('utf-8')
            logging.info(f"vmess://{decoded_str}\n")
            with open('vmess.txt', 'a', encoding='utf-8') as f:
                f.write(f"vmess://{decoded_str}\n")
            return True
        except Exception as e:
            logging.error(f"{ip} 获取失败: {e}")
            return False



if __name__ == '__main__':
    
    # 使用argparse添加命令行参数
    parser = argparse.ArgumentParser(description="XUI 入站管理脚本")
    parser.add_argument('--notes', type=str, default="dl", help="用于入站条目的备注，默认为'dl'")
    parser.add_argument('--idx', type=int, default=0, help="入站条目的索引(默认值:0)")
    args = parser.parse_args()
    notes = args.notes
    idx = args.idx

    with open('ips.txt', 'r', encoding='utf-8') as f:
        ips_list = f.readlines()
        for i, ip in enumerate(ips_list):
            ip = ip.strip()
            manager = XUIManager()
            if manager.login(ip):
                client_id = str(uuid.uuid4())
                manager.add_inbound(ip, notes, client_id, i+idx)
                manager.get_inbounds(ip, client_id)

    print("done")
