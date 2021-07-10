import json
import os

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
        for genre_type in genrelist.values():
            if genre_type["Name"] == "その他":
                continue
            # if "・" in genre_type["Name"]:
            genre_type["Name"] = genre_type["Name"].replace("・", "や",1).replace("・", "、もしくは",1)
            new_genrelist.append(genre_type["Name"])
        genre = new_genrelist
    return max(genre, key=len)


a = get_genre("80010918")
# a = get_genre("80011612")
print(a)