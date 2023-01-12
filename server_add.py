from urllib.request import Request, urlopen
import PySimpleGUI as sg
from els import els
import os
import minecraft
import shutil
import csv
import datetime
import sys

#自前でjarファイルを持っていたときに読み込む関数
def minecraft_server_local_jar_file():
    minecraft_local_jar_yes_no = sg.popup_yes_no("Jarファイル手動読み込み\n\nインストールのときにプログラムを書いたとき最新のサーバーバージョンにするようにしていますが\n最新のバージョンではない・入れたいバージョンがない場合があります。\nもしjarファイル(例server.jar)がある場合は読み込むことができます。\n手動で読み込みますか？")
    if minecraft_local_jar_yes_no == "Yes":
        while True:
            print()
            minecraft_local_jar_path = sg.popup_get_file('jarファイルを指定してください\n例:server.jar', file_types=(("Java Archive", ".jar"),))
            if not minecraft_local_jar_path:
                sg.popup("ファイルが選択されていません")
                return "no"
            minecraft_local_jar_check_file = els.check_file_dir(minecraft_local_jar_path, "False", "False")
            if minecraft_local_jar_check_file == "error":
                sg.popup("ファイルが存在しません。")
                return False
            return minecraft_local_jar_path
    elif minecraft_local_jar_yes_no == "No":
        return "no"

# server.properties ダウンロード
def minecraft_server_properties_download(path):
    url = 'https://server.properties/'
    # そのままだとurllib.error.HTTPError: HTTP Error 403: Forbiddenでコケるからユーザーエージェントを偽装
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)
    html = urlopen(request).read()
    html = html.decode('utf-8')
    # ファイル書き込み(server.properties)
    file = open(path+"/server.properties", mode='w')
    file.write(str(html))
    file.close()

def main_run():
    dt_now = datetime.datetime.now()
    check_dir = els.check_file_dir("minecraft/", "false", "false")
    if (check_dir == "error"):
        os.mkdir("minecraft")
    BAR_MAX = 100
    # ウィンドウに配置するコンポーネント
    layout = [  [sg.Text('作成',font=('Arial',20))],
                [sg.Text("バージョンは自分がjarファイルを持っている場合には、入力する必要がありません")],
                [sg.Text('バージョン(デフォルトだと：1.19.3)'), sg.InputText()],
                [sg.Text('ポート(デフォルトだと：25565)'), sg.InputText()],
                [sg.Text('名前(デフォルトだと：サーバー（未入力）)'), sg.InputText()],
                [sg.Text("進捗："),sg.ProgressBar(BAR_MAX, orientation='h', size=(20, 20), key='-PROG-')],
                [sg.Text('', key='-PROGRESS-')],
                [sg.Button('次へ'), sg.Button('戻る')] ]

    # ウィンドウの生成
    window = sg.Window('Minecraft-Auto-Server', layout)

    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '戻る':
            break
        elif event == '次へ':
            # jar読み込みモードかどうか・その場合の動作
            minecraft_server_local_jar_result = minecraft_server_local_jar_file()
            minecraft.minecraft_install_yes_no(values[1], values[0], minecraft_server_local_jar_result)
            new_dir_path_time = dt_now.strftime('%Y-%m-%d-%H-%M-%S-%f')[:-3]
            new_dir_path = "minecraft/minecraft-"+new_dir_path_time
            window['-PROGRESS-'].update(f'フォルダ作成'+new_dir_path)
            os.mkdir(new_dir_path)
            window['-PROGRESS-'].update(f'ファルダ作成完了')
            window.find_element('-PROG-').update(10)
            # jar読み込みモードではないときの動作
            if minecraft_server_local_jar_result == "no":
                window['-PROGRESS-'].update(f'サーバーダウンロード中')
                minecraft_server_version = minecraft.minecraft_download(values[0], new_dir_path)
                print(minecraft_server_version)
                window.find_element('-PROG-').update(70)
                window['-PROGRESS-'].update(f'サーバーダウンロード完了')
            # jar読み込みモード時の動作
            else:
                window['-PROGRESS-'].update(f'jarファイルコピー中')
                shutil.copyfile(minecraft_server_local_jar_result, new_dir_path+"/server.jar")
                minecraft_server_version = "unknown"
                window.find_element('-PROG-').update(70)
                window['-PROGRESS-'].update(f'jarファイルコピー完了')
            # minecraftのeula(eula.txt)の同意するか？同意したら書き換える
            eula_yes_no_popup = sg.popup_yes_no("Minecraft EULA（使用許諾契約 / 利用許諾契約）に同意しますか？\nMinecraftのEULA は https://www.minecraft.net/ja-jp/terms/r3 こちらを参照してください。")
            if eula_yes_no_popup == "Yes":
                pass
            else:
                sys.exit()
            file = open(new_dir_path+"/eula.txt", mode='w')
            # 書き換え(作成)内容
            file.write('#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n#Fri Dec 09 09:06:15 JST 2022\neula=true')
            file.close()
            window.find_element('-PROG-').update(85)
            window['-PROGRESS-'].update(f'EULA(ソフトウェア利用許諾契約)同意完了')
            # minecraftのポート変更（server.properties）
            window['-PROGRESS-'].update(f'ポート設定中')
            minecraft_server_properties_download(new_dir_path)
            if not values[1]:
                values[1] = "25565"
            window['-PROGRESS-'].update(f'ポート設定完了')
            # txtファイル（data/minecraft-dir-list.txt・data/minecraft-list.txt）
            window['-PROGRESS-'].update(f'txtファイル記述中')
            minecraft_server_name = values[2]
            minecraft_server_list_txt_lines_count = sum([1 for _ in open('data/minecraft-list.txt')])
            if not minecraft_server_name:
                minecraft_server_name = "サーバー（未入力）"
            with open('data/minecraft-list.txt', 'a', encoding="utf-8") as f:
                print("NO："+str(minecraft_server_list_txt_lines_count + 1)+" ｜サーバー名："+minecraft_server_name+" ｜作成時間："+dt_now.strftime('%Y年%m月%d日 %H:%M:%S')[:-3]+" ｜サーバーバージョン（jar読み込みだとunknown）："+minecraft_server_version+" ｜ディレクトリ位置："+new_dir_path+"/", file=f)
            with open('data/minecraft-dir-list.txt', 'a', encoding="utf-8") as f:
                print(new_dir_path, file=f)
            window['-PROGRESS-'].update(f'txtファイル記述完了')
            # 終わり
            window.find_element('-PROG-').update(100)
            window['-PROGRESS-'].update(f'インストール完了')
            sg.popup("インストールが終わりました\n管理から起動できます")
            break


    window.close()

if __name__ == "__main__":
    main_run()