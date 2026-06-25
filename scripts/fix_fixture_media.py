import json
import os
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from juego.models import Famoso


root = ROOT
fixture_path = root / 'juego' / 'fixtures' / 'famosos.json'
media_dir = root / 'media'

with fixture_path.open('r', encoding='utf-8') as f:
    data = json.load(f)

files = [p.name for p in media_dir.iterdir() if p.is_file()]


def normalize(text: str) -> str:
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    return re.sub(r'[^a-z0-9]+', '', text)

file_map = {normalize(Path(f).stem): f for f in files}

for item in data:
    fields = item['fields']
    nombre = fields.get('nombre', '')
    nombre_norm = normalize(nombre)
    target = ''

    if nombre_norm in file_map:
        target = file_map[nombre_norm]
    else:
        matches = [value for key, value in file_map.items() if key in nombre_norm or nombre_norm in key]
        if matches:
            target = matches[0]

    fields['imagen'] = target

fixture_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

updated = 0
for item in data:
    nombre = item['fields'].get('nombre', '')
    image_name = item['fields'].get('imagen', '')
    if not image_name:
        continue

    try:
        famoso = Famoso.objects.get(pk=item['pk'])
    except Famoso.DoesNotExist:
        continue

    famoso.imagen = image_name
    famoso.save(update_fields=['imagen'])
    updated += 1

print(f'Fixture actualizado: {fixture_path}')
print(f'Imágenes asignadas a {updated} registros')
print('Ejemplo:', Famoso.objects.exclude(imagen='').first().imagen.name)
