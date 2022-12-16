import PySimpleGUI as sg
import minecraft

def main_run():
    
    # ウィンドウに配置するコンポーネント
    layout = [  [sg.Text('管理（起動）',font=('Arial',20))],
                [sg.Text('Xms(最小メモリ)を入力してください（G）※数字のみ：'), sg.InputText()],
                [sg.Text('Xmx(最大メモリ)を入力してください（G）※数字のみ：'), sg.InputText()],
                [sg.Button('起動'), sg.Button('戻る')] ]

    # ウィンドウの生成
    window = sg.Window('Minecraft-Auto-Server', layout)

    # イベントループ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '戻る':
            break
        elif event == '起動':
            minecraft.minecraft_exec(values[1],values[0])


    window.close()

if __name__ == "__main__":
    main_run()