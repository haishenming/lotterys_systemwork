import os
import json

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
lottery_dict_path = os.path.join(BASE_DIR, 'lottery_dict')
LOTTERY_DICR = json.loads(open(lottery_dict_path).read())