import PySimpleGUI as sg
import os
from els import els
import minecraft

def main_run():
    check_dir = els.check_file_dir("minecraft/", "false", "false")
    if (check_dir == "error"):
        os.mkdir("minecraft")
    # ウィンドウに配置するコンポーネント
    layout = [  [sg.Text('作成',font=('Arial',20))],
                [sg.Text('バージョンを入力してください(デフォルトだと：25565)'), sg.InputText()],
                [sg.Text('ポートを入力してください(デフォルトだと：25565)'), sg.InputText()],
                [sg.Button('次へ'), sg.Button('戻る')] ]

    # ウィンドウの生成
    window = sg.Window('Minecraft-Auto-Server', layout)

    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '戻る':
            break
        elif event == '次へ':
            minecraft.minecraft_download(values[0])
            minecraft.minecraft_eula_edit()
            minecraft.minecraft_port(values[1])
            els.global_ip("False", "True")


    window.close()

if __name__ == "__main__":
    main_run()