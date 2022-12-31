import PySimpleGUI as sg
import server_add
import server_control
import os
from els import els

def main():
    # ファイル存在チェック
    path = ["server_add.py", "server_control.py", "minecraft.py", "els/els.py"]
    for pathcount in path:
        if els.check_file_dir(pathcount, "False", "False") == "error":
            sg.popup("ファイルが見つからないため実行できません\n見つからないファイル:\n"+pathcount)
            quit()
    # もしファイル・ディレクトリが存在しない場合は、作成する
    if (els.check_file_dir("data/", "false", "false") == "error"):
        os.mkdir("data")
    if (els.check_file_dir("minecraft/", "false", "false") == "error"):
        os.mkdir("minecraft")
    path = ["data/minecraft-list.txt", "data/minecraft-dir-list.txt"]
    for pathcount in path:
        check_file_minecraft_csv = els.check_file_dir(pathcount, "False", "False")
        if check_file_minecraft_csv == "error":
            file = open(pathcount, mode='w')
            file.write('')
            file.close()

    # ウィンドウに配置するコンポーネント
    layout = [  [sg.Text('Minecraft-Auto-Server GUI',font=('Arial',20))],
                [sg.Text('不具合が発生した場合はgithubのIssuesにお知らせください。')],
                [sg.Text('作成か管理を選択してください')],
                [sg.Button('作成'), sg.Button('管理'), sg.Button('終了')] ]

    # ウィンドウの生成
    window = sg.Window('Minecraft-Auto-Server', layout)

    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '終了':
            break
        # ボタンの操作により他のプログラムが実行される
        elif event == '作成':
            server_add.main_run()
        elif event == '管理':
            server_control.main_run()


    window.close()
if __name__ == ("__main__"):
    main()
