import json
from os import replace
import re
from load_mecabdic import mecab

class Tourist_DB:
    def __init__(self, data_id, key):
        data_name = data_id + ".json"
        data_open = open(data_name, 'r')
        self.data = json.load(data_open)
        # self.id = os.path.splitext(os.path.basename(data))[0]
        self.sightlist_element = self.data[0]["SightList"][0][key]

    def get_name(self, SightID):
        data_name = SightID + ".json"
        data_open = open(data_name, 'r')
        data = json.load(data_open)
        return data[0]["SightList"][0]["Title"]

    def load_element(self):
        return self.sightlist_element

    def print_SightList_element(self):
        # print(self.data[0]["SightList"][0][key])
        print(self.sightlist_element)


# a = Tourist_DB("80010838", "Title")
# a.print_SightList_element()
# b = a.load_element()
# print(b)


def get_name(SightID):
    data_name = SightID + ".json"
    data_open = open(data_name, 'r')
    data = json.load(data_open)
    return data[0]["SightList"][0]["Title"]

# a = get_name("80010838")
# print(a)


def get_genre(SightID, seikei=True):
    data_name = SightID + ".json"
    data_open = open(data_name, 'r')
    data = json.load(data_open)
    genre = "null"
    if seikei:
        whichGenre = 0
        genrelist = data[0]["SightList"][0]["GenreList"][whichGenre]
        # print(genrelist)
        new_genrelist = []
        vocabs = []
        maxlen_genre = ""
        genre = ""
        for i,genre_type in enumerate(genrelist.values()):
            if genre_type["Name"] == "その他":
                new_genrelist.append("")
                vocabs.append([""])
                continue
            new_genrelist.append(genre_type["Name"])
            vocabs.append(genre_type["Name"].split("・"))
        maxlen_genre = max(new_genrelist, key=len)
        maxlen_genre_index = new_genrelist.index(max(new_genrelist, key=len))
        print(maxlen_genre)
        print(maxlen_genre_index)
        print(vocabs)
        for i,vocab in enumerate(vocabs):
            print(vocab)
            if i==maxlen_genre_index:
                continue
            for voc in vocab:
                if voc in vocabs[maxlen_genre_index]:
                    genre += voc+"や"
        if genre=="":
            genre = maxlen_genre.replace("・", "や")
            # if i>0 and len(new_genrelist[i])>len(new_genrelist[i-1]) and vocabs[i-1]!="その他":
            #     for vocab in vocabs[i-1]:
            #         if vocab in new_genrelist[i]:
            #     # if new_genrelist[i-1] in new_genrelist[i] or vocabs[i-1]:
            #             # genre = new_genrelist[i-1]
            #             genre += vocab
            # elif i>0 and len(new_genrelist[i])<len(new_genrelist[i-1]):
            #     for vocab in vocabs[i]:
            #         if vocab in new_genrelist[i-1]:
            #     # if new_genrelist[i] in new_genrelist[i-1]:
            #             # genre = new_genrelist[i]
            #             genre += vocab
                # maxlen_genre = genre_type["Name"]
            # genre_type["Name"] = genre_type["Name"].replace("・", "や",1).replace("・", "、もしくは",1)
        # if new_genrelist in max(new_genrelist, key=len):
        # genre = new_genrelist
    # return max(genre, key=len)
    return genre.rstrip("や")

# id = "80010918"
# a = get_genre(id)
# print(a)


def _parse_text(text):
    parsed_text = []
    for line in mecab.parse(text).splitlines():
        # print(line)
        if line == "EOS":
            break
        else:
            surface, features = line.split("\t")
            parsed_text.append([surface] + features.split(","))
    # print(parsed_text)
    return parsed_text


def _modify_text_tail(text):
    parsed_text = _parse_text(text)
    # print(parsed_text)
    
    if len(parsed_text) < 2:
        print("modify_texts:: parsed_text {}".format(parsed_text))
    pre_tail_token, tail_token = parsed_text[-2], parsed_text[-1]
    modified_pre_tail_word, modified_tail_word = "", ""

    if tail_token[1] == "名詞":
        # 1-1. 名詞の場合
        if tail_token[2] == "サ変接続":
            modified_tail_word = tail_token[0] + "したものです"
        elif tail_token[2] == "固有名詞" and tail_token[3] == "一般":
            modified_tail_word = tail_token[0] + "しました"
        else:
            modified_tail_word = tail_token[0] + "です"

    elif tail_token[1] == "動詞":
        if tail_token[2] == "自立":
            if tail_token[5] == "一段" and tail_token[7] == "できる":
                modified_tail_word = "できます"
            elif tail_token[5] == "五段・ラ行" and tail_token[6] == "基本形":
                modified_tail_word = tail_token[0].replace("る", "ります")

        elif tail_token[2] == "非自立":
            # print("非自立", tail_token[5], tail_token[7])
            if tail_token[5] == "一段" and tail_token[7] == "いる":
                modified_tail_word = "います"
    
    elif tail_token[1] == "助動詞":
        if tail_token[-1] == "タ":
            if pre_tail_token[1] == "動詞" and pre_tail_token[2] == "自立" and pre_tail_token[5] == "サ変・スル":
                modified_pre_tail_word, modified_tail_word = "しま", "した"

        elif tail_token[-1] == "ダ":
            if tail_token[5] == "特殊・ダ" and tail_token[6] == "基本形":
                modified_tail_word = "ですよ"

    # 3. 文の単語リストを作成
    # 3-1. 末尾二つ以外
    word_list = [token[0] for token in parsed_text[:-2]]
    
    # 3-2. 末尾から二つ目をmodifyしていれば置き換え
    if modified_pre_tail_word:
        word_list.append(modified_pre_tail_word)
    else:
        word_list.append(parsed_text[-2][0])

    # 3-3. 末尾modifyしていれば置き換え
    if modified_tail_word:
        word_list.append(modified_tail_word)
    else:
        word_list.append(parsed_text[-1][0])
    # <<< 読点分割 <<<

    # 4. 文章に復元
    return "".join(word_list)




