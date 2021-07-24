from transitions import Machine
class Rules:
    def __init__(self):
        #システム意図
        self.system_intention = SystemIntention()
        #観光地データベースのモジュール?(後で作る)
        self.database = Database()
        # 観光地おすすめフェーズ進捗管理用
        self.recommend_done = {"target_first_introduce":0, "dummy_first_introduce":0, "ask_interest":0, "dummy_second_introduce":0, "target_second_introduce":0, "ask_question":0}
        

    #開始フェーズのルール
    def rule_phase_start(self):
        #response =  "はじめまして、今回観光地をご案内させていただく＊＊です。"
        #return response
        #self.system_intention.set("greet_start")
        result = {"general-greet": {"robot_name": "サトウ"}}
        return result


    #ユーザ情報収集フェーズのルール
    def rule_phase_collect(self, user_info, user_intent):
        if user_info["user_name"] == "null":
            #response = "お客様のお名前を伺ってもよろしいでしょうか"
            #self.system_intention.set("request_user_name")
            restlt =  {"request-user_name": {}}
            return restlt
        elif user_info["target_genre_like"] == "null" and user_info["target_genre_like"] == "null":
            """
            target_name = self.database.get_name(user_info["target_id"])
            dummy_name = self.database.get_name(user_info["dummy_id"])
            genre_target = self.database.get_genre(user_info["target_id"], True)
            genre_dummy = self.database.get_genre(user_info["dummy_id"], True)
            genres = ""
            if genre_target == genre_dummy:
                genres = "{0}".format(genre_target)
            else:
                genres = "{0}や{1}".format(genre_dummy, genre_target)
            response = "お客様がご希望されたのは{0}と{1}ですね。{2}がお好きなんですか？".format(target_name, dummy_name, genres)
            return response
            """
            #self.system_intention.set("request_genre_like")
            result = {"request-genre_like": {}}
            result["request-genre_like"]["target_name"] = self.database.get_name(user_info["target_id"])
            result["request-genre_like"]["dummy_name"] = self.database.get_name(user_info["dummy_id"])
            result["request-genre_like"]["sight_genre"] = self.database.get_genre(user_info["target_id"], True) + "・" + self.database.get_genre(user_info["dummy_id"], True)
            return result
        
        elif user_info["target_experience"] == "null" and user_info["dummy_experience"] == "null":
            #target_name = self.database.get_name(user_info["target_id"])
            #response = "今回選ばれた観光地に行ったことがあるか順番にお聞きしたいです。{0}に行ったことはありますか？".format(target_name)
            #return response
            #self.system_intention.set("request_target_experience")
            result = {"request-target_experience": {}}
            result["request-target_experience"]["user_name"] = user_info["user_name"]
            result["request-target_experience"]["target_name"] = self.database.get_name(user_info["target_id"])
            return result

        elif user_info["dummy_experience"] == "null":
            #dummy_name = self.database.get_name(user_info["dummy_id"])
            #response = "{0}はどうですか？".format(dummy_name)
            #return response
            #self.system_intention.set("request_dummy_experience")
            result = {"request-dummy_experience": {}}
            result["request-dummy_experience"]["dummy_name"] = self.database.get_name(user_info["dummy_id"])
            return result
        
        elif user_info["fellow_travellers"] == "null":
            #response = "今回はお1人でご旅行ですか？それとも誰かと一緒に行かれますか？"
            #return response
            #self.system_intention.set("request_fellow_travellers")
            result = {"request-companion_type": {}}
            return result

        elif user_info["with_child"] == "null":
            #response = "小さいお子様もご一緒ですか？"
            #return response
            #self.system_intention.set("request_with_child")
            result = {"request-with_child": {}}
            return result
    """
    #終了フェーズ
    def rule_phase_end(self, user_info, user_intent):
        #user_name = user_info["user_name"]
        #response = "{0}様、本日はご利用いただきありがとうございました。".format(user_name)
        #return response
        self.system_intention.set("greet_end")
    """

