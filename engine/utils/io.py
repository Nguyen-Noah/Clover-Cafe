import json, os
from engine.utils.assets import load_img

def recursive_file_op(path, func, filetype=None):
    data = {}
    base_path = path.split('/')
    for f in os.walk(path):
        wpath = f[0].replace('\\', '/').split('/')
        path_ref = wpath.copy()
        data_ref = data

        while len(path_ref) > len(base_path):
            current_dir = path_ref[len(base_path)]
            if current_dir not in data_ref:
                data_ref[current_dir] = {}
            data_ref = data_ref[current_dir]
            path_ref.pop(len(base_path))

        for asset in f[2]:
            asset_type = asset.split('.')[-1]
            if (asset_type == filetype) or (filetype == None):
                data_ref[asset.split('.')[0]] = func(f[0] + '/' + asset)

    return data

def load_dirs(path):
    dirs = {}
    for folder in os.listdir(path):
        dirs[folder] = load_dir(f'{path}/{folder}')
    return dirs

def load_dir(path):
    image_dir = {}
    for f in os.listdir(path):
        image_dir[f.split('.')[0]] = f'{path}/{f}'
    return image_dir

def write_f(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

def read_f(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data

def read_json(path):
    f = open(path, 'r')
    data = json.load(f)
    f.close()
    return data

def write_json(path, data):
    f = open(path, 'w')
    print(data)
    json.dump(data, f)
    f.close()

def tuplestrkey(obj):
    if type(obj) == tuple:
        obj = 't\0' + str(obj).replace(' ', '')
    return obj

def tuple_change_keys(obj, convert):
    if isinstance(obj, (str, int, float)):
        return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in obj.items():
            new[convert(k)] = tuple_change_keys(v, convert)
    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__(tuple_change_keys(v, convert) for v in obj)
    else:
        return obj
    return new

def tjson_hook(obj):
    if type(obj) == dict:
        for key in list(obj):
            if (type(key) == str) and (key.translate({ord(k): None for k in ' (),t\0'}).isalnum()) and (key.find(',') != -1) and (key[:2] == 't\0'):
                new_key = tuple(int(v) for v in key.translate({ord(k): None for k in ' ()t\0'}).split(','))
                obj[new_key] = obj[key]
                del obj[key]
    return obj

def tjson_hook_loose(obj):
    if type(obj) == dict:
        for key in list(obj):
            if (type(key) == str) and (key.translate({ord(k): None for k in ' (),t\0'}).isalnum()) and (key.find(',') != -1):
                new_key = tuple(int(v) for v in key.translate({ord(k): None for k in ' ()t\0'}).split(','))
                obj[new_key] = obj[key]
                del obj[key]
    return obj

def tjson_encode(data):
    return json.dumps(tuple_change_keys(data, tuplestrkey))

def tjson_decode(data, loose=False):
    if loose:
        return json.loads(data, object_hook=tjson_hook_loose)
    else:
        return json.loads(data, object_hook=tjson_hook)

def read_tjson(path, loose=False):
    return tjson_decode(read_f(path), loose=loose)

def write_tjson(path, data):
    write_f(path, tjson_encode(data))