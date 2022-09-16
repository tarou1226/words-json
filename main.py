import sys
import json
import ndjson
import os
import subprocess

# ファイルのパスを定数として定義する
JSON_FALE_PATH = "lists.json"
NDJSON_FALE_PATH = "lists.ndjson"

def help():

    print("add                  add a word and description")
    print("show                 show word lists")
    print("delete               delete lists")

def add():

    while True:
        word = input("word:")
        description = input("description:")
        # wordかdescriptionが空白の場合、処理を戻す
        if(not word or not description):
            print("入力されていません\n")
            continue
        # 単語が数字のみの場合、処理を戻す
        elif(word.isdigit() == True):
            print("wordが数字のみで構成されています")
            print("やり直してください\n")
            continue
        # それ以外の場合、処理から抜け出す
        else:
            break
        
    # wordとdescriptionを辞書化する
    word_dict = {word: description}

    # ファイルが存在している場合、以下の処理を実行する
    if(os.path.exists(NDJSON_FALE_PATH) == True):
        # ndjsonファイルに追加記載する
        with open(NDJSON_FALE_PATH, 'a') as add_ndjson:
            writer = ndjson.writer(add_ndjson)
            writer.writerow(word_dict)
        # ndjsonファイルを読み込む
        with open(NDJSON_FALE_PATH, "r") as read_ndjson:
            data = ndjson.load(read_ndjson)
        # 読み込んだdataをjson方式に変換する
        data = json.dumps(data, indent = 4, ensure_ascii = False)
        # jsonファイルに書き込む
        with open(JSON_FALE_PATH, "w") as write_json:
            # jsonに書き込む際に、シングルコーテーションで囲まれていて
            # jsonファイルはダブルコーテーションでなければいけないので
            # replaceメソッドを使用して、変換する
            write_json.write(str(data).replace("'", '"'))
    # ファイルが存在しない場合、以下の処理を実行する
    else:
        # ndjsonファイルを作成、書き込む
        with open(NDJSON_FALE_PATH, mode = "w") as write_ndjson:
            writer = ndjson.writer(write_ndjson)
            writer.writerow(word_dict)
        # ndjsonファイルを読み込む
        with open(NDJSON_FALE_PATH, "r") as read_ndjson:
            data = ndjson.load(read_ndjson)
        # 読み込んだdataをjson方式に変換する
        data = json.dumps(data, indent = 4, ensure_ascii = False)
        # jsonファイルに書き込む
        with open(JSON_FALE_PATH, "w") as write_json:
            # jsonに書き込む際に、シングルコーテーションで囲まれていて
            # jsonファイルはダブルコーテーションでなければいけないので
            # replaceメソッドを使用して、変換する
            write_json.write(str(data).replace("'", '"'))
    
    print("add処理が終了しました")

def show():

    try:
        # 検索したいwordを打ち込む
        word = input("単語:")
        # jsonファイルを読み込む
        with open(JSON_FALE_PATH, "r") as read_json:
            show_data = json.load(read_json)
        # 読み込んだdataをlist化する
        show_data = list(show_data)
        # list内のキーから値を取得するgetメソッドを使用して
        # 全てのdataを調べる
        # 一致したら文字が取得でき、一致しない場合はNoneで返される
        word_dec = [i.get("{}".format(word)) for i in show_data]
        # Noneじゃないものをfilterメソッドで見つける
        # 見つけたものをlist化する
        word_dec_search = list(filter(lambda item: item != None, word_dec))
        # 条件に一致するものが一個でもあった場合
        if word_dec_search:
            # 取得した値をアンパックして出力する
            print(*word_dec_search)
        # 条件に一致するものがなかった場合
        else:
            # 存在していないことを知らせて
            # add関数を実行する
            print("wordが存在していません")
            print("wordを登録してください\n")
            add()
    # wordを一度も登録していないのに、showコマンドを実行した際の
    # 例外処理を挟む
    except FileNotFoundError:
        print("addコマンドを実行して、wordを登録してください")

    print("show処理が終了しました")

def delete():

    """
    今後の課題
    wordを入力したら、特定の単語が消える機能←こちらの開発
    allを入力したら、全てが消える機能
    cmd = input("word or all")
    if(cmd == "word"):
        word = input("word:")
    elif(cmd == "all"):
    """

    # jsonとndjsonのファイルを消去するのを
    # 自動で実行してくれる
    subprocess.run(["rm {}".format(JSON_FALE_PATH)], encoding = "utf-8", shell = True)
    subprocess.run(["rm {}".format(NDJSON_FALE_PATH)], encoding = "utf-8", shell = True)
    print("delete処理が終了しました")

def main():

    # sys.argv[index] = ["main.py", "[add] [show] [delete]"]
    try:
        # 入力したコマンドを取得する
        cmd = sys.argv[1]
        # addの場合
        if(cmd == "add"): 
            add()
        # showの場合
        elif(cmd == "show"):
            show()
        # deleteの場合
        elif(cmd == "delete"):
            delete()
        # それ以外の場合、help関数を実行する
        else:
            help()
            sys.exit()
    # commandが入力されていないと、cmdにardv[1]が挿入されないので
    # 例外処理を挟む
    except IndexError:
        print("commandを入力してください")
        print("usage: python main.py help")
    # control + c を押すと、強制終了されるので
    # 例外処理を挟む
    except KeyboardInterrupt:
        print("\n")
        print("強制終了しました")

if __name__ == "__main__":

    main()