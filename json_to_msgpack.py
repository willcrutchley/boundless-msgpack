import msgpack, json, os

keys = []
def get_keys(obj):
    
    if isinstance(obj, list):
        for element in obj:
            get_keys(element)
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key not in keys:
                keys.append(key)
            get_keys(value)
    else:
        pass

    return keys

def transform(obj):
    
    if isinstance(obj, list):
        return [transform(element) for element in obj]
    elif isinstance(obj, dict):
        return {int(keys.index(key)): transform(value) for key, value in obj.items()}
    else:
        return obj

def convert(file):
    with open('converted/%s' % file, 'rb') as in_file:
        data = json.load(in_file)

    keys = get_keys(data)
    json_obj = transform(data)

    final = [json_obj, keys]

    with open('msgpack_reconverted/%s.msgpack' % file[:-5], 'wb+') as out_file:
        out_file.write(msgpack.dumps(final))
    

for file in sorted(os.listdir('converted')):
    if file.endswith('.json'):
        print('%s ...' % file, end='\r')
        convert(file)
        keys = []
        print('Done!')
