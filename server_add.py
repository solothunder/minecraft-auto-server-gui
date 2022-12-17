import PySimpleGUI as sg
import os
from els import els
import minecraft

def main_run():
    check_dir = els.check_file_dir("minecraft/", "false", "false")
    if (check_dir == "error"):
        os.mkdir("minecraft")
    BAR_MAX = 100
    # ウィンドウに配置するコンポーネント
    layout = [  [sg.Text('作成',font=('Arial',20))],
                [sg.Text('バージョンを入力してください(デフォルトだと：1.19.3)'), sg.InputText()],
                [sg.Text('ポートを入力してください(デフォルトだと：25565)'), sg.InputText()],
                [sg.ProgressBar(BAR_MAX, orientation='h', size=(20, 20), key='-PROG-')],
                [sg.Button('次へ'), sg.Button('戻る')] ]

    # ウィンドウの生成
    window = sg.Window('Minecraft-Auto-Server', layout)

    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '戻る':
            break
        elif event == '次へ':
            minecraft.minecraft_install_yes_no(values[1])
            window.find_element('-PROG-').update(10)
            minecraft.minecraft_download(values[0])
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