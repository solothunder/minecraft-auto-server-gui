import urllib.request
import sys
import subprocess
import os
from els import els
import PySimpleGUI as sg

minecraft_download_link_list = [
    'https://launcher.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar', #1.16.5
    'https://launcher.mojang.com/v1/objects/0a269b5f2c5b93b1712d0f5dc43b6182b9ab254e/server.jar', #1.17
    'https://launcher.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar', #1.17.1
    'https://launcher.mojang.com/v1/objects/3cf24a8694aca6267883b17d934efacc5e44440d/server.jar', #1.18
    'https://launcher.mojang.com/v1/objects/125e5adf40c659fd3bce3e66e67a16bb49ecc1b9/server.jar', #1.18.1
    'https://launcher.mojang.com/v1/objects/c8f83c5655308435b3dcf03c06d9fe8740a77469/server.jar', #1.18.2
    'https://launcher.mojang.com/v1/objects/e00c4052dac1d59a1188b2aa9d5a87113aaf1122/server.jar', #1.19
    'https://piston-data.mojang.com/v1/objects/8399e1211e95faa421c1507b322dbeae86d604df/server.jar', #1.19.1
    'https://piston-data.mojang.com/v1/objects/f69c284232d7c7580bd89a5a4931c3581eae1378/server.jar', #1.19.2
    'https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar' #1.19.3
]

# papermc dl
def minecraft_download(minecraft_server_version, dir_name):
    server_download_advance_check_ping = els.check_ping("google.com", "3", "False", "False")
    if server_download_advance_check_ping == "error":
        sg.popup("ネットワークがつながっていません\nダウンロードは行えません")
        sys.exit()
    # 入力情報に対してmatch caseで対応
    match minecraft_server_version:
        case "1.19.3": minecraft_server_link_lines = 9
        case "1.19.2": minecraft_server_link_lines = 8
        case "1.19.1": minecraft_server_link_lines = 7
        case "1.19": minecraft_server_link_lines   = 6
        case "1.18.2": minecraft_server_link_lines = 5
        case "1.18.1": minecraft_server_link_lines = 4
        case "1.18": minecraft_server_link_lines   = 3
        case "1.17.1": minecraft_server_link_lines = 2
        case "1.17": minecraft_server_link_lines   = 1
        case "1.16.5": minecraft_server_link_lines = 0
        case _:
            minecraft_server_link_lines = 9
            minecraft_server_version = "1.19.3"
            anser = sg.popup_yes_no("こちらでは判定できないバージョン・文字列が検出されました\nYesを押すと自動的に最新バージョン(ver."+minecraft_server_version+")がインストールされます。")
            if anser == "Yes":
                pass
            else:
                quit()
    save_name=dir_name+"/server.jar"
    urllib.request.urlretrieve(minecraft_download_link_list[minecraft_server_link_lines], save_name)
    return minecraft_server_version
# 入れた情報がいいかどうか？
def minecraft_install_yes_no(port, version, minecraft_server_local_jar_result):
    if not port:
        port = "25565(デフォルト)"
    else:
        pass
    if minecraft_server_local_jar_result == "no":
        if not version:
            version = "1.19.3(デフォルト)"
    #jarファイルを自前で持っていた場合は?.?になる
    else:
        version = "?.?(ユーザー自前 jarファイル)"
    anser = sg.popup_yes_no("これでよろしいでしょうか\n入力情報：\nサーバーメインポート：",port,"\nバージョン：", version)
    if anser == "Yes":
        pass
    else:
        quit()
# minecraft 実行
def minecraft_exec(xmx, xms, dir_name):
    # もし入力内容が0かnotだったら1(1GB)に
    mem = [xms, xmx]
    for column_num in range(2):
        if not mem[column_num] or mem[column_num] == "0":
            mem[column_num] = "1"
        if mem[column_num].isdigit():
            pass
        else:
            sg.popup("数字（例:1）などを入力してください\n起動できません")
            quit()
    for column_num in range(2):
        mem[column_num]
    exec_server_popup = sg.popup_yes_no("サーバー起動しますか？\n[ファイル名:"+dir_name+"/server.jar\nXms(最小メモリ):"+mem[0]+"GB\nXmx(最大メモリ):"+mem[1]+"GB\n]")
    if exec_server_popup == "No":
        quit()
    cmd = "java -Xmx"+mem[1]+"G -Xms"+mem[0]+"G -jar server.jar"
    subprocess.call(cmd, shell=True, cwd=r""+dir_name+"/")
    sg.popup("サーバー停止")
# 行編集
def replace_func(fname, replace_set):
    target, replace = replace_set
    
    with open(fname, 'r') as f1:
        tmp_list =[]
        for row in f1:
            if row.find(target) != -1:
                tmp_list.append(replace)
            else:
                tmp_list.append(row)
    
    with open(fname, 'w') as f2:
        for i in range(len(tmp_list)):
            f2.write(tmp_list[i])

def file_identification_rewriting(dir_name, file_name, before, after):
    path = dir_name+"/"+file_name
    replace_setA = (before, after) # (検索する文字列, 置換後の文字列)
    # call func
    replace_func(path, replace_setA)