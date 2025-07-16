sub_kriteria = {
    "harga": {"300.000 - 800.000": 3, "800.000 - 1.300.000": 2, "diatas 1.300.000": 1},
    "merk": {"Kurang Terkenal": 1, "Cukup Terkenal": 2, "Sangat Terkenal": 3},
    "diameter ban": {"Kecil (14 - 16)": 1, "Sedang (17 - 19)": 2, "Besar (diatas 20)": 3},
    "kecepatan maksimum": {"70 km/jam - 120 km/jam": 1, "120 km/jam - 170 km/jam": 2, "diatas 170 km/jam": 3},
    "beban maksimum": {"< 600kg": 1, "600kg - 900kg": 2, "diatas 900kg": 3},
    "kondisi medan": {"Highway Terrain (H/T)": 1, "Mud Terrain (M/T)": 2, "All Terrain (A/T)": 3},
    "pola tapak": {"Simetris": 1, "Asimetris": 2, "Directional / Searah": 3}
}

bobot_opsi_per_kriteria = {
    "harga": {"300.000 - 800.000": 3, "800.000 - 1.300.000": 2, "diatas 1.300.000": 1},
    "merk": {"Kurang Terkenal": 1, "Cukup Terkenal": 2, "Sangat Terkenal": 3},
    "diameter ban": {"Kecil (14 - 16)": 1, "Sedang (17 - 19)": 2, "Besar (diatas 20)": 3},
    "kecepatan maksimum": {"70 km/jam - 120 km/jam": 1, "120 km/jam - 170 km/jam": 2, "diatas 170 km/jam": 3},
    "beban maksimum": {"< 600kg": 1, "600kg - 900kg": 2, "diatas 900kg": 3},
    "kondisi medan": {"Highway Terrain (H/T)": 1, "Mud Terrain (M/T)": 2, "All Terrain (A/T)": 3},
    "pola tapak": {"Simetris": 1, "Asimetris": 2, "Directional / Searah": 3}
}

def reverse_map(kriteria_dict, nilai):
    for label, val in kriteria_dict.items():
        if val == nilai:
            return label
    return str(nilai)

def get_all_reverse_maps():
    return {k: {v: label for label, v in sub_kriteria[k].items()} for k in sub_kriteria}

def map_to_score(kriteria, nilai):
    kategori = sub_kriteria[kriteria]

    if kriteria == "harga":
        if nilai <= 800000:
            return kategori["300.000 - 800.000"]
        elif nilai <= 1300000:
            return kategori["800.000 - 1.300.000"]
        else:
            return kategori["diatas 1.300.000"]

    elif kriteria == "diameter ban":
        if nilai <= 16:
            return kategori["Kecil (14 - 16)"]
        elif nilai <= 19:
            return kategori["Sedang (17 - 19)"]
        else:
            return kategori["Besar (diatas 20)"]

    elif kriteria == "kecepatan maksimum":
        if nilai <= 120:
            return kategori["70 km/jam - 120 km/jam"]
        elif nilai <= 170:
            return kategori["120 km/jam - 170 km/jam"]
        else:
            return kategori["diatas 170 km/jam"]

    elif kriteria == "beban maksimum":
        if nilai < 600:
            return kategori["< 600kg"]
        elif nilai <= 900:
            return kategori["600kg - 900kg"]
        else:
            return kategori["diatas 900kg"]

    elif kriteria == "merk":
        val = str(nilai).lower()
        if "bridgestone" in val or "michelin" in val or "dunlop" in val:
            return kategori["Sangat Terkenal"]
        elif "gt radial" in val or "achilles" in val or "toyo" in val:
            return kategori["Cukup Terkenal"]
        else:
            return kategori["Kurang Terkenal"]

    elif kriteria == "kondisi medan":
        return kategori.get(nilai, 1)

    elif kriteria == "pola tapak":
        return kategori.get(nilai, 1)

    return 1  # fallback jika nilai tidak cocok
