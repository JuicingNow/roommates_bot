import pandas as pd

class Dataworker():
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.data = self.df.values.tolist()

    def get_floor_list(self, floor):
        floor_list = []
        for person in self.data:
            if int(str(person[0])[0]) == floor:
                floor_list.append(str(person[0]))
        return sorted(list(set(floor_list)))
    
    def get_room_list(self, room):
        room_list = []
        for person in self.data:
            if person[0] == room:
                room_list.append(' '.join(person[1:]))
        return room_list