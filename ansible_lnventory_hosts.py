import argparse

def generate_inventory(input_file, ansible_user):
    # 创建或清空 hosts 文件
    with open("hosts", 'w', encoding='utf-8') as f:
        f.write("[servers]\n")

        # 读取 ips.txt 文件并添加到 hosts 文件
        with open(input_file, 'r') as ip_file:
            for line in ip_file:
                ip = line.strip()
                f.write(f"{ip} ansible_user={ansible_user} ansible_ssh_private_key_file=/root/.ssh/id_rsa\n")

        f.write("[all:vars]\n")
        f.write("ansible_user={}\n".format(ansible_user))
        f.write("ansible_ssh_private_key_file=/root/.ssh/id_rsa\n")
    print("Ansible hosts file generated successfully!")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="生成 Ansible 格式文件")
    parser.add_argument('--input-file', type=str, default="ips.txt", help="包含IP地址的输入文件(默认值:dlips.txt)")
    parser.add_argument('--ansible-user', type=str, default="root", help="库存的ansible_user用户(默认值:root)")

    args = parser.parse_args()

    generate_inventory(args.input_file, args.ansible_user)