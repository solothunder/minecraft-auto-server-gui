import PySimpleGUI as sg
import os
from els import els
import minecraft
import shutil
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

def main_run():
    check_dir = els.check_file_dir("minecraft/", "false", "false")
    if (check_dir == "error"):
        os.mkdir("minecraft")
    BAR_MAX = 100
    # ウィンドウに配置するコンポーネント
    layout = [  [sg.Text('作成',font=('Arial',20))],
                [sg.Text("バージョンは自分がjarファイルを持っている場合には、入力する必要がありません")],
                [sg.Text('バージョンを入力してください(デフォルトだと：1.19.3)'), sg.InputText()],
                [sg.Text('ポートを入力してください(デフォルトだと：25565)'), sg.InputText()],
                [sg.Text("進捗："),sg.ProgressBar(BAR_MAX, orientation='h', size=(20, 20), key='-PROG-')],
                [sg.Button('次へ'), sg.Button('戻る')] ]

    # ウィンドウの生成
    window = sg.Window('Minecraft-Auto-Server', layout)

    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '戻る':
            break
        elif event == '次へ':
            minecraft_server_local_jar_result = minecraft_server_local_jar_file()
            minecraft.minecraft_install_yes_no(values[1], values[0], minecraft_server_local_jar_result)
            window.find_element('-PROG-').update(10)
            if minecraft_server_local_jar_result == "no":
                minecraft.minecraft_download(values[0])
                window.find_element('-PROG-').update(70)
            else:
                shutil.copyfile(minecraft_server_local_jar_result, "minecraft/server.jar")
                window.find_element('-PROG-').update(70)
            minecraft.minecraft_eula_edit()
            window.find_element('-PROG-').update(85)
            minecraft.minecraft_port(values[1])
            window.find_element('-PROG-').update(100)
            sg.popup("インストールが終わりました\n管理から起動できます")
            break


    window.close()

if __name__ == "__main__":
    main_run()