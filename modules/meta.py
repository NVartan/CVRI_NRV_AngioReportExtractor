from os import listdir, getenv
from os.path import join
from dotenv import load_dotenv

load_dotenv()

class Patient():    
    def __init__(self,pt_id):
        self.pt_id = pt_id    
        self.files = [join(getenv('DATADIR'), i) for i in listdir(getenv('DATADIR')) if self.pt_id in i]
        
        self.data = []
        
    def validate_data(self):
        with open('assets/fields.txt', 'r') as reference:
            ref = [line.strip('\n') for line in reference.readlines()]
            
            for item in ref:
                if item not in [point[1] for point in self.data]:
                    # print(f'{item} does not exist in data. Now adding.')
                    self.data.append((item.split('_')[-1], item, 'N/A'))
                # else: print(f'{item} already found in data.')
        return self
    
    def get_data(self, field):
        for item in self.data:
            # print(item)
            if item[1] == field:
                return item[2]
    
    #NOTE add set_data function if planning to expand for in-silico
            
    def __repr__(self):
        return self.pt_id