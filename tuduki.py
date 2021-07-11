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
