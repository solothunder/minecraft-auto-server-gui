import PySimpleGUI as sg
import minecraft
from els import els
import sys
import linecache

def main_run():
    path = ["data/minecraft-list.txt", "data/minecraft-dir-list.txt"]
    for pathcount in path:
        check_file_minecraft_txt = els.check_file_dir(pathcount, "False", "False")
        if check_file_minecraft_txt == "error":
            sg.popup("必要なファイルが存在しません。")
            quit()
    # txtファイルの行数カウント
    minecraft_server_list_txt_lines_count = sum([1 for _ in open('data/minecraft-list.txt', encoding="utf-8")])
    minecraft_server_dir_list_txt_lines_count = sum([1 for _ in open('data/minecraft-dir-list.txt', encoding="utf-8")])
    # もし行数が一致しなければポップアップを出して終了させる
    if minecraft_server_dir_list_txt_lines_count == minecraft_server_list_txt_lines_count:
        pass
    else:
        sg.popup('txtファイル同士の行数が一致しないため起動できません。')
    # txtファイル内容を読み込み
    with open("data/minecraft-list.txt", "r", encoding="utf-8") as f:
        minecraft_server_list_txt = f.read()

    # ウィンドウに配置するコンポーネント
    layout = [  [sg.Text('管理（起動）',font=('Arial',20))],
                [sg.Text('起動するサーバーを選択してください',font=('Arial',15))],
                [sg.Text(minecraft_server_list_txt, font=('Arial',12))],
                [sg.Text('サーバーを選んでください (NOと同じ・上から1.2.3.4)：'), sg.InputText()],
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
            # ifは数字ではないときのために分けておく
            if not values[0] or not values[0].isdigit():
                sg.popup("サーバー選択数字の入力方法が間違っているか、指定した行がない可能性があります。発見された可能性　「行数が入力されていない・数字ではない」")
                quit()
            if int(values[0]) <= 0 or int(minecraft_server_dir_list_txt_lines_count) < int(values[0]) - 1 or int(minecraft_server_list_txt_lines_count) < int(values[0]):
                sg.popup("サーバー選択数字の入力方法が間違っているか、指定した行がない可能性があります。発見された可能性　「0か0よりも小さい・その行が存在しない」")
                quit()
            path = linecache.getline('data/minecraft-dir-list.txt', int(values[0])).strip()
            minecraft.minecraft_exec(values[2], values[1], path)


    window.close()

if __name__ == "__main__":
    main_run()