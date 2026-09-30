"""
Hastes codificadas para scanbody — gerador paramétrico de STL.
Desenvolvido para o scanbody de minipilar cônico (compatível com Neodent® Grand Morse®),
adaptável a outros scanbodies alterando D_SCANBODY.

Licença: MIT (ver LICENSE). Repositório: [URL do GitHub]  DOI: [DOI do Zenodo]

Geometria: um anel (luva, com fenda vertical opcional oposta à haste) que desliza sobre o cilindro do scanbody + uma haste
retangular horizontal (com chanfro num dos lados) com marcações em relevo no topo. Cada variante tem um
tipo de marcação, comprimento e largura diferentes, para o scanner não confundir
scanbodies vizinhos.

Ajuste os parâmetros abaixo com as medidas reais do SEU scanbody (paquímetro)
antes de imprimir.

Uso:  python3 haste_scanbody.py [pasta_de_saida]
      Gera todos os STL da lista VARIANTES (padrão: pasta atual). Requer só Python 3.
"""
import math, os, struct, sys

# ---------------- PARÂMETROS GERAIS (mm) ----------------
D_SCANBODY   = 4.80   # diâmetro externo do cilindro do scanbody (MEDIR!)
FOLGA        = 0.05   # folga radial (com fenda: 0.00–0.05 dá leve pressão; sem fenda: 0.05–0.15)
FENDA        = 0.60   # largura da fenda vertical no anel, oposta à haste (0 = anel fechado)
PAREDE       = 1.20   # espessura da parede do anel
ALTURA_ANEL  = 4.00   # altura do anel
CHANFRO      = 0.50   # chanfro 45° na aresta superior de UM lado da haste (quebra a simetria)
MARC_MARGEM  = 0.02   # recuo mínimo da marcação em relação à borda da face plana (evita faces coincidentes)
ALT_HASTE    = 2.00   # altura da haste retangular (eixo Z)
Z_HASTE      = 2.00   # altura do centro da haste (a partir da base do anel)

# marcações no topo da haste
MARC_ALT     = 1.00   # altura do relevo
MARC_INICIO  = 1.00   # distância da borda da 1ª marcação à face externa do anel
MARC_FIM     = 0.30   # margem entre a última marcação e a ponta da haste
VAO_MIN      = 0.80   # vão mínimo entre bordas de marcações vizinhas
# As marcações ocupam toda a face plana do topo (largura da haste menos o chanfro):
#   quadrado = lado S, cilindro = diâmetro S, triângulo = base S e comprimento S
#   (apontando para a ponta), sendo S = largura - CHANFRO - 2*MARC_MARGEM
SEG          = 96     # resolução circular

# variantes: (arquivo, comprimento da haste a partir da face externa do anel,
#             largura da haste, padrão de marcações, vãos)
# - o padrão de marcações se repete ciclicamente ao longo da haste
# - vãos = distâncias livres entre as bordas de marcações consecutivas, em mm;
#   são propositalmente irregulares e diferentes em cada haste, para que nenhum
#   trecho se repita (o scanner não consegue "deslizar" a imagem)
# - cabem tantas marcações quanto o comprimento permitir
VARIANTES = [
    ("haste_A_triangulos_12mm_L3.0.stl", 12.0, 3.0, ["tri"],                [1.0, 1.9]),
    ("haste_B_quadrados_15mm_L3.5.stl",  15.0, 3.5, ["quad"],               [1.9, 1.0]),
    ("haste_C_cilindros_18mm_L4.0.stl",  18.0, 4.0, ["cil"],                [1.2, 2.4]),
    ("haste_D_misto_21mm_L4.5.stl",      21.0, 4.5, ["cil", "tri", "quad"], [2.2, 1.0]),
]
# ---------------------------------------------------------

