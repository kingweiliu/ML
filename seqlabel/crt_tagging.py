# https://www.biaodianfu.com/crf.html
"""
利用人民日报199801的标注语料，生成hmm和crf需要的数据格式
"""
data_dir = "./data/"

def split_word(words):
    li = list()
    for word in words:
        li.append(word)
    return li


# 4 tag
# S/B/E/M
def get4tag(li):
    length = len(li)
    if length == 1:
        return ['S']
    elif length == 2:
        return ['B', 'E']
    elif length > 2:
        li = list()
        li.append('B')
        for i in range(0, length - 2):
            li.append('M')
        li.append('E')
        return li


# 6 tag
# S/B/E/M/M1/M2
def get6tag(li):
    length = len(li)
    if length == 1:
        return ['S']
    elif length == 2:
        return ['B', 'E']
    elif length == 3:
        return ['B', 'M', 'E']
    elif length == 4:
        return ['B', 'M1', 'M', 'E']
    elif length == 5:
        return ['B', 'M1', 'M2', 'M', 'E']
    elif length > 5:
        li = list()
        li.append('B')
        li.append('M1')
        li.append('M2')
        for i in range(0, length - 4):
            li.append('M')
        li.append('E')
        return li

def save_hmm_data_file(filehandle, word, handle, tag):
    if len(word) == 0:
        filehandle.write("\n")
    elif len(word) == 1:
        filehandle.write(word + "/S ")
    elif len(word) == 2:
        filehandle.write(word[0] + "/B " + word[1] + "/E ")
    else:
        filehandle.write(word[0] + "/B " + " ".join(c + "/M" for c in word[1:-1]) + " " + word[-1] + "/E ")


def save_data_file(train_obj, test_obj, hmm_train_obj, hmm_test_obj, is_test, word, handle, tag):
    if is_test:
        save_train_file(test_obj, word, handle, tag)
        save_hmm_data_file(hmm_test_obj, word, handle, tag)

    else:
        save_train_file(train_obj, word, handle, tag)
        save_hmm_data_file(hmm_train_obj, word, handle, tag)

def save_train_file(fiobj, word, handle, tag):
    if len(word) > 0:
        wordli = split_word(word)
        if tag == '4':
            tagli = get4tag(wordli)
        if tag == '6':
            tagli = get6tag(wordli)
        for i in range(0, len(wordli)):
            w = wordli[i]
            h = handle
            t = tagli[i]
            fiobj.write(w + '\t' + h + '\t' + t + '\n')
    else:
        # print 'New line'
        fiobj.write('\n')


# B,M,M1,M2,M3,E,S
def convert_tag(filename, tag):
    tag = str(tag)
    fi_obj = open(data_dir + filename, 'r', encoding='utf-8')
    train_obj = open(data_dir + filename + tag + '.crf.train.data', 'w', encoding='utf-8')
    test_obj = open(data_dir + filename + tag + '.crf.test.data', 'w', encoding='utf-8')
    hmm_train_obj = open(data_dir + filename + tag + '.hmm.train.data', 'w', encoding='utf-8')
    hmm_test_obj = open(data_dir + filename + tag + '.hmm.test.data', 'w', encoding='utf-8')

    arr = fi_obj.readlines()
    i = 0
    for a in arr:
        i += 1
        a = a.strip('\r\n\t ')
        if a == "":
            continue
        words = a.split(" ")
        test = False
        if i % 10 == 0:
            test = True
        for word in words:
            # print("---->", word)
            word = word.strip('\t ')
            if len(word) > 0:
                i1 = word.find('[')
                if i1 >= 0:
                    word = word[i1 + 1:]
                i2 = word.find(']')
                if i2 > 0:
                    w = word[:i2]
                word_hand = word.split('/')
                w, h = word_hand
                if ']' in h:
                    h = h.split("]")[0]
                if h == 'nr':  # ren min
                    # print 'NR',w
                    if w.find('·') >= 0:
                        tmpArr = w.split('·')
                        for tmp in tmpArr:
                            save_data_file(train_obj, test_obj, hmm_train_obj, hmm_test_obj, test, tmp, h, tag)
                    else:
                        save_data_file(train_obj, test_obj, hmm_train_obj, hmm_test_obj, test, w, h, tag)
                    continue
                if h != 'm':
                    save_data_file(train_obj, test_obj, hmm_train_obj, hmm_test_obj, test, w, h, tag)

                # if h == 'w':
                #     save_data_file(train_obj, test_obj, hmm_train_obj, hmm_test_obj, test, "", "", tag)  # split

        save_data_file(train_obj, test_obj, hmm_train_obj, hmm_test_obj, test, "", "", tag)


    train_obj.flush()
    test_obj.flush()
    hmm_train_obj.flush()
    hmm_test_obj.flush()


if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print('tag[6,4] convert raw data to train.data and tag.test.data')
    # else:
    #     tag = sys.argv[1]
    #     convert_tag(tag)
    convert_tag("renminribao199801.txt", 4)