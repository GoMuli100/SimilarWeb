import os
import sys
from loader import loader
from persistentLayer import persistentLayer

input_folder = "input/"
data_folder = "data/"

def init_loading(directory,pl):
    print("Loading begins")
    l = loader(pl)
    for file_name in os.listdir(directory):
        if file_name.endswith(".csv"):
            l.loadFile(os.path.join(directory,file_name))
            #break
    #print(l.counter)
    l.build_sessions()
    l.process_sessions()
    l.organize_data_for_quering()
    print("Loading end")

#def begin_interaction():
    

if __name__=="__main__":
    pl = persistentLayer()
    if sys.argv[1]=="load":
        init_loading(input_folder,pl)
        pl.save_to_disk(data_folder)

    if sys.argv[1]=="num_sessions":
        pl.load_from_disk(data_folder)
        print(pl.get_number_of_sessions(sys.argv[2]))
    
    if sys.argv[1]=="median_session_length":
        pl.load_from_disk(data_folder)
        print(pl.get_median_session_length(sys.argv[2]))
    
    if sys.argv[1]=="num_unique_visited_sites":
        pl.load_from_disk(data_folder)
        print(pl.get_number_of_sites(sys.argv[2]))
    