def tube(tris, r_in, r_out, z0, z1, n):
    for i in range(n):
        a0, a1 = 2*math.pi*i/n, 2*math.pi*(i+1)/n
        c0, s0, c1, s1 = math.cos(a0), math.sin(a0), math.cos(a1), math.sin(a1)
        oi0, oi1 = (r_out*c0, r_out*s0), (r_out*c1, r_out*s1)
        ii0, ii1 = (r_in*c0, r_in*s0), (r_in*c1, r_in*s1)
        tris.append(((*oi0, z0), (*oi1, z0), (*oi1, z1)))   # parede externa
        tris.append(((*oi0, z0), (*oi1, z1), (*oi0, z1)))
        tris.append(((*ii0, z0), (*ii1, z1), (*ii1, z0)))   # parede interna
        tris.append(((*ii0, z0), (*ii0, z1), (*ii1, z1)))
        tris.append(((*ii0, z1), (*oi1, z1), (*ii1, z1)))   # topo
        tris.append(((*ii0, z1), (*oi0, z1), (*oi1, z1)))
        tris.append(((*ii0, z0), (*ii1, z0), (*oi1, z0)))   # base
        tris.append(((*ii0, z0), (*oi1, z0), (*oi0, z0)))

def c_ring(tris, r_in, r_out, z0, z1, n, fenda):
    """Anel com fenda vertical de faces paralelas, centrada no lado -X (oposto à haste)."""
    h = fenda/2
    d_o, d_i = math.asin(h/r_out), math.asin(h/r_in)
    lim_o, lim_i = math.pi - d_o, math.pi - d_i
    def P(r, lim, t):
        a = -lim + 2*lim*t
        return (r*math.cos(a), r*math.sin(a))
    for i in range(n):
        t0, t1 = i/n, (i+1)/n
        oi0, oi1 = P(r_out, lim_o, t0), P(r_out, lim_o, t1)
        ii0, ii1 = P(r_in, lim_i, t0), P(r_in, lim_i, t1)
        tris.append(((*oi0, z0), (*oi1, z0), (*oi1, z1)))   # parede externa
        tris.append(((*oi0, z0), (*oi1, z1), (*oi0, z1)))
        tris.append(((*ii0, z0), (*ii1, z1), (*ii1, z0)))   # parede interna
        tris.append(((*ii0, z0), (*ii0, z1), (*ii1, z1)))
        tris.append(((*ii0, z1), (*oi1, z1), (*ii1, z1)))   # topo
        tris.append(((*ii0, z1), (*oi0, z1), (*oi1, z1)))
        tris.append(((*ii0, z0), (*ii1, z0), (*oi1, z0)))   # base
        tris.append(((*ii0, z0), (*oi1, z0), (*oi0, z0)))
    # faces planas da fenda (y = -h no início, y = +h no fim)
    i0, o0 = P(r_in, lim_i, 0), P(r_out, lim_o, 0)
    i1, o1 = P(r_in, lim_i, 1), P(r_out, lim_o, 1)
    tris.append(((*i0, z0), (*o0, z0), (*o0, z1))); tris.append(((*i0, z0), (*o0, z1), (*i0, z1)))
    tris.append(((*i1, z0), (*o1, z1), (*o1, z0))); tris.append(((*i1, z0), (*i1, z1), (*o1, z1)))

def prism(tris, pts, z0, z1):
    """Extrusão vertical de um polígono convexo (pontos em sentido anti-horário)."""
    n = len(pts)
    lo = [(x, y, z0) for x, y in pts]; hi = [(x, y, z1) for x, y in pts]
    for i in range(1, n-1):
        tris.append((lo[0], lo[i+1], lo[i]))   # base
        tris.append((hi[0], hi[i], hi[i+1]))   # topo
    for i in range(n):
        j = (i+1) % n
        tris.append((lo[i], lo[j], hi[j])); tris.append((lo[i], hi[j], hi[i]))

def box(tris, x0, x1, y0, y1, z0, z1):
    prism(tris, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], z0, z1)

def prism_x(tris, sec, x0, x1):
    """Extrusão ao longo de X de uma seção convexa (lista de (y, z))."""
    area = sum(sec[i][0]*sec[(i+1)%len(sec)][1] - sec[(i+1)%len(sec)][0]*sec[i][1]
               for i in range(len(sec)))
    if area < 0:
        sec = sec[::-1]
    n = len(sec)
    a = [(x0, y, z) for y, z in sec]; b = [(x1, y, z) for y, z in sec]
    for i in range(1, n-1):
        tris.append((a[0], a[i+1], a[i]))   # tampa em x0 (normal -X)
        tris.append((b[0], b[i], b[i+1]))   # tampa em x1 (normal +X)
    for i in range(n):
        j = (i+1) % n
        tris.append((a[i], a[j], b[j])); tris.append((a[i], b[j], b[i]))