#観光地おすすめフェーズ
class RulePhaseRecommend:
    #初期化（ステートマシンの定義：とりうる状態の定義、初期状態の定義、各種遷移と紐付くアクションの定義）
    def __init__(self, name):
        self.system_intention = SystemIntention()
        self.name = name
        #状態の定義
        self.states = ["start", "s11", "s12", "s13", "s21", "s22", "s23", "s24", "s25", "s3", "end"]
        self.machine = Machine(model=self, states=self.states, initial='start', auto_transitions=False)
        self.machine.add_transition(trigger='start_recommend_phase', source='start', dest='s11', before='start_s11')
        self.machine.add_transition(trigger='request_target_introduction', source='s11', dest='s21', before='s11_s21')
        self.machine.add_transition(trigger='except_request_target_introduction', source='s11', dest='s12', before='s11_s12')
        self.machine.add_transition(trigger='request_dummy_introduction', source='s12', dest='s22', before='s12_s22')
        self.machine.add_transition(trigger='except_reqtest_dummy_introduction', source='s12', dest='s13', before='s12_s13')
        self.machine.add_transition(trigger='inform_interest_dummy', source='s13', dest='s22', before='s13_s22')
        self.machine.add_transition(trigger='except_inform_interest_dummy', source='s13', dest='s21', before='s13_s21')
        self.machine.add_transition(trigger='except_answer_no', source='s22', dest='s3', before='s22_s24_s3')
        self.machine.add_transition(trigger='answer_no', source='s22', dest='s3', before='s22_s3')
        self.machine.add_transition(trigger='request_dummy_introduction', source='s21', dest='s3', before='s21_s25_s3')
        self.machine.add_transition(trigger='except_request_dummy_introduction', source='s21', dest='s3', before='s21_s3')
        self.machine.add_transition(trigger='except_answer_no', source='s3', dest='s4', before='s3_s4')
        self.machine.add_transition(trigger='answer_no', source='s3', dest='s5', before='s3_s5')
        self.machine.add_transition(trigger='except_nothing', source='s4', dest='s4', before='s4_s4')
        self.machine.add_transition(trigger='nothing', source='s4', dest='s3', before='s4_s3')
        self.machine.add_transition(trigger='nothing', source='s5', dest='s5', before='s5_s5')
        self.machine.add_transition(trigger='except_nothing', source='s5', dest='s4', before='s5_s4')
        #self.machine.add_transition(trigger='except_answer_no', source='s3', dest='s3', before='s3_s3')
        #self.machine.add_transition(trigger='answer_no', source='s3', dest='end_user', before='all_end_user')
        #終了フェーズ
        #状態増やしたらここにも書き足すこと
        self.machine.add_transition(trigger='time_up', source=['start', 's11', 's12', 's13', 's21', 's22', 's3', 's4', 's5'], dest='end_timeup', before='all_end_timeup')



    """
    #発話
    def utterance_s11(self, user_info):
        target_experience = user_info["target_experience"]
        if target_experience == "yes":
            target_name = self.database.get_name(user_info["target_id"])
            summary = self.database.get_summary(user_info["target_id"], "first")
            response = "{0}への旅行経験があるということでしたが、一応簡単に紹介させていただきます。{1}は{2}です。".format(target_name, target_name, summary)
            return response
        else:
            target_name = self.database.get_name(user_info["target_id"])
            summary = self.database.get_summary(user_info["target_id"], "first")
            response = "{0}への旅行経験がないということなので、手短に紹介させていただきます。{1}は{2}です。".format(target_name, target_name, summary)
            return response
    def utterance_s12(self, user_info):
        dummy_experience = user_info["dummy_experience"]
        if dummy_experience == "yes":
            dummy_name = self.database.get_name(user_info["dummy_id"])
            summary = self.database.get_summary(user_info["dummy_id"], "first")
            response = "{0}への旅行経験があるということでしたが、一応簡単に紹介させていただきます。{1}は{2}です。".format(dummy_name, dummy_name, summary)
            return response
        else:#今はunknownも含まれてるからunknownは分けた方がいいかも？
            dummy_name = self.database.get_name(user_info["dummy_id"])
            summary = self.database.get_summary(user_info["dummy_id"], "first")
            response = "{0}への旅行経験がないということなので、簡単に紹介させていただきます。{1}は{2}です。".format(dummy_name, dummy_name, summary)
            return response
    def utterance_s21(self, user_info):
        response = ""
        target_experience = user_info["target_experience"]
        genre_like = user_info["genre_like"]
        user_name = user_info["user_name"]
        target_name = self.database.get_name(user_info["target_id"])
        genre_target = self.database.get_genre(user_info["target_id"], True)
        summary = self.database.get_summary(user_info["target_id"]["target_second"])
        if genre_like == "positive":
            if target_experience == "yes":
                response += "{0}が好きな{1}様には{2}がよりおすすめです。{3}は{4}なのでおすすめです。".format(genre_target, user_name, target_name, target_name, summary)
            elif target_experience == "no":
                response += "{0}が好きな{1}様には{2}がよりおすすめです。{3}は{4}なのでおすすめです。".format(genre_target, user_name, target_name, target_name, summary)
            else:#"null", "unkonown"
                response += "{0}が好きな{1}様には{2}がよりおすすめです。{3}は{4}なのでおすすめです。".format(genre_target, user_name, target_name, target_name, summary)
        elif genre_like == "negative":
            if target_experience == "yes":
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
            elif target_experience == "no":
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
            else:#"null", "unkonown"
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
        else:#"null","unknown"
            if target_experience == "yes":
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
            elif target_experience == "no":
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
            else:#"null", "unkonown"
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
        if (user_info["with_child"] == "yes") and (self.database.get_child_recommend(user_info["target_id"]) == "おすすめ"):
            response += "また、お子さまにもおすすめです。"
        return response
    def utterance_s22(self, user_info):
        dummy_name = self.database.get_name(user_info["dummy_id"])
        summary = self.database.get_summary(user_info["dummy_id"], "dummy_second")
        response = "{0}についてもっと詳しく説明させていただきます。{1}は{2}です。".format(dummy_name, dummy_name, summary)
        #s23に相当する部分
        target_name = self.database.get_name(user_info["target_id"])
        response += "{0}についておすすめさせてもらってもいいですか？"
        return response
    def utterance_s13(self, user_info):
        response = "どちらにより興味がおありですか？"
        return response
    def utterance_s3_froms24(self, user_info):
        #s24
        response = ""
        target_experience = user_info["target_experience"]
        genre_like = user_info["genre_like"]
        user_name = user_info["user_name"]
        target_name = self.database.get_name(user_info["target_id"])
        genre_target = self.database.get_genre(user_info["target_id"], True)
        summary = self.database.get_summary(user_info["target_id"]["target_second"])
        if genre_like == "positive":
            if target_experience == "yes":
                response += "{0}が好きな{1}様には{2}がよりおすすめです。{3}は{4}なのでおすすめです。".format(genre_target, user_name, target_name, target_name, summary)
            elif target_experience == "no":
                response += "{0}が好きな{1}様には{2}がよりおすすめです。{3}は{4}なのでおすすめです。".format(genre_target, user_name, target_name, target_name, summary)
            else:#"null", "unkonown"
                response += "{0}が好きな{1}様には{2}がよりおすすめです。{3}は{4}なのでおすすめです。".format(genre_target, user_name, target_name, target_name, summary)
        elif genre_like == "negative":
            if target_experience == "yes":
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
            elif target_experience == "no":
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
            else:#"null", "unkonown"
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
        else:#"null","unknown"
            if target_experience == "yes":
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
            elif target_experience == "no":
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
            else:#"null", "unkonown"
                response += "私は{0}が{1}なのでおすすめです。".format(target_name, summary)
        if (user_info["with_child"] == "yes") and (self.database.get_child_recommend(user_info["target_id"]) == "おすすめ"):
            response += "また、お子さまにもおすすめです。"
        #s3
        response += "営業時間やアクセス方法など何かお聞きになりたいことはありますか？"
        return response
    def utterance_s3_froms22(self, user_info):
        response = "それでは営業時間やアクセス方法など何かお聞きになりたいことはありますか？"
        return response
    def utterance_s3_froms25(self, user_info):
        #s25
        dummy_name = self.database.get_name(user_info["dummy_id"])
        summary = self.database.get_summary(user_info["dummy_id"], "dummy_second")
        response = "{0}についてもっと詳しく説明させていただきます。{1}は{2}です。".format(dummy_name, dummy_name, summary)
        #s3
        response += "営業時間やアクセス方法など何かお聞きになりたいことはありますか？"
        return response
    def utterance_s3_froms21(self, user_info):
        response = "それでは営業時間やアクセス方法など何かお聞きになりたいことはありますか？"
        return response
    def utterance_s3_s3(self, user_info):
        response = "ユーザの質問に答える発話"
        return response
    def utterance_s3_end(self, user_info):
        response = "わかりました。"
        return response
    """

    #以下、遷移時のアクション
    def start_s11(self, user_info):
        #self.system_intention.set("introuce_target")
        #response = self.utterance_s11(user_info)
        #return response
        result = {"introduce-target": {}}
        result["introduce-target"]["target_name"] = self.database.get_name(user_info["target_id"])
        result["introduce-target"]["target_summarry"] = self.database.get_summary(user_info["target_id"])
        return result
    def s11_s12(self, user_info):
        #self.system_intention.set("introduce_dummy")
        #response = self.utterance_s12(user_info)
        #return response
        result = {"introduce-dummy": {}}
        result["introduce-dummy"]["dummy_name"] = self.database.get_name(user_info["dummy_id"])
        result["introduce-dummy"]["dummy_summarry"] = self.database.get_summary(user_info["dummy_id"])
        return result
    def s11_s21(self, user_info):
        #self.system_intention.set("recommend_target")
        #response = self.utterance_s21(user_info)
        #return response
        result = {"recommend-target": {}}
        result["recommend-target"]["target_name"] = self.database.get_name(user_info["target_id"])
        result["recommend-target"]["target_summarry"] = self.database.get_summary(user_info["target_id"])
        return result
    def s12_s22(self, user_info):
        #introduce_dummyもする
        #self.system_intention.set("introduce_dummy")
        #self.system_intention.set("suggest_target")
        #response = self.utterance_s22(user_info)
        #return response
        result = {"introduce-dummy": {}, "suggest-target": {}}
        result["introduce-dummy"]["dummy_name"] = self.database.get_name(user_info["dummy_id"])
        result["introduce-dummy"]["dummy_summarry"] = self.database.get_summary(user_info["dummy_id"])
        result["suggest-target"]["target_name"] = self.database.get_name(user_info["target_id"])
        return result
    def s12_s13(self, user_info):
        #self.system_intention.set("ask_interest_sight")
        #response = self.utterance_s13(user_info)
        #return response
        result = {"ask-interest_sight": {}}
        return result
    def s13_s21(self, user_info):
        #self.system_intention.set("recommend_target")
        #response = self.utterance_s21(user_info)
        #return response
        result = {"introduce-target": {}}
        result["introduce-target"]["target_name"] = self.database.get_name(user_info["target_id"])
        result["introduce-target"]["target_summarry"] = self.database.get_summary(user_info["target_id"])
        return result
    def s13_s22(self, user_info):
        #introduce_dummyもする
        #self.system_intention.set("introduce_dummy")
        #self.system_intention.set("suggest_target")
        #response = self.utterance_s22(user_info)
        #return response
        result = {"introduce-dummy": {}, "suggest-target": {}}
        result["introduce-dummy"]["dummy_name"] = self.database.get_name(user_info["dummy_id"])
        result["introduce-dummy"]["dummy_summarry"] = self.database.get_summary(user_info["dummy_id"])
        result["suggest-target"]["target_name"] = self.database.get_name(user_info["target_id"])
        return result
    def s22_s24_s3(self, user_info):
        #s24
        #self.system_intention.set("recommend_target")
        #self.system_intention.set("ask_for_question")
        #response = self.utterance_s3_froms24(user_info)
        #return response
        result = {"recommend-target": {}, "ask-for_question": {}}
        result["recommend-target"]["target_name"] = self.database.get_name(user_info["target_id"])
        result["recommend-target"]["target_summarry"] = self.database.get_summary(user_info["target_id"])
        result["ask-for_question"]["example_slot_1"] = "料金"
        result["ask-for_question"]["example_slot_2"] = "アクセス方法"
        return result
    def s22_s3(self, user_info):
        #self.system_intention.set("ask_for_question")
        #response = self.utterance_s3_froms22(user_info)
        #return response
        result = { "ask-for_question": {}}
        result["ask-for_question"]["example_slot_1"] = "料金"
        result["ask-for_question"]["example_slot_2"] = "アクセス方法"
        return result
    def s21_s25_s3(self, user_info):
        #s25
        #self.system_intention.set("introduce_dummy")
        #self.system_intention.set("ask_for_question")
        #response = self.utterance_s3_froms25(user_info)
        #return response
        result = {"introduce-dummy": {}, "ask-for_question": {}}
        result["introduce-dummy"]["dummy_name"] = self.database.get_name(user_info["dummy_id"])
        result["introduce-dummy"]["dummy_summarry"] = self.database.get_summary(user_info["dummy_id"])
        result["ask-for_question"]["example_slot_1"] = "料金"
        result["ask-for_question"]["example_slot_2"] = "アクセス方法"
        return result
    def s21_s3(self, user_info):
        #self.system_intention.set("ask_for_question")
        #response = self.utterance_s3_froms21(user_info)
        #return response
        result = { "ask-for_question": {}}
        result["ask-for_question"]["example_slot_1"] = "料金"
        result["ask-for_question"]["example_slot_2"] = "アクセス方法"
        return result
    """
    def s3_s3(self, user_info):
        #self.system_intention.set("ask_for_question")
        #response = self.utterance_s3_froms3(user_info)
        #return response
        result = { "ask-for_question": {}}
        result["ask-for_question"]["example_slot_1"] = "料金"
        result["ask-for_question"]["example_slot_2"] = "アクセス方法"
        return result
    """
    def s3_s4(self, user_info):
        result = { "ask-for_question": {}}
        result["ask-for_question"]["example_slot_1"] = "料金"
        result["ask-for_question"]["example_slot_2"] = "アクセス方法"
        return result
    def s3_s5(self, user_info, user_intent):
        system_intent = { "inform-for_continue": {}}
        slot = "time"
        system_slot = "sight_{}".format(slot) # sight_time
        answer_value = self.database.get_question_answer(slot) # 無休
        result = {system_intent: {system_slot: answer_value}}
        return result
    def s4_s4(self, user_info, user_intent):
        # user_intent  = "request-time"
        slot = user_intent.replace("request-", "")
        system_intent = "answer-{}".format(slot) # answer-time
        system_slot = "sight_{}".format(slot) # sight_time
        answer_value = self.database.get_question_answer(slot) # 無休
        result = {system_intent: {system_slot: answer_value}}
        return result
    def s4_s3(self, user_info, user_intent):
        result = { "ask-for_question": {}}
        result["ask-for_question"]["example_slot_1"] = "料金"
        result["ask-for_question"]["example_slot_2"] = "アクセス方法"
        return result
    def s5_s5(self, user_info, user_intent):
        system_intent = { "inform-for_continue": {}}
        slot = "time"
        system_slot = "sight_{}".format(slot) # sight_time
        answer_value = self.database.get_question_answer(slot) # 無休
        result = {system_intent: {system_slot: answer_value}}
        return result
    def s5_s4(self, user_info, user_intent):
        slot = user_intent.replace("request-", "")
        system_intent = "answer-{}".format(slot) # answer-time
        system_slot = "sight_{}".format(slot) # sight_time
        answer_value = self.database.get_question_answer(slot) # 無休
        result = {system_intent: {system_slot: answer_value}}
        return result
    def all_end_timeup(self, user_info):
        #self.system_intention.set("phase_end_timeup")
        result = {"general-bye": {}}
        return result

if __name__ == "__main__":
    
    user_info = {"user_name":"null", "target_id":"80028808", "dummy_id":"80028943", "genre_like":"null", "target_experience":"null", "dummy_experience":"null", "companion_type":"null", "with_child":"null", "interest_id":"null"}
    class SystemIntention():
        def __init__(self):
            self.intent = "nannan"
        def set(self, systemintention):
            self.intent = systemintention
    class Database():
        def __init__(self):
            self.a = 8

    rule = Rules()
