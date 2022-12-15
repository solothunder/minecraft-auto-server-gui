import PySimpleGUI as sg

sg.theme('DarkAmber')   # デザインテーマの設定

# ウィンドウに配置するコンポーネント
layout = [  [sg.Text('Minecraft-Auto-Server GUI',font=('Arial',20))],
            [sg.Text('作成か管理を選択してください')],
            [sg.Button('作成'), sg.Button('管理'), sg.Button('終了')] ]

# ウィンドウの生成
window = sg.Window('Minecraft-Auto-Server', layout)

# イベントループ
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == '終了':
        break
    elif event == 'OK':
        print('あなたが入力した値： ', values[0])

window.close()