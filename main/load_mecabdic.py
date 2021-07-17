import MeCab
# import mecab as mecab_setting

# mecab = MeCab.Tagger("-r {} -d {}".format(mecab_setting.MECAB_RC_DIR["/etc/mecabrc"], mecab_setting.MECAB_DIC_DIR["/home/higashinakalab/dev/mecab-ipadic-neologd"]))
# mecab = MeCab.Tagger("-r {} -d {}".format("/etc/mecabrc", "/home/higashinakalab/dev/mecab-ipadic-neologd"))
mecab = MeCab.Tagger("-r {} -d {}".format("/etc/mecabrc", "/usr/lib/mecab/dic/mecab-ipadic-neologd"))
mecab.parse('')