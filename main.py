import sys
import json
import ndjson
import os
import subprocess

#def usage():
#    # Linuxのようなhelpを作成する。
#    print("add command:python main.py add [tango] [description]")
#    print("show command:python main.py show [tango]")

JSON_FALE_PATH = "lists.json"
NDJSON_FALE_PATH = "lists.ndjson"

def add():

    while True:
        word: str = input("単語:")
        description: str = input("説明:")
        # wordかdescriptionが空白の場合、処理を戻す
        if(not word or not description):
            print("入力されていません\n")
            continue
        # 単語が数字のみの場合、処理を戻す
        elif(word.isdigit() == True):
            print("単語が数字のみで構成されています")
            print("やり直してください\n")
            continue
        else:
            break
    
    word_dict = {word: description}

    if(os.path.exists("lists.ndjson") == True):
        #print("ファイルが存在します")
        with open("lists.ndjson", 'a') as add_ndjson:
            writer = ndjson.writer(add_ndjson)
            writer.writerow(word_dict)
        with open("lists.ndjson", "r") as read_ndjson:
            data = ndjson.load(read_ndjson)
        data = json.dumps(data, indent = 4, ensure_ascii = False)
        with open("lists.json", "w") as write_json:
            write_json.write(str(data).replace("'", '"'))

    else:
        #print("ファイルが存在しません")
        with open("lists.ndjson", mode = "w") as write_ndjson:
            writer = ndjson.writer(write_ndjson)
            writer.writerow(word_dict)
        with open("lists.ndjson", "r") as read_ndjson:
            data = ndjson.load(read_ndjson)
        data = json.dumps(data, indent = 4, ensure_ascii = False)
        with open("lists.json", "w") as write_json:
            write_json.write(str(data).replace("'", '"'))
    
    print("add処理が終了しました")

def show():
    word = input("単語:")
    with open("lists.json", "r") as read_json:
        show_data = json.load(read_json)
    show_data = list(show_data)
    word_dec = [i.get("{}".format(word)) for i in show_data]
    word_dec_search = list(filter(lambda item: item != None, word_dec))
    if word_dec_search:
        print(*word_dec_search)
    else:
        print("wordが存在していません")
        print("wordを登録してください")

    print("show処理が終了しました")

def clear():
    """
    cmd = input("word or all")
    if(cmd == "word"):
        word = input("word:")

    elif(cmd == "all"):
    """
    subprocess.run(["rm {}".format(JSON_FALE_PATH)], encoding = "utf-8", shell = True)
    subprocess.run(["rm {}".format(NDJSON_FALE_PATH)], encoding = "utf-8", shell = True)
    print("clear処理が終了しました")

def main():
    # sys.argv[index] = ["main.py", "add/show/clear"]
    try:
        cmd = sys.argv[1]

        if(cmd == "add"): 
            add()
        elif(cmd == "show"):
            show()
        elif(cmd == "clear"):
            clear()
        else:
            usage()
            sys.exit()  
    except IndexError:
        print("commandを入力してください")
    except KeyboardInterrupt:
        print("\n")
        print("強制終了しました")

if __name__ == "__main__":
    main()