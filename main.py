import sys
import json
import ndjson
import os


#def usage():
#    # Linuxのようなhelpを作成する。
#    print("add command:python main.py add [tango] [description]")
#    print("show command:python main.py show [tango]")

def add():

    tango = input("単語:")
    description = input("説明:")

    tango_dict = {tango: description}

    if(os.path.exists("lists.ndjson") == True):
        print("ファイルが存在します")
        with open("lists.ndjson", 'a') as f:
            writer = ndjson.writer(f)
            writer.writerow(tango_dict)
        with open("lists.ndjson") as f:
            data = ndjson.load(f)
            data = json.dumps(data, indent = 4, ensure_ascii = False)
        with open("lists.json", "w") as f:
            f.write(str(data).replace("'", '"'))

    else:
        print("ファイルが存在しません")
        with open("lists.ndjson", mode = "w") as f:
            writer = ndjson.writer(f)
            writer.writerow(tango_dict)
        with open("lists.ndjson") as f:
            data = ndjson.load(f)
            data = json.dumps(data, indent = 4, ensure_ascii = False)
        with open("lists.json", "w") as f:
            f.write(str(data).replace("'", '"'))

def show():
    tango = input("単語:")
    with open("lists.json") as f:
        show_data = json.load(f)
    show_data = list(show_data)
    word_dec = [i.get("aaa") for i in show_data]
    print(*list(filter(lambda item: item != None, word_dec)))


    #print("show func")


def main():
    # コマンドがない場合の処理
    #if(len(sys.argv) < 2):
    #    usage()
    #    sys.exit()
    # sys.argv[index] = ["main.py", "add/show"]
    cmd = sys.argv[1]

    if(cmd == "add"): 
        add()
    elif(cmd == "show"):
        show()
    else:
        usage()
        sys.exit()  

if __name__ == "__main__":
    main()