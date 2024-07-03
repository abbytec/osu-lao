import math

def calculate_jumps(hit_objects):
    jumps = 0
    for i in range(1, len(hit_objects)):
        distance = ((hit_objects[i]['x'] - hit_objects[i-1]['x']) ** 2 + 
                    (hit_objects[i]['y'] - hit_objects[i-1]['y']) ** 2) ** 0.5
        if distance > 100:
            jumps += 1
    return jumps / len(hit_objects) * 10

def calculate_streams(hit_objects, mod=None):
    streams = 0
    stream_threshold = 200
    if mod == 'DT':
        stream_threshold /= 1.5
    for i in range(1, len(hit_objects)):
        time_diff = hit_objects[i]['time'] - hit_objects[i-1]['time']
        if time_diff < stream_threshold:
            streams += 1
    return streams / len(hit_objects) * 10

def calculate_techniques(hit_objects):
    sliders = sum(1 for obj in hit_objects if obj['object_type'] == 'slider')
    rhythm_variations = 0
    consecutive_hits = 0
    for i in range(1, len(hit_objects) - 1):
        time_diff1 = hit_objects[i]['time'] - hit_objects[i-1]['time']
        time_diff2 = hit_objects[i+1]['time'] - hit_objects[i]['time']
        if (hit_objects[i-1]['object_type'] == 'circle' and hit_objects[i]['object_type'] == 'circle'):
            consecutive_hits += 1
            if abs(time_diff1 - time_diff2) > 20:
                rhythm_variations += 1
    return ((sliders/len(hit_objects)) + (rhythm_variations / consecutive_hits)) * 7.5

def calculate_alt(hit_objects):
    alt_patterns = 0
    for i in range(1, len(hit_objects) - 1):
        angle = calculate_angle(hit_objects[i-1], hit_objects[i], hit_objects[i+1])
        if angle is not None and angle < 90:
            alt_patterns += 1
    return alt_patterns / len(hit_objects) * 10

def calculate_speed(hit_objects, mod=None):
    speed = 0
    threshold = 100
    if mod == 'DT':
        threshold /= 1.5
    for i in range(1, len(hit_objects)):
        time_diff = hit_objects[i]['time'] - hit_objects[i-1]['time']
        if time_diff < threshold:
            speed += 1
    return speed / len(hit_objects) * 10

def calculate_gimmicks(hit_objects, ar, cs):
    gimmicks = 0
    for i in range(1, len(hit_objects) - 1):
        angle = calculate_angle(hit_objects[i-1], hit_objects[i], hit_objects[i+1])
        if (angle is not None and (60 <= angle <= 120 or 240 <= angle <= 300 or 5 <= angle <= 0 or 175 <= angle <= 185)) or angle is None:
            gimmicks += 1
    
    gimmick_score = gimmicks / len(hit_objects) * 10

    # AR and CS bonus multiplier
    ar_multiplier = 1.5 if ar == 1 else (1 if ar >= 9 else (1.5 - 0.0625 * (ar - 1)))
    cs_multiplier = 1.5 if cs == 1 else (1 if cs >= 4 else (1.5 - 0.125 * (cs - 1)))
    
    return gimmick_score * ar_multiplier * cs_multiplier

def calculate_angle(p1, p2, p3):
    a = ((p2['x'] - p1['x']) ** 2 + (p2['y'] - p1['y']) ** 2) ** 0.5
    b = ((p3['x'] - p2['x']) ** 2 + (p3['y'] - p2['y']) ** 2) ** 0.5
    c = ((p3['x'] - p1['x']) ** 2 + (p3['y'] - p1['y']) ** 2) ** 0.5
    if a == 0 or b == 0:
        return None
    try:
        value = (a**2 + b**2 - c**2) / (2 * a * b)
        value = max(-1, min(1, value))  # Ensure value is within [-1, 1]
        angle = math.acos(value)
        return math.degrees(angle)
    except ValueError:
        return None