def marca(tris, tipo, xc, yc, S, z0, z1):
    h = S/2
    if tipo == "tri":      # triângulo apontando para a ponta da haste (+X)
        pts = [(xc-h, yc-h), (xc+h, yc), (xc-h, yc+h)]
    elif tipo == "quad":
        pts = [(xc-h, yc-h), (xc+h, yc-h), (xc+h, yc+h), (xc-h, yc+h)]
    elif tipo == "cil":
        pts = [(xc + h*math.cos(2*math.pi*k/64), yc + h*math.sin(2*math.pi*k/64)) for k in range(64)]
    else:
        raise ValueError(tipo)
    prism(tris, pts, z0, z1)

def normal(t):
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = t
    ux, uy, uz = bx-ax, by-ay, bz-az
    vx, vy, vz = cx-ax, cy-ay, cz-az
    nx, ny, nz = uy*vz-uz*vy, uz*vx-ux*vz, ux*vy-uy*vx
    l = math.sqrt(nx*nx+ny*ny+nz*nz) or 1
    return nx/l, ny/l, nz/l

def gerar(arquivo, comp, larg, padrao, vaos):
    tris = []
    r_in  = D_SCANBODY/2 + FOLGA
    r_out = r_in + PAREDE
    if FENDA > 0:
        c_ring(tris, r_in, r_out, 0.0, ALTURA_ANEL, SEG, FENDA)
    else:
        tube(tris, r_in, r_out, 0.0, ALTURA_ANEL, SEG)
    # a haste começa no meio da parede (sobreposição) para fundir com o anel
    x_ini, x_fim = r_in + PAREDE/2, r_out + comp
    z_bot, z_top = Z_HASTE - ALT_HASTE/2, Z_HASTE + ALT_HASTE/2
    w = larg/2
    # seção com chanfro na aresta superior do lado +Y
    sec = [(-w, z_bot), (w, z_bot), (w, z_top - CHANFRO), (w - CHANFRO, z_top), (-w, z_top)]
    prism_x(tris, sec, x_ini, x_fim)

    # marcações ocupando toda a face plana superior (entre -w e w-CHANFRO)
    plana = larg - CHANFRO
    yc = -CHANFRO/2
    S = plana - 2*MARC_MARGEM
    x_lim = x_fim - MARC_FIM
    xc = r_out + MARC_INICIO + S/2
    usadas, vaos_usados = [], []
    k = 0
    while xc + S/2 <= x_lim + 1e-9:
        tipo = padrao[k % len(padrao)]
        marca(tris, tipo, xc, yc, S, z_top - 0.05, z_top + MARC_ALT)
        usadas.append(tipo)
        vao = vaos[k % len(vaos)]
        if vao < VAO_MIN - 1e-9:
            raise ValueError(f"{arquivo}: vão de {vao:.2f} mm (< {VAO_MIN} mm).")
        if xc + S/2 + vao + S > x_lim + 1e-9:
            break
        vaos_usados.append(vao)
        xc += S + vao; k += 1
    livre = x_lim - (xc + S/2)

    with open(arquivo, "wb") as f:
        f.write(f"Haste scanbody Neodent {comp:.0f}mm".encode().ljust(80, b" "))
        f.write(struct.pack("<I", len(tris)))
        for t in tris:
            f.write(struct.pack("<3f", *normal(t)))
            for v in t:
                f.write(struct.pack("<3f", *v))
            f.write(b"\0\0")
    print(f"{arquivo}: haste {comp:.0f} x {larg:.1f} mm | marcações {S:.2f} x {S:.2f} x {MARC_ALT:.1f} mm | "
          f"{len(usadas)}: {' '.join(usadas)} | vãos {vaos_usados} mm | sobra na ponta {livre+MARC_FIM:.1f} mm")

if __name__ == "__main__":
    saida = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(saida, exist_ok=True)
    for arq, comp, larg, padrao, vaos in VARIANTES:
        arq = os.path.join(saida, arq)
        if FENDA > 0:
            arq = arq.replace(".stl", f"_fenda{FENDA:.1f}.stl")
        gerar(arq, comp, larg, padrao, vaos)
