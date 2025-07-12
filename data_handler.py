import json
import os
import re
from utils import map_to_score

def load_ban_list(file_path="databan.json"):
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as f:
        raw_data = json.load(f)

    # Tambahkan skor (untuk keperluan ELECTRE)
    for b in raw_data:
        b["skor_kriteria"] = {
            k: map_to_score(k, v)
            for k, v in b["kriteria"].items()
        }

    return raw_data

def save_ban(nama_ban, gambar_ban, kriteria_ban, file_path="databan.json"):
    data = load_ban_list(file_path)
    last_id = max([int(re.sub(r"\D", "", b["id"])) for b in data], default=0)

    new_ban = {
        "id": f"ban{last_id + 1}",
        "nama": nama_ban,
        "gambar": gambar_ban,
        "kriteria": kriteria_ban,
        "skor_kriteria": {
            k: map_to_score(k, v) for k, v in kriteria_ban.items()
        }
    }

    data.append(new_ban)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return new_ban
