import urllib.request
import shutil
import sys
import subprocess
import os
from els import els
import PySimpleGUI as sg
#同意用プログラム
def yes_no_input(anser):
    if anser == "Yes":
        return True
    else:
        sys.exit()
# papermc dl
def minecraft_download(minecraft_server_version):
    server_download_advance_check_ping = els.check_ping("google.com", "3", "False", "False")
    if server_download_advance_check_ping == "error":
        sg.popup("ネットワークがつながっていません\nダウンロードは行えません")
        sys.exit()
    ### ファイル内の文字列を検索・抽出
    file_name = 'advance_file/minecraft_server_link.txt'
    file_path = os.path.join(file_name)
    with open(file_path) as f:
        lines = f.readlines()
    # 入力情報に対してmatch caseで対応
    match minecraft_server_version:
        case "1.19.3": minecraft_server_link_lines = 0
        case "1.19.2": minecraft_server_link_lines = 1
        case "1.19": minecraft_server_link_lines = 2
        case "1.12.2": minecraft_server_link_lines = 3
        case "1.8.9": minecraft_server_link_lines = 4
        case _: 
            minecraft_server_link_lines = 0
    save_name='minecraft/server.jar'
    urllib.request.urlretrieve(lines[minecraft_server_link_lines], save_name)
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
    minecraft_input_info_yes_no = sg.popup_yes_no("これでよろしいでしょうか\n入力情報：\nサーバーメインポート：",port,"\nバージョン：", version)
    yes_no_input(minecraft_input_info_yes_no)
# eula 同意（yes no あり）
def minecraft_eula_edit():
    eula_popup_input = sg.popup_yes_no("Minecraft EULA（使用許諾契約 / 利用許諾契約）に同意しますか？\nMinecraftのEULA は https://www.minecraft.net/ja-jp/terms/r3 こちらを参照してください。")
    yes_no_input(eula_popup_input)
    shutil.copyfile("advance_file/eula.txt", "minecraft/eula.txt")
    sg.popup("同意しました。")
# minecraft 実行
def minecraft_exec(xmx, xms):
    exec_server_popup = sg.popup_yes_no("サーバー起動しますか？\n[Xms(最小メモリ):"+xms+"GB\nXmx(最大メモリ):"+xmx+"GB\n]")
    if exec_server_popup == "No":
        quit()
    cmd = "java -Xmx"+xmx+"G -Xms"+xms+"G -jar server.jar"
    subprocess.call(cmd, shell=True, cwd=r"minecraft/")
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

def minecraft_port(port):
    if not port:
        port = "25565"
    else:
        pass
    path = 'advance_file/server.properties'
    port_text = "server-port="+port+"\n"
    replace_setA = ('server-port=', port_text) # (検索する文字列, 置換後の文字列)
    # call func
    replace_func(path, replace_setA)
    shutil.copyfile("advance_file/server.properties", "minecraft/server.properties")