import os
import pandas as pd
from filesystem.extractor import extract_osz_files
from filesystem.parser import parse_osu_file
from osu.modifiers import apply_modifiers
from osu.calculators import calculate_jumps, calculate_streams, calculate_techniques, calculate_alt, calculate_speed, calculate_gimmicks
from osu.classifier import classify_map
from osu.string_constants import JUMP_DIFF, STREAM_DIFF, TECH_DIFF, SPEED, ALT, GIMMICKS, AR, CS

def read_map_data(file_path):
    hit_objects, ar, cs = parse_osu_file(file_path)

    map_stats = {
        'map_id': os.path.basename(file_path),
        JUMP_DIFF: calculate_jumps(hit_objects),
        STREAM_DIFF: calculate_streams(hit_objects),
        TECH_DIFF: calculate_techniques(hit_objects),
        ALT: calculate_alt(hit_objects),
        SPEED: calculate_speed(hit_objects),
        GIMMICKS: calculate_gimmicks(hit_objects, ar, cs),
        AR: ar,
        CS: cs,
    }

    # Aplicar modificadores de mods
    ar_hr, cs_hr = apply_modifiers(ar, cs, 'HR')
    ar_dt, _ = apply_modifiers(ar, cs, 'DT')

    map_stats_hr = map_stats.copy()
    map_stats_hr[AR] = ar_hr
    map_stats_hr[CS] = cs_hr
    map_stats_hr[STREAM_DIFF] = calculate_streams(hit_objects, 'HR')
    map_stats_hr[SPEED] = calculate_speed(hit_objects, 'HR')

    map_stats_dt = map_stats.copy()
    map_stats_dt[AR] = ar_dt
    map_stats_dt[STREAM_DIFF] = calculate_streams(hit_objects, 'DT')
    map_stats_dt[SPEED] = calculate_speed(hit_objects, 'DT')

    # Clasificar mapas para mods
    map_stats['Categories'] = classify_map(map_stats, None)
    map_stats['Mod'] = 'NM'
    map_stats_hr['Categories'] = classify_map(map_stats_hr, 'HR')
    map_stats_hr['Mod'] = 'HR'
    map_stats_dt['Categories'] = classify_map(map_stats_dt, 'DT')
    map_stats_dt['Mod'] = 'DT'

    return map_stats, map_stats_hr, map_stats_dt

# Directorios
osz_directory = '/home/abby/Descargas/drive-download-20240703T010213Z-001'
extract_to = '/home/abby/Descargas/drive-download-20240703T010213Z-001/extracted'
maps_directory = extract_to

# Extraer archivos .osz
extract_osz_files(osz_directory, extract_to)

# Lista para almacenar los resultados
results = []

# Leer todos los archivos .osu en el directorio extraído
for root, _, files in os.walk(maps_directory):
    for file_name in files:
        if file_name.endswith('.osu'):
            file_path = os.path.join(root, file_name)
            map_stats, map_stats_hr, map_stats_dt = read_map_data(file_path)
            results.append(map_stats)
            results.append(map_stats_hr)
            results.append(map_stats_dt)

# Convertir los resultados a un DataFrame y guardarlo en un archivo CSV
df = pd.DataFrame(results)
df['Categories'] = df['Categories'].apply(lambda x: ', '.join(x))  # Convertir lista de categorías a cadena

df_grouped = df.groupby('map_id')['Categories'].apply(lambda x: ', '.join(set(', '.join(x).split(', ')))).reset_index()

df_grouped.to_csv('map_classification.csv', index=False)

print("Clasificación de mapas completada y guardada en map_classification.csv")
