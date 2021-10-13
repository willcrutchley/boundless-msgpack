import msgpack, json, os

def transform(obj):
    
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    
    if isinstance(obj, list):
        return [transform(element) for element in obj]
    elif isinstance(obj, dict):
        return {keys[int(key)]: transform(value) for key, value in obj.items()}
    else:
        return obj

def convert(file):
    with open('msgpack/%s' % file, 'rb') as in_file:
            data = msgpack.unpack(in_file, strict_map_key=False)
            
    json_obj = data[0]
    global keys
    keys = data[1]

    out = transform(json_obj)
    
    with open('converted/%s.json' % file[:-8], 'w+') as out_file:
        json.dump(out, out_file, indent=4, separators=(',', ': '))

for file in sorted(os.listdir('msgpack')):
    if file.endswith('.msgpack'):
        print('%s ...' % file, end='\r')

        convert(file)

        print(" Done!")
