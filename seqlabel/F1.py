
def crf_result_f1(filename):
    with open(rst_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
        wc_of_test = 0
        wc_of_gold = 0
        wc_of_correct = 0
        flag = True

        for l in lines:
            if l == '\n': continue

            _, _, g, r = l.strip().split()

            if r != g:
                flag = False

            if r in ('E', 'S'):
                wc_of_test += 1
                if flag:
                    wc_of_correct += 1
                flag = True

            if g in ('E', 'S'):
                wc_of_gold += 1

        print("WordCount from test result:", wc_of_test)
        print("WordCount from golden data:", wc_of_gold)
        print("WordCount of correct segs :", wc_of_correct)

        # 查全率
        P = wc_of_correct / float(wc_of_test)
        # 查准率，召回率
        R = wc_of_correct / float(wc_of_gold)

        print("P = %f, R = %f, F-score = %f" % (P, R, (2 * P * R) / (P + R)))

def hmm_result_f1(result_file):
    with open(result_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
        wc_of_test = 0
        wc_of_gold = 0
        wc_of_correct = 0
        flag = True

        for ln in lines:
            for item in ln.strip().split(" "):

                if len(item) < 3 : continue

                _, g, r = item[0], item[2], item[4]

                if r != g:
                    flag = False

                if r in ('E', 'S'):
                    wc_of_test += 1
                    if flag:
                        wc_of_correct += 1
                    flag = True

                if g in ('E', 'S'):
                    wc_of_gold += 1

        print("WordCount from test result:", wc_of_test)
        print("WordCount from golden data:", wc_of_gold)
        print("WordCount of correct segs :", wc_of_correct)

        # 查全率
        P = wc_of_correct / float(wc_of_test)
        # 查准率，召回率
        R = wc_of_correct / float(wc_of_gold)

        print("P = %f, R = %f, F-score = %f" % (P, R, (2 * P * R) / (P + R)))


if __name__ == "__main__":
    rst_file = './crf/crf.4.test.log'
    crf_result_f1(rst_file)
    hmm_result_f1("data/renminribao199801.txt4.hmm.test.data.hmmret")