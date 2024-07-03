def parse_osu_file(file_path):
    hit_objects = []
    ar = 0
    cs = 0
    in_hit_objects_section = False

    object_type_map = {
        1: 'circle',
        2: 'slider',
        8: 'spinner'
    }

    def get_object_type(type_code):
        for key, value in object_type_map.items():
            if type_code & key:
                return value
        return 'unknown'

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('ApproachRate:'):
                ar = float(line.split(':')[1].strip())
            elif line.startswith('CircleSize:'):
                cs = float(line.split(':')[1].strip())
            elif line == '[HitObjects]':
                in_hit_objects_section = True
            elif in_hit_objects_section and line:
                parts = line.split(',')
                hit_objects.append({
                    'x': int(parts[0]),
                    'y': int(parts[1]),
                    'time': int(parts[2]),
                    'type': int(parts[3]),
                    'object_type': get_object_type(int(parts[3]))
                })
    return hit_objects, ar, cs
