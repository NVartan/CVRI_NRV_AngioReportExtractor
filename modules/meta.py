import os
from os import listdir, getenv
from os.path import join
from dotenv import load_dotenv

from modules._paths import PROJECT_ROOT, ENV_FILE, FIELDS

load_dotenv(str(ENV_FILE))


class Patient:
    def __init__(self, pt_id):
        self.pt_id = pt_id
        data_dir = getenv('DATADIR') or ''
        if data_dir and not os.path.isabs(data_dir):
            data_dir = join(PROJECT_ROOT, data_dir)
        self.files = [join(data_dir, i) for i in listdir(data_dir) if self.pt_id in i]

        self.data = []

    def validate_data(self):
        with open(str(FIELDS), 'r') as reference:
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

    # NOTE add set_data function if planning to expand for in-silico

    def __repr__(self):
        return self.pt_id
