import pickle

#basic data in session
data = {
    'time': '2016-Aug-04 08:24:38',
    "siren": False
}

#new SessionHelper
class SessionHelper:            
    def __init__(self):
        #Try to download session or start new seesion
        try: 
            with open('data.pickle', 'rb') as f:
                pickle.load(f)
        except:
            with open('data.pickle', 'wb') as f:
                pickle.dump(data, f)
        self.reset_data()

    def load_data(self, data_new):
        #Upload new data to session
        with open('data.pickle', 'wb') as f:
            pickle.dump(data_new, f)

    def read_data(self):
        #Download data from session
        with open('data.pickle', 'rb') as f:
            data_new = pickle.load(f)
        return data_new

    def reset_data(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(data, f)