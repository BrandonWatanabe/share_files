import rule
import json


class PhaseManager:
    def __init__(self):
        # self.phase = phase
        self.rule_phase = rule.Rules()

    def phases_flow(self, user_info, user_intent):
        # result = self.rule_phase.rule_phase_start()
        while True:
            result = self.rule_phase.rule_phase_collect(user_info, user_intent)
            if result==None: break


a = PhaseManager()
user_info = {"user_name":"null", "target_genre_like":"null", "target_experience":"null"}
a.phases_flow()