def get_summary(SightID, state="first"):
    data_name = SightID + ".json"
    data_open = open(data_name, 'r')
    data = json.load(data_open)
    all_summary = data[0]["SightList"][0]["Summary"]
    summary_list = all_summary.split("。")
    summary_list = [summary+"。" for summary in summary_list]
    summary_list.pop(-1)
    if state == "first":
        total_textnumber = 0
        i = 0
        first_summary = ""
        while total_textnumber < 20:
            total_textnumber+=len(summary_list[i])
            first_summary += summary_list[i]
            i+=1
        print("Before:",first_summary)
        return _modify_text_tail(first_summary.rstrip("。"))+"。"
    elif state == "dummy_second":
        print("Before:",summary_list[1])
        return _modify_text_tail(summary_list[1].rstrip("。"))+"。"
    elif state=="target_second":
        target_second_list = []
        for summary in summary_list[1:]:
            target_second_list.append(_modify_text_tail(summary.rstrip("。"))+"。")
        print("Before:",summary_list[1:])
        return target_second_list
    # return summary_list


# id = "80010838"
# a = get_summary(id, "dummy_second")
# print("After :",a)
# for i in a:
#     print(i)


def get_child_recommend(SightID):
    data_name = SightID + ".json"
    data_open = open(data_name, 'r')
    data = json.load(data_open)
    option_list = data[0]["SightList"][0]["SightOptionList"]
    for option in option_list:
        if option["SightOptionName"]=="ベビーおすすめ" or option["SightOptionName"]=="キッズおすすめ":
            if option["SightOptionLevelName"]=="おすすめ":
                return "おすすめ"
            
    return "Not おすすめ"


# a = get_child_recommend("80010918")
# print(a)


def get_question_answer(SightID, question):
    data_name = SightID + ".json"
    data_open = open(data_name, 'r')
    data = json.load(data_open)
    answer_area = data[0]["SightList"][0]
    def make_raw(q,add=""):
        if q.capitalize()+add in answer_area: return answer_area[q.capitalize()+add]
        else: return ""
    if question!="traffic":raw_ans = make_raw(question)
    if question=="address":
        answer = "住所は" + raw_ans
    elif question=="time":
        num_line_pattern = r'\d+[～]+'
        numline_search = re.search(num_line_pattern,raw_ans)
        any_line_pattern = r'.[～]+'
        anyline_search = re.search(any_line_pattern,raw_ans)
        if numline_search:
            replace_str = numline_search.group().replace('～','時から')
            answer = "時間は" + re.sub(num_line_pattern,replace_str,raw_ans)
            if re.search(any_line_pattern,answer).group():
                replace_str = re.search(any_line_pattern,answer).group().replace('～','から')
                answer = re.sub(any_line_pattern,replace_str,answer)
        elif anyline_search:
            replace_str = anyline_search.group().replace('～','から')
            answer = "時間は" + re.sub(r'.[～]+',replace_str,raw_ans)
        else:
            if "自由" in raw_ans:
                answer = raw_ans.replace("自由","は自由")
            else:
                answer = raw_ans
    elif question=="closed":
        answer = raw_ans.replace("曜","曜日").replace("(","、").replace(")","")
    elif question=="price":
        answer = raw_ans.replace("自由","無料")
    elif question=="traffic":
        raw_ans_1 = make_raw(question,add="1")
        raw_ans_2 = make_raw(question,add="2")
        answer1 = raw_ans_1.replace("→","から")
        answer2 = raw_ans_2.replace("m","mで")
        if answer2 != "": answer = answer1 + "です、また運転する場合、" + answer2 + "です"
        else: answer = answer1 + "です"
    elif question=="station":
        print(raw_ans["Name"])
        pref = re.search(r'（.*）',raw_ans["Name"]).group()
        answer = "最寄り駅は" + pref.lstrip("（").rstrip("）") + "の" + raw_ans["Name"].replace(pref,"")
    else:
        answer = "I don't know"
    return _modify_text_tail(answer)



id = "80011585"
question ="station"
a = get_question_answer(id, question)
print(a)