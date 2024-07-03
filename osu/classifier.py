from string_constants import JUMP_DIFF, STREAM_DIFF, TECH_DIFF, SPEED, ALT, GIMMICKS, AR, CS
def classify_nm(map_stats):
    categories = []
    if map_stats[JUMP_DIFF] > 7:
        categories.append('NM1')
    if map_stats[STREAM_DIFF] > 7:
        categories.append('NM2')
    if map_stats[TECH_DIFF] > 7:
        categories.append('NM3')
    if map_stats[ALT] > 7:
        categories.append('NM4')
    if map_stats[SPEED] > 7:
        categories.append('NM5')
    if map_stats[GIMMICKS] > 7:
        categories.append('NM6')
    if map_stats[AR] < 8.1:
        categories.append('HD1')
    if map_stats[STREAM_DIFF] > 7 or map_stats[JUMP_DIFF] > 7:
        categories.append('HD2')
    if map_stats[TECH_DIFF] > 7:
        categories.append('HD3')
    if map_stats[JUMP_DIFF] <= 7 and 7 < map_stats["AR"] <= 8.1:
        categories.append('FM1')
    if map_stats[CS] > 4.6 and map_stats[AR] < 8.1:
        categories.append('FM3')
    return categories

def classify_hr(map_stats):
    categories = []
    if map_stats[CS] > 6:
        categories.append('HR1')
    if map_stats[TECH_DIFF] > 7 or map_stats[JUMP_DIFF] > 7:
        categories.append('HR2')
    if map_stats[STREAM_DIFF] > 7 or map_stats[SPEED] > 7:
        categories.append('HR3')
    if map_stats[JUMP_DIFF] > 7:
        categories.append('FM1')
    if map_stats[STREAM_DIFF] > 7:
        categories.append('FM2')
    if map_stats[TECH_DIFF] > 7:
        categories.append('FM4')
    return categories

def classify_dt(map_stats):
    categories = []
    if map_stats[JUMP_DIFF] > 7:
        categories.append('DT1')
    if map_stats[STREAM_DIFF] > 7:
        categories.append('DT2')
    if map_stats[TECH_DIFF] > 7:
        categories.append('DT3')
    if map_stats[SPEED] > 7:
        categories.append('DT4')
    return categories

def classify_map(map_stats, mod):
    categories = []
    if mod == 'NM':
        categories = classify_nm(map_stats)
    elif mod == 'HR':
        categories = classify_hr(map_stats)
    elif mod == 'DT':
        categories = classify_dt(map_stats)

    if not categories:
        categories.append('TB')
        
    return categories