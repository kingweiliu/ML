"""
hmm 5要素
状态集：BMES
观察集： 所有的字符
状态转移矩阵： Aij ： 从状态i 到j的概率
发射矩阵：Bij ： 状态i观察到j的概率
初始概率 T
"""

from collections import defaultdict
import functools
import math

def hmm(inputfile):
    states = defaultdict(int)  # 状态计数
    observes = defaultdict(dict) # 观察汉字计数
    starts = defaultdict(int)  # 起始计数
    state_cond = defaultdict(dict)
    for line in inputfile:
        parts = line.strip().split()
        if len(parts) < 1:
            continue
        starts[parts[0][2]] += 1
        laststate = None
        for part in parts:
            currentstate=part[2]
            word = part[0]
            states[currentstate] += 1
            observes[currentstate][word] = observes[currentstate].get(word, 0) + 1;
            if laststate:
                state_cond[laststate][currentstate] = state_cond[laststate].get(currentstate, 0) + 1
            laststate = currentstate

    # 初始概率
    linecnt = functools.reduce(lambda x, y : starts[x] + starts[y], starts)
    print("初始概率")
    initprob = {}
    for x in states:
        print(x, ":", (starts.get(x, 0) + 1) / (linecnt + 1))
        initprob[x] = (starts.get(x, 0) + 1) / (linecnt + 1)

    print("发射概率")
    wordset = set()
    for x in observes:
        wordset = wordset.union(observes[x].keys())
    emitprob = defaultdict(dict)
    for state in observes:
        statecnt = states[state]
        for word in wordset:
            emitprob[state][word] = (observes[state].get(word, 0) + 1) / (statecnt + 1)
    for state in emitprob:
        idx = 0
        for word in emitprob[state]:
            print(state, "->", word, ":", emitprob[state][word])
            idx += 1
            if idx > 10:
                break
    print("状态转移")
    Astatetrans = defaultdict(dict)
    for state in state_cond:
        statecnt = sum([state_cond[state][x] for x in  state_cond[state]])
        for nextstate in states:
            Astatetrans[state][nextstate] = (state_cond[state].get(nextstate, 0) + 1) / (statecnt + 1)

    print(Astatetrans)
    #
    #
    # print(states)
    # print(observes)
    # print(state_cond)

    return Astatetrans, emitprob, initprob;


def hmm_seg(A, emitprob, initprob, sentence):

    c = sentence[0]
#    print(c)
    stepprob = {}
    laststate = None
    lastprob = -1e7
    for state in emitprob:
        stepprob[state] = math.log(initprob[state]) + math.log(emitprob[state].get(c, 1e-9));
        if (stepprob[state] > lastprob):
            lastprob = stepprob[state]
            laststate = state
#    print(c, laststate, lastprob)

    result = []
    result.append((c, laststate))

    for pos in range(1, len(sentence)):
        c = sentence[pos]
        tmpprob = -1e7
        tmpstate = None
        for state in stepprob:
            # print(laststate, "->",  state, c, stepprob[laststate], math.log(A[laststate][state]), math.log(emitprob[state][c]))
            stepprob[state] = math.log(A[laststate][state]) + math.log(emitprob[state].get(c, 1e-9))
            if stepprob[state] > tmpprob:
                tmpprob = stepprob[state]
                tmpstate = state
        laststate = tmpstate
        #print(c, laststate, tmpprob)
        result.append((c, laststate))

    ret = ""
    print(result)
    for (c, state) in result:
        ret += c
        if state == 'S' or state == 'E':
            ret += " "
    return ret

def hmm_seg_viterbi(A, emitprob, initprob, sentence):
    c = sentence[0]
    stepprob = {}
    for state in emitprob:
        stepprob[state] = math.log(initprob[state]) + math.log(emitprob[state].get(c, 1e-9))

    stateseq = {}
    for state in initprob:
        stateseq[state] = ""
#        print(state, stepprob[state])

    for pos in range(1, len(sentence)):
        c = sentence[pos]
        # print(c)
        newstepprob = {}
        newstateseq = {}

        for state in stepprob:
            tmpprob = -1e10
            tmpstate = None
            for laststate in stepprob:
                nextprob = stepprob[laststate] + math.log(A[laststate][state]) + math.log(emitprob[state].get(c, 1e-10))
                if nextprob > tmpprob:
                    tmpprob = nextprob
                    tmpstate = laststate

            newstepprob[state] = tmpprob
            newstateseq[state] = stateseq[tmpstate] + tmpstate

        stepprob = newstepprob
        stateseq = newstateseq
        # for st in stepprob:
        #     print(c, "---", stepprob[st], stateseq[st], "--->", st)

    tmpprob = -1e10
    tmpstate = None
    for state in stepprob:
        if stepprob[state] > tmpprob:
            tmpprob = stepprob[state]
            tmpstate = state
