import numpy as np

def electre_with_steps(alternatif, preferensi):
    k = list(preferensi.keys())
    w = np.array([v / sum(preferensi.values()) for v in preferensi.values()])
    n = len(alternatif)

    matriks = np.array([[alt['kriteria'][c] for c in k] for alt in alternatif])
    norm = matriks / np.sqrt((matriks ** 2).sum(axis=0))
    terbobot = norm * w

    C = np.zeros((n, n))
    D = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            cidx = terbobot[i] >= terbobot[j]
            didx = terbobot[i] < terbobot[j]
            C[i][j] = sum(w[cidx])
            D[i][j] = max(abs(terbobot[i][didx] - terbobot[j][didx])) if any(didx) else 0

    cbar = C.sum() / (n * (n - 1))
    dbar = D.sum() / (n * (n - 1))

    F = np.array([
        sum([(C[i][j] >= cbar) and (D[i][j] <= dbar) for j in range(n) if i != j])
        for i in range(n)
    ])

    ranking = np.argsort(-F)

    # ===============================
    # 🔍 Dominasi Detail (tambahan)
    # ===============================
    dominasi_detail = []
    for i in range(n):
        dominasi_info = []
        for j in range(n):
            if i == j:
                continue
            if (C[i][j] >= cbar) and (D[i][j] <= dbar):
                # cek dominasi kriteria mana saja
                kriteria_didominasi = [k[idx] for idx in range(len(k)) if terbobot[i][idx] >= terbobot[j][idx]]
                dominasi_info.append({
                    "target": j,
                    "jumlah_kriteria": len(kriteria_didominasi),
                    "kriteria": kriteria_didominasi
                })
        dominasi_detail.append(dominasi_info)

    return {
        "matriks": matriks,
        "norm": norm,
        "terbobot": terbobot,
        "C": C,
        "D": D,
        "cbar": cbar,
        "dbar": dbar,
        "F": F,
        "ranking": ranking,
        "dominasi_detail": dominasi_detail  # 🔍 hasil tambahan
    }
