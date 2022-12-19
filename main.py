import PySimpleGUI as sg
import server_add
import server_control
import os
from els import els

def main():
    
    path = ["server_add.py", "server_control.py", "minecraft.py", "els/els.py", "advance_file/server.properties", "advance_file/eula.txt", "advance_file/minecraft_server_link.txt"]
    for pathcount in path:
        file_check = els.check_file_dir(pathcount, "False", "False")
        if file_check == "error":
            sg.popup("ファイルが見つからないため実行できません\n見つからないファイル:\n"+pathcount)

    check_dir = els.check_file_dir("minecraft/", "false", "false")
    if (check_dir == "error"):
        os.mkdir("minecraft")
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
        elif event == '作成':
            server_add.main_run()
        elif event == '管理':
            server_control.main_run()


    window.close()
if __name__ == ("__main__"):
    main()
