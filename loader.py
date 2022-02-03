import csv
import sys
import persistentLayer

input_folder = "input/"
input_file1 = input_folder+"input_1.csv"
input_file2 = input_folder+"input_2.csv"
input_file3 = input_folder+"input_3.csv"

class loader:
    loading_results = {}
    sessions = {}
    persistency = None
    counter = 0

    def __init__(self,pl):
        self.persistency = pl
        return

    def loadFile(self,file_name):
        for row in self.readFile(file_name):
            self.process_row(row)

    def readFile(self,file_name):
        with open(file_name,"rt") as csv_file:
            csv_reader = csv.reader(csv_file)
            yield next(csv_reader)
            for row in csv_reader:
                yield row

    def process_row(self,row):
        user = row[0]
        site = row[1]
        ts = int(row[3])
        if user not in self.loading_results.keys():
            self.loading_results[user] = {}
        if site in self.loading_results[user].keys():
            self.loading_results[user][site].append(ts)
        else:
            self.loading_results[user][site] = [ts]
            

    def findMaxVisitIdx_old(self,visits, to_value, from_idx):
        last_idx = len(visits)-1
        from_idx = from_idx
        to_idx = last_idx
        idx_to_check = 0
        idx_to_check = int((from_idx+to_idx)//2)
        while from_idx<to_idx:
            if visits[idx_to_check]==to_value:
                return idx_to_check
            elif visits[idx_to_check]>to_value:
                to_idx = idx_to_check-1
            else:
                from_idx = idx_to_check+1
            idx_to_check = int((from_idx+to_idx)//2)
        if visits[idx_to_check]>to_value:
            return idx_to_check-1
        else:
            return idx_to_check

    def findMaxVisitIdx(self,visits, from_idx):
        allowed_gap = 1800
        to_idx = from_idx
        for item in range(from_idx+1, len(visits)):
            if visits[item]>visits[to_idx]+allowed_gap:
                break
            else:
                to_idx+=1
        return to_idx

    def process_visits(self,visits):
        session_lengths = []
        visits.sort()
        from_idx = 0
        firstVisit = visits[0]
        while firstVisit != None:
            lastVisitIdx = self.findMaxVisitIdx(visits,from_idx)
            lastVisit = visits[lastVisitIdx]
            session_lengths.append(lastVisit-firstVisit)
            if lastVisitIdx==len(visits)-1:
                firstVisit = None
            else:
                from_idx = lastVisitIdx+1
                firstVisit = visits[from_idx]
        session_lengths.sort()
        return session_lengths 

    def build_sessions(self):
        sessions_data = {}
        for user in self.loading_results:
            for site in self.loading_results[user]:
                sessions = self.process_visits(self.loading_results[user][site])
                if user in sessions_data:
                    sessions_data[user].update({site:sessions})
                else:
                    sessions_data[user] = {site:sessions}
        self.sessions.update(sessions_data)

    def process_sessions(self):
        sessions = self.sessions
        for user in sessions:
            new_user_data = {user:len(sessions[user].keys())}
            self.persistency.user_data.update(new_user_data)
            for site in sessions[user]:
                for session_length in sessions[user][site]:
                    self.persistency.add_to_session_durations(site,session_length)

    def organize_data_for_quering(self):
        self.persistency.sort_session_lengths()

if __name__=="__main__":
    pl = persistentLayer.persistentLayer()
    l = loader(pl)
    l.loadFile(input_file1)
    l.loadFile(input_file2)
    l.loadFile(input_file3)
    l.build_sessions()
    l.process_sessions()
    l.organize_data_for_quering()
    print(pl.site_data)