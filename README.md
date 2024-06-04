XUI 入站管理脚本

## 简介

这是一个用于管理XUI面板入站配置的自动化脚本。通过简单的命令行界面，您可以轻松地向XUI面板添加新的入站连接配置项，适用于批量管理和自动化部署场景。

## 特性

灵活的参数配置：支持自定义用户名、密码、面板端口、备注信息及入站条目索引。

自动化操作：自动登录面板、添加入站配置、获取配置详情并保存为vmess链接。

命令行友好：使用argparse库简化命令行参数输入，提高易用性。

* * *

# 安装依赖

在不同的Linux服务器上安装Ansible通常涉及以下几个步骤。在大多数情况下，您需要在控制节点（即运行Ansible的机器）上进行安装，而不是在目标服务器上。`ansible_ssh_private_key_file` 是指在控制节点上用于SSH连接到目标服务器的私钥文件路径，这与安装Ansible的过程无关。以下是安装Ansible的一般步骤：

1. 更新系统
  
         sudo apt-get update  # 对于Debian/Ubuntu
         sudo yum update  # 对于CentOS/RHE
  
2. **安装Python相关依赖**： 如果您的系统中没有`python3-pip`或`pip3`，您需要先安装它：
  
         sudo apt-get install python3-pip  # Debian/Ubuntu
         sudo yum install python3-pip  # CentOS/RHEL 
  
3. 安装requests库
  
          pip install requests  # 如果没有pip3使用这条
          pip3 install requests # 有pip3使用这条
  
4. 安装Ansible
  
      # Debian/Ubuntu
         sudo apt-get update
         sudo apt-get install ansible
      # CentOS/RHEL
         sudo yum install -y epel-release
         sudo yum install -y ansible
      # 使用 dnf（CentOS 8及以上 / RHEL 8及以上）：
         sudo dnf install -y ansible
      # Fedora
         sudo dnf install ansible
  
5. 验证安装
  
         ansible --version
  
  * * *
  

# 快速开始

1. 准备一个文本文件（默认为`ips.txt`），每行一个IP地址。
  
2. 在命令行中运行脚本，并根据需要调整参数：
  
         python ansible_lnventory_hosts.py --help
  

## 示例命令

* 指定输入文件为`ips.txt`，Ansible用户为`hosts`：
  
      python3 ansible_lnventory_hosts.py --input-file=ips.txt --ansible-user=hosts
  

## 修改Ansible配置文件

1. **当前目录下的 `ansible.cfg` 文件**：如果在当前工作目录下有 `ansible.cfg` 文件，Ansible 会使用它。
  
2. **用户主目录下的 `.ansible.cfg` 文件**：如果在用户的主目录下有 `.ansible.cfg` 文件，Ansible 会使用它。
  
3. **全局配置文件 `/etc/ansible/ansible.cfg`**：这是系统范围内的配置文件，如果以上位置都没有找到配置文件，Ansible 会使用这个文件。
  

使用命令:

    vim /etc/ansible/ansible.cfg
    # 把文件中的前面的"#"号删除
    host_key_checking = False

# 新建ansible的yml文件

* 新建一个名为"playbook.yml"的文件
  

    touch playbook.yml
    vim playbook.yml

* 复制下面的文件内容并且保存
  

    ---
    - name: Execute script on multiple servers
      hosts: servers
      tasks:
        - name: Run x-ui install script
          shell: bash -c 'yes | bash <(curl -Ls https://raw.githubusercontent.com/fusurus/x-ui/main/install.sh)'
          args:
            executable: /bin/bash

## 执行批量安装x-ui面板

    ansible-playbook -i hosts playbook.yml

* * *

# 使用指南

## 基本用法

运行脚本前，请确保您有权限访问目标XUI面板，并且了解基本的命令行操作。

    python xui_manager.py --help

上述命令将展示所有可用的命令行参数及其默认值。

### 参数说明

* `--user` 或 `-u`: 面板用户名，默认为 `'admin'`。
* `--pwd` 或 `-p`: 面板密码，默认为 `'123456'`。
* `--port` 或 `-P`: 面板端口，默认为 `'1314'`。
* `--notes` 或 `-n`: 用于入站条目的备注，默认为 `'dl'`。
* `--idx` 或 `-i`: 入站条目的索引，默认为 `0`，用于区分不同的配置项。

### 示例

添加一个新的入站配置，使用默认用户名和端口，自定义备注为"dl"，索引从1开始：

python xui_manager.py --notes "dl" --idx 1

### 注意事项

* 请确保提供正确的面板地址、端口、用户名和密码。
* 脚本执行过程中会产生vmess链接，存储于当前目录下的`vmess.txt`文件中。

开发与贡献

欢迎提交问题或提出改进意见。如有兴趣贡献代码，请遵循标准的GitHub流程进行。

* * *

此README提供了脚本的基本介绍、安装指南、使用示例及注意事项，便于其他开发者或用户快速上手并使用您的脚本。
