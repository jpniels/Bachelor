import pandas



def read_file_path(path):

    with open(path, 'r') as f:
            objects  = pandas.read_json(path)
            return objects




data = read_file_path('e22-601b-0.json')

print(data.columns[2])