#    print(tmpstate)
    stateseq[tmpstate] = stateseq[tmpstate] + tmpstate
#   print(stateseq[tmpstate])
    result = zip(sentence, stateseq[tmpstate])
    print(stateseq[tmpstate])
    ret = ""
    laststate = None
    for (c, state) in result:
        if state == 'B':
            ret += " "
        ret += c
        if state == 'E' or state == 'S':
            ret += " "


    return ret

def hmm_label_viterbi(A, emitprob, initprob, sentence):

    c = sentence[0]
    stepprob = {}
    for state in emitprob:
        stepprob[state] = math.log(initprob[state]) + math.log(emitprob[state].get(c, 1e-9))

    stateseq = {}
    for state in initprob:
        stateseq[state] = ""
    #        print(state, stepprob[state])

    for pos in range(1, len(sentence)):
        c = sentence[pos]
        # print(c)
        newstepprob = {}
        newstateseq = {}

        for state in stepprob:
            tmpprob = -1e10
            tmpstate = None
            for laststate in stepprob:
                nextprob = stepprob[laststate] + math.log(A[laststate][state]) + math.log(emitprob[state].get(c, 1e-10))
                if nextprob > tmpprob:
                    tmpprob = nextprob
                    tmpstate = laststate

            newstepprob[state] = tmpprob
            newstateseq[state] = stateseq[tmpstate] + tmpstate

        stepprob = newstepprob
        stateseq = newstateseq
        # for st in stepprob:
        #     print(c, "---", stepprob[st], stateseq[st], "--->", st)

    tmpprob = -1e10
    tmpstate = None
    for state in stepprob:
        if stepprob[state] > tmpprob:
            tmpprob = stepprob[state]
            tmpstate = state
    #    print(tmpstate)
    stateseq[tmpstate] = stateseq[tmpstate] + tmpstate
    #   print(stateseq[tmpstate])
    result = list(zip(sentence, stateseq[tmpstate]))
    return result
    print(stateseq[tmpstate])


    return " ".join([c+"/" +state for (c, state) in result])


def label_test_data(filename, A, emitprob, initprob):
    """
    对已经标注好的句子分词，邓/B 小/M 平/E
    :param filename:
    :return:  邓/B/B 小/M/M 平/E/S
    """
    outputfile = open(filename+".hmmret", "w", encoding='utf8')

    with open(filename, "r", encoding='utf8') as nf:
        for line in nf:
            charpos = [x.split("/") for x in line.strip().split(" ")]
            origin_sent = "".join([c[0] for c in charpos])

            if len(origin_sent) == 0:
                print(line)
                continue
            ret_charpos = hmm_label_viterbi(A, emitprob, initprob, origin_sent)
            # print(charpos)
            # print(ret_charpos)
            if len(charpos) != len(ret_charpos):
                raise Exception("cuwu")
            outline = " ".join(("/".join([part[0][0], part[0][1], part[1][1]]) for part in zip(charpos, ret_charpos)))
            outputfile.write(outline + "\n")
    outputfile.close()






if __name__ == "__main__":
    A = None
    emitprob = None
    initprob = None
    with open("data/renminribao199801.txt4.hmm.train.data", encoding='utf8') as nf:
        A, emitprob, initprob = hmm(nf)
    ret = hmm_seg_viterbi(A, emitprob, initprob, "人类社会前进的航船就要驶入21世纪的新航程")
    print(ret)
    bb = hmm_label_viterbi(A, emitprob, initprob, "人类社会前进的航船就要驶入21世纪的新航程")
    print(bb)
    ret = hmm_seg(A, emitprob, initprob, "人类社会前进的航船就要驶入21世纪的新航程")
    print(ret)

    label_test_data("data/renminribao199801.txt4.hmm.test.data", A, emitprob, initprob)

    # result = []
    #
    # with open("icwb2-data/testing/pku_test.utf8", encoding='utf8') as rawfile:
    #     for line in rawfile:
    #         if len(line.strip()) == 0:
    #             continue
    #         ret = hmm_seg_viterbi(A, emitprob, initprob, line.strip())
    #         result.append(ret + "\n")
    # with open("data/hmm_seg_pku_test_viterbi.txt", "w", encoding='utf8') as outfile:
    #     outfile.writelines(result)