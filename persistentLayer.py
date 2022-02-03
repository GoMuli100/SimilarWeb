import os
import json

class persistentLayer:
    site_data = {}
    user_data = {}
    repeatedLengths = {}

    def __init___(self):
        return

    def add_to_session_durations(self,site,key):
        if site not in self.site_data:
            self.site_data.update({site:{"sessions":0, "sessions_lengths":[]}})
        combine_key = site+"_"+str(key)
        if combine_key in self.repeatedLengths:
            self.repeatedLengths[combine_key]+=1
            self.site_data[site]["sessions"]+=1
        else:
            self.repeatedLengths[combine_key]=1
            self.site_data[site]["sessions"]+=1
            self.site_data[site]["sessions_lengths"].append(key)

    def sort_session_lengths(self):
        for site in self.site_data.values():
            site["sessions_lengths"].sort()

    def get_number_of_sessions(self,site):
        if site in self.site_data:
            return self.site_data[site]["sessions"]
        else:
            return 0

    def get_number_of_sites(self,user):
        if user in self.user_data:
            return self.user_data[user]
        else:
            return 0

    def get_median_session_length(self,site):
        if site in self.site_data:
            num_of_sessions = self.get_number_of_sessions(site)
            middleIdx = num_of_sessions/2
            idxCounter = 0
            if num_of_sessions % 2 == 1:
                for item in self.site_data[site]["sessions_lengths"]:
                    idxCounter += self.repeatedLengths[site+"_"+str(item)]
                    if idxCounter>=middleIdx:
                        return item
            else:
                sumOfMiddle = 0
                for item in self.site_data[site]["sessions_lengths"]:
                    if sumOfMiddle==0:
                        idxCounter += self.repeatedLengths[site+"_"+str(item)]
                        if idxCounter == middleIdx:
                            sumOfMiddle+=item
                        elif idxCounter > middleIdx:
                            return item
                    else:
                        return (sumOfMiddle+item)/2
        else:
            return 0

    def save_to_disk(self,directory):
        json.dump(self.site_data,open(os.path.join(directory,"site_data.json"),"w"))
        json.dump(self.user_data,open(os.path.join(directory,"user_data.json"),"w"))
        json.dump(self.repeatedLengths,open(os.path.join(directory,"repeatedLengths.json"),"w"))

    def load_from_disk(self,directory):
        self.site_data = json.load(open(os.path.join(directory,"site_data.json"),"r"))
        self.user_data = json.load(open(os.path.join(directory,"user_data.json"),"r"))
        self.repeatedLengths = json.load(open(os.path.join(directory,"repeatedLengths.json"),"r"))