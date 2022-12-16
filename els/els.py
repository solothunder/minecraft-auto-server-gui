import ctypes
import os
import platform
import socket
import subprocess
import sys
import time
from threading import Event
import urllib.request
# 遅延関数化
def wait(time):
    Event().wait(int(time))



def print_els(text_els, print_switch):
    if print_switch == "True":
        print(text_els)
    else:
        pass

def stop_15_sec(print_switch):
    if print_switch == "True":
        wait(15)
        sys.exit()
    else:
        pass

# OS確認
def check_platform(print_switch):
    print_els("Your PC OS [{0}]".format(platform.system()), print_switch)
    return platform.system()

# ファイルチェック（存在）
def check_file_dir(path, error_stop_switch, print_switch):
    is_path_file = os.path.exists(str(path))
    if is_path_file:
        if print_switch == "True":
            print("\r[OK] File {0}                                           .".format(path),end="")
        return "ok"
    else:
        if print_switch == "True":
            print("[Error] File {0}                                           .".format(path),end="")
        if error_stop_switch == "True":
            print_els("残念ながらファイルが存在しません　15秒後にプログラムが終了します", print_switch)
            stop_15_sec(print_switch)
            sys.exit()
        else:
            pass
        return "error"

# Pingで応答来るか
def check_ping(host, count_els, error_stop_switch, print_switch):
    if not host:
        host = "google.com"
    else:
        pass
    if not count_els:
        count_els = "2"
    else:
        pass
    wait(1)
    if platform.system() == "Windows":
        res = subprocess.run(["ping",host,"-n",count_els, "-w", "300"],stdout=subprocess.PIPE)
        if res.returncode == 0 :
            print_els("[OK] NetWork {0}".format(host), print_switch)
            time.sleep(1.7)
            return "ok"
        else:
            print_els("[Error] Network {0}".format(host), print_switch)
            if error_stop_switch == "True":
                print_els("残念ながらネットワークがつながっていませんでした 15秒後にプログラムが終了します", print_switch)
                stop_15_sec(print_switch)
                sys.exit()
            return "error"
    else:
        res = subprocess.run(["ping",host,"-c",count_els],stdout=subprocess.PIPE)
        if res.returncode == 0 :
            print_els("[OK] NetWork {0}".format(host), print_switch)
            time.sleep(1.7)
            return "ok"
        else:
            print_els("[Error] Network {0}".format(host), print_switch)
            if error_stop_switch == "True":
                print_els("残念ながらネットワークがつながっていませんでした 15秒後にプログラムが終了します", print_switch)
                stop_15_sec(print_switch)
                sys.exit()
            else:
                pass
            return "error"
# IP確認（192）
def private_ip(host, port, print_switch):
        time.sleep(0.3)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((host, int(port)))
        print_els("Private_IP: {0}".format(s.getsockname()[0]), print_switch)
        time.sleep(1.7)
        return s.getsockname()[0]
# G_IP確認
def global_ip(error_stop_switch, print_switch):
    if platform.system() == "Windows":
        res = subprocess.run(["ping","google.com","-n","1", "-w", "300"],stdout=subprocess.PIPE)
        if res.returncode == 0 :
            time.sleep(0.3)
            g_ip = urllib.request.urlopen('http://api.ipify.org/').read().decode('utf-8')
            print_els("グローバルIP（ポート開放した後に必要です。）: {0}".format(g_ip), print_switch)
            return g_ip
        else:
            print_els("残念ながらネットワークがつながっていませんでした グローバルIPは後で確認してください。", print_switch)
            if error_stop_switch == "True":
                print_els("残念ながらネットワークがつながっていませんでした 15秒後にプログラムが終了します", print_switch)
                stop_15_sec(print_switch)
                sys.exit()
            return "error"