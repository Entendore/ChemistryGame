#!/home/z/.venv/bin/python
"""
Chemistry Lab - Molecule Combiner v3
======================================
Build molecules from atoms, then combine molecules for reactions!
Multiple items can go in the reactor at once.

Controls:
  - Drag atoms/molecules from inventory to reactor slots
  - Click filled reactor slots to return items
  - Click REACT when a valid combination is loaded
  - Press H for hint, R to reset, TAB for recipe book, ESC for menu
"""

import pygame, sys, math, random
from collections import Counter

pygame.init()
W, H = 1280, 780
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Chemistry Lab - Molecule Combiner")
clock = pygame.time.Clock()
FPS = 60

def _f(sz, b=False):
    for n in ["Segoe UI","Arial","DejaVu Sans",None]:
        try: return pygame.font.SysFont(n, sz, bold=b)
        except: continue
    return pygame.font.Font(None, sz)

FT=_f(42,True); FL=_f(26,True); FM=_f(19); FMB=_f(19,True)
FS=_f(15); FSB=_f(15,True); FX=_f(12); FF=_f(20,True); FFB=_f(28,True)

BG=(12,14,26); PANEL=(20,23,40); PANEL2=(28,32,52); BORDER=(48,52,78)
TXT=(220,225,238); TXT_D=(120,125,150); ACCENT=(0,175,255)
GREEN=(0,220,130); RED=(255,75,75); YELLOW=(255,215,50)
PURPLE=(160,100,255); ORANGE=(255,155,55); CYAN=(0,220,240)
BTN=(35,52,92); BTN_H=(48,68,115); BTN_D=(28,35,55)
SLOT_E=(30,35,55); SLOT_H=(42,48,72)

# ═══════════════════════════════════════════════════════════════════════════════
#  ELEMENT COLORS & RADII  (31 elements)
# ═══════════════════════════════════════════════════════════════════════════════
EC = {
    'H':(190,200,255), 'O':(255,75,75),  'N':(75,115,255),  'C':(130,130,140),
    'Na':(170,110,255),'Cl':(75,225,75),  'S':(240,240,75),  'Ca':(80,200,120),
    'Fe':(210,140,80), 'K':(200,100,200),
    'P':(255,150,50),  'Mg':(100,210,120),'Al':(180,195,215), 'Si':(200,180,150),
    'Li':(230,90,90),  'F':(140,255,100), 'Br':(185,85,55),   'I':(120,60,190),
    'Ag':(200,205,215),'Cu':(215,135,60), 'Zn':(125,145,190),
    'He':(220,220,255),'Ne':(255,100,150),'Ar':(180,130,255),
    'Mn':(140,120,180),'Cr':(170,170,200),'Ni':(180,200,160),
    'Sn':(200,200,210),'Pb':(100,100,120),'Ba':(100,200,180),
    'Ti':(190,180,210),
}
AR = {
    'H':8,'C':10,'N':9,'O':9,'Na':11,'Cl':10,'S':10,'Ca':11,'Fe':10,'K':10,
    'P':10,'Mg':10,'Al':10,'Si':10,'Li':8,'F':8,'Br':10,'I':10,
    'Ag':10,'Cu':10,'Zn':10,
    'He':7,'Ne':7,'Ar':8,'Mn':10,'Cr':10,'Ni':10,
    'Sn':11,'Pb':11,'Ba':11,'Ti':10,
}

# ═══════════════════════════════════════════════════════════════════════════════
#  ITEM DATA  (atoms + molecules)
#  (display_name, card_color, [(dx,dy,elem),...], [(i,j),...], is_atom)
# ═══════════════════════════════════════════════════════════════════════════════
MOL = {
    # ── Atoms (31) ──
    'H':  ('Hydrogen',    EC['H'],  [(0,0,'H')],  [], True),
    'O':  ('Oxygen',      EC['O'],  [(0,0,'O')],  [], True),
    'N':  ('Nitrogen',    EC['N'],  [(0,0,'N')],  [], True),
    'C':  ('Carbon',      EC['C'],  [(0,0,'C')],  [], True),
    'Na': ('Sodium',      EC['Na'], [(0,0,'Na')], [], True),
    'Cl': ('Chlorine',    EC['Cl'], [(0,0,'Cl')], [], True),
    'S':  ('Sulfur',      EC['S'],  [(0,0,'S')],  [], True),
    'Ca': ('Calcium',     EC['Ca'], [(0,0,'Ca')], [], True),
    'Fe': ('Iron',        EC['Fe'], [(0,0,'Fe')], [], True),
    'K':  ('Potassium',   EC['K'],  [(0,0,'K')],  [], True),
    'P':  ('Phosphorus',  EC['P'],  [(0,0,'P')],  [], True),
    'Mg': ('Magnesium',   EC['Mg'], [(0,0,'Mg')], [], True),
    'Al': ('Aluminum',    EC['Al'], [(0,0,'Al')], [], True),
    'Si': ('Silicon',     EC['Si'], [(0,0,'Si')], [], True),
    'Li': ('Lithium',     EC['Li'], [(0,0,'Li')], [], True),
    'F':  ('Fluorine',    EC['F'],  [(0,0,'F')],  [], True),
    'Br': ('Bromine',     EC['Br'], [(0,0,'Br')], [], True),
    'I':  ('Iodine',      EC['I'],  [(0,0,'I')],  [], True),
    'Ag': ('Silver',      EC['Ag'], [(0,0,'Ag')], [], True),
    'Cu': ('Copper',      EC['Cu'], [(0,0,'Cu')], [], True),
    'Zn': ('Zinc',        EC['Zn'], [(0,0,'Zn')], [], True),
    'He': ('Helium',      EC['He'], [(0,0,'He')], [], True),
    'Ne': ('Neon',        EC['Ne'], [(0,0,'Ne')], [], True),
    'Ar': ('Argon',       EC['Ar'], [(0,0,'Ar')], [], True),
    'Mn': ('Manganese',   EC['Mn'], [(0,0,'Mn')], [], True),
    'Cr': ('Chromium',    EC['Cr'], [(0,0,'Cr')], [], True),
    'Ni': ('Nickel',      EC['Ni'], [(0,0,'Ni')], [], True),
    'Sn': ('Tin',         EC['Sn'], [(0,0,'Sn')], [], True),
    'Pb': ('Lead',        EC['Pb'], [(0,0,'Pb')], [], True),
    'Ba': ('Barium',      EC['Ba'], [(0,0,'Ba')], [], True),
    'Ti': ('Titanium',    EC['Ti'], [(0,0,'Ti')], [], True),

    # ── Diatomic / Simple Molecules ──
    'H\u2082':  ('Hydrogen Gas',       (110,140,210), [(-11,0,'H'),(11,0,'H')],             [(0,1)], False),
    'O\u2082':  ('Oxygen Gas',         (210,90,90),   [(-11,0,'O'),(11,0,'O')],             [(0,1)], False),
    'N\u2082':  ('Nitrogen Gas',       (90,120,220),  [(-11,0,'N'),(11,0,'N')],             [(0,1)], False),
    'Cl\u2082': ('Chlorine Gas',       (80,195,80),   [(-12,0,'Cl'),(12,0,'Cl')],           [(0,1)], False),
    'CO':     ('Carbon Monoxide',     (210,100,100), [(-11,0,'C'),(11,0,'O')],             [(0,1)], False),
    'NO':     ('Nitric Oxide',        (110,100,230), [(-11,0,'N'),(11,0,'O')],             [(0,1)], False),
    'HF':     ('Hydrofluoric Acid',   (150,245,120), [(-11,0,'H'),(11,0,'F')],             [(0,1)], False),
    'HBr':    ('Hydrobromic Acid',    (180,130,110), [(-11,0,'H'),(11,0,'Br')],            [(0,1)], False),
    'HI':     ('Hydroiodic Acid',     (150,100,210), [(-11,0,'H'),(11,0,'I')],             [(0,1)], False),
    'KCl':    ('Potassium Chloride',  (200,115,205), [(-12,0,'K'),(12,0,'Cl')],            [(0,1)], False),
    'LiH':    ('Lithium Hydride',     (230,110,110), [(-11,0,'Li'),(11,0,'H')],            [(0,1)], False),
    'NaF':    ('Sodium Fluoride',     (200,175,225), [(-12,0,'Na'),(12,0,'F')],            [(0,1)], False),
    'AgCl':   ('Silver Chloride',     (210,215,225), [(-12,0,'Ag'),(12,0,'Cl')],           [(0,1)], False),
    'CaO':    ('Calcium Oxide',       (110,200,135), [(-12,0,'Ca'),(12,0,'O')],            [(0,1)], False),
    'MgO':    ('Magnesium Oxide',     (100,210,130), [(-12,0,'Mg'),(12,0,'O')],            [(0,1)], False),
    'CuO':    ('Copper(II) Oxide',    (215,145,75),  [(-11,0,'Cu'),(11,0,'O')],            [(0,1)], False),
    'ZnO':    ('Zinc Oxide',          (130,150,195), [(-11,0,'Zn'),(11,0,'O')],            [(0,1)], False),

    # ── Triatomic / Bent / Linear ──
    'H\u2082O': ('Water',             (60,140,225),  [(0,-7,'O'),(-13,10,'H'),(13,10,'H')],  [(0,1),(0,2)], False),
    'NO\u2082':  ('Nitrogen Dioxide',  (180,80,180), [(-13,8,'O'),(0,-6,'N'),(13,8,'O')],    [(1,0),(1,2)], False),
    'SO\u2082':  ('Sulfur Dioxide',    (225,215,80), [(-13,8,'O'),(0,-6,'S'),(13,8,'O')],    [(1,0),(1,2)], False),
    'SiO\u2082': ('Silicon Dioxide',   (205,190,160),[(-13,8,'O'),(0,-6,'Si'),(13,8,'O')],   [(1,0),(1,2)], False),
    'HCl':    ('Hydrochloric Acid',   (130,205,155), [(-12,0,'H'),(12,0,'Cl')],             [(0,1)], False),
    'NaCl':   ('Table Salt',          (180,170,205), [(-12,0,'Na'),(12,0,'Cl')],            [(0,1)], False),
    'Na\u2082O': ('Sodium Oxide',     (190,140,235), [(-14,0,'Na'),(0,0,'O'),(14,0,'Na')],  [(0,1),(1,2)], False),
    'MgCl\u2082':('Magnesium Chloride',(125,215,155),[(-14,0,'Cl'),(0,0,'Mg'),(14,0,'Cl')],[(0,1),(1,2)], False),

    # ── 4-atom molecules ──
    'NH\u2083':  ('Ammonia',           (80,110,225),  [(0,-9,'N'),(-13,8,'H'),(13,8,'H'),(0,17,'H')],         [(0,1),(0,2),(0,3)], False),
    'SO\u2083':  ('Sulfur Trioxide',   (235,225,80),  [(0,-10,'S'),(-14,8,'O'),(14,8,'O'),(0,18,'O')],        [(0,1),(0,2),(0,3)], False),
    'CH\u2084':  ('Methane',           (140,140,165), [(0,0,'C'),(-14,-12,'H'),(14,-12,'H'),(-14,12,'H'),(14,12,'H')], [(0,1),(0,2),(0,3),(0,4)], False),
    'NaOH':   ('Sodium Hydroxide',    (200,160,240), [(0,0,'Na'),(16,0,'O'),(28,0,'H')],                     [(0,1),(1,2)], False),
    'CO\u2082':  ('Carbon Dioxide',     (185,130,130), [(-16,0,'O'),(0,0,'C'),(16,0,'O')],                      [(0,1),(1,2)], False),
    'PCl\u2083': ('Phosphorus Trichloride',(225,165,80),[(0,-10,'P'),(-14,8,'Cl'),(14,8,'Cl'),(0,18,'Cl')],  [(0,1),(0,2),(0,3)], False),
    'C\u2082H\u2082': ('Acetylene',     (185,165,210), [(-10,0,'C'),(10,0,'C'),(-18,0,'H'),(18,0,'H')],        [(0,1),(0,2),(1,3)], False),
    'H\u2082O\u2082':('Hydrogen Peroxide',(255,200,100),[(-10,-8,'O'),(10,8,'O'),(-10,8,'H'),(10,-8,'H')],   [(0,3),(1,2)], False),

    # ── 5-atom molecules ──
    'HNO\u2083': ('Nitric Acid',      (200,120,200), [(0,0,'N'),(-15,-8,'O'),(15,-8,'O'),(0,15,'O'),(-15,15,'H')], [(0,1),(0,2),(0,3),(3,4)], False),
    'C\u2082H\u2084': ('Ethylene',     (175,175,195), [(-10,0,'C'),(10,0,'C'),(-20,-12,'H'),(-20,12,'H'),(20,-12,'H'),(20,12,'H')], [(0,1),(0,2),(0,3),(1,4),(1,5)], False),
    'Ca(OH)\u2082':('Calcium Hydroxide',(125,215,155),[(0,0,'Ca'),(-16,-12,'O'),(-28,-12,'H'),(-16,12,'O'),(-28,12,'H')], [(0,1),(1,2),(0,3),(3,4)], False),
    'Mg(OH)\u2082':('Magnesium Hydroxide',(115,205,145),[(0,0,'Mg'),(-16,-12,'O'),(-28,-12,'H'),(-16,12,'O'),(-28,12,'H')], [(0,1),(1,2),(0,3),(3,4)], False),

    # ── 6+ atom molecules ──
    'C\u2082H\u2086': ('Ethane',       (160,160,180), [(-10,0,'C'),(10,0,'C'),(-22,-10,'H'),(-22,10,'H'),(22,-10,'H'),(22,10,'H'),(-10,-16,'H'),(10,16,'H')], [(0,1),(0,2),(0,3),(1,4),(1,5),(0,6),(1,7)], False),
    'C\u2083H\u2088': ('Propane',      (155,155,170), [(-18,0,'C'),(0,0,'C'),(18,0,'C'),(-28,-12,'H'),(-28,12,'H'),(-10,-16,'H'),(10,-16,'H'),(28,-12,'H'),(28,12,'H'),(0,16,'H'),(0,-16,'H')], [(0,1),(1,2),(0,3),(0,4),(0,5),(1,6),(1,7),(2,8),(2,9),(1,10)], False),
    'H\u2083PO\u2084':('Phosphoric Acid',(245,225,100),[(0,-5,'P'),(-16,-12,'O'),(16,-12,'O'),(-16,10,'O'),(16,10,'O'),(-28,-12,'H'),(28,-12,'H'),(-28,10,'H')], [(0,1),(0,2),(0,3),(0,4),(5,1),(6,2),(7,3)], False),
    'H\u2082SO\u2084':('Sulfuric Acid', (220,200,80), [(0,0,'S'),(-16,-12,'O'),(16,-12,'O'),(-16,12,'O'),(16,12,'O'),(0,-22,'H'),(0,22,'H')], [(0,1),(0,2),(0,3),(0,4),(5,1),(6,3)], False),

    # ── Complex molecules ──
    'CaCO\u2083': ('Calcium Carbonate',(200,220,180), [(0,0,'Ca'),(18,0,'C'),(30,-10,'O'),(30,10,'O'),(42,0,'O')], [(0,1),(1,2),(1,3),(1,4)], False),
    'Fe\u2082O\u2083':('Iron Oxide',   (200,140,90),  [(-12,0,'Fe'),(12,0,'Fe'),(0,-16,'O'),(-18,12,'O'),(18,12,'O')], [(0,2),(1,2),(0,3),(1,4)], False),
    'Al\u2082O\u2083':('Aluminum Oxide',(195,200,220), [(-12,0,'Al'),(12,0,'Al'),(0,-16,'O'),(-20,12,'O'),(20,12,'O')], [(0,2),(1,2),(0,3),(1,4)], False),
    'H\u2082CO\u2083':('Carbonic Acid',(150,190,210), [(0,-5,'C'),(-16,8,'O'),(16,8,'O'),(-22,-14,'O'),(-28,-14,'H'),(22,-14,'O'),(28,-14,'H')], [(0,1),(0,2),(0,3),(3,4),(0,5),(5,6)], False),
    'NH\u2084Cl': ('Ammonium Chloride',(170,180,200), [(0,-8,'N'),(-14,5,'H'),(14,5,'H'),(0,16,'H'),(-8,-18,'H'),(22,0,'Cl')], [(0,1),(0,2),(0,3),(0,4),(0,5)], False),
    'ZnCl\u2082': ('Zinc Chloride',    (135,155,200), [(-14,0,'Cl'),(0,0,'Zn'),(14,0,'Cl')], [(0,1),(1,2)], False),

    # ── New: Metal Oxides (extended) ──
    'MnO':     ('Manganese(II) Oxide',  (150,130,195), [(-12,0,'Mn'),(12,0,'O')],            [(0,1)], False),
    'MnO\u2082': ('Manganese(IV) Oxide',(155,135,200), [(-13,8,'O'),(0,-6,'Mn'),(13,8,'O')],   [(1,0),(1,2)], False),
    'Cr\u2082O\u2083':('Chromium(III) Oxide',(180,180,210),[(-12,0,'Cr'),(12,0,'Cr'),(0,-16,'O'),(-18,12,'O'),(18,12,'O')], [(0,2),(1,2),(0,3),(1,4)], False),
    'NiO':     ('Nickel(II) Oxide',     (190,205,170), [(-12,0,'Ni'),(12,0,'O')],            [(0,1)], False),
    'SnO\u2082': ('Tin(IV) Oxide',     (210,210,220), [(-13,8,'O'),(0,-6,'Sn'),(13,8,'O')],  [(1,0),(1,2)], False),
    'PbO':     ('Lead(II) Oxide',       (115,115,135), [(-12,0,'Pb'),(12,0,'O')],            [(0,1)], False),
    'BaO':     ('Barium Oxide',         (110,210,190), [(-12,0,'Ba'),(12,0,'O')],            [(0,1)], False),
    'TiO\u2082': ('Titanium(IV) Oxide', (200,190,220), [(-13,8,'O'),(0,-6,'Ti'),(13,8,'O')],  [(1,0),(1,2)], False),

    # ── New: Metal Sulfides ──
    'FeS':     ('Iron(II) Sulfide',     (220,160,95),  [(-12,0,'Fe'),(12,0,'S')],            [(0,1)], False),
    'CuS':     ('Copper(II) Sulfide',   (225,150,75),  [(-12,0,'Cu'),(12,0,'S')],            [(0,1)], False),
    'ZnS':     ('Zinc Sulfide',         (140,160,200), [(-12,0,'Zn'),(12,0,'S')],            [(0,1)], False),

    # ── New: Metal Chlorides (extended) ──
    'AlCl\u2083': ('Aluminum Chloride',(195,205,225), [(0,-10,'Al'),(-14,8,'Cl'),(14,8,'Cl'),(0,18,'Cl')], [(0,1),(0,2),(0,3)], False),
    'CaCl\u2082': ('Calcium Chloride', (100,210,140), [(-14,0,'Cl'),(0,0,'Ca'),(14,0,'Cl')],[(0,1),(1,2)], False),
    'CuCl\u2082': ('Copper(II) Chloride',(225,150,80),[(-14,0,'Cl'),(0,0,'Cu'),(14,0,'Cl')],[(0,1),(1,2)], False),
    'FeCl\u2082': ('Iron(II) Chloride', (220,155,90), [(-14,0,'Cl'),(0,0,'Fe'),(14,0,'Cl')],[(0,1),(1,2)], False),
    'FeCl\u2083': ('Iron(III) Chloride',(215,145,85), [(0,-10,'Fe'),(-14,8,'Cl'),(14,8,'Cl'),(0,18,'Cl')], [(0,1),(0,2),(0,3)], False),
    'BaCl\u2082': ('Barium Chloride',   (115,210,190), [(-14,0,'Cl'),(0,0,'Ba'),(14,0,'Cl')],[(0,1),(1,2)], False),

    # ── New: Alkali Compounds ──
    'KOH':     ('Potassium Hydroxide',  (210,120,210), [(0,0,'K'),(16,0,'O'),(28,0,'H')],      [(0,1),(1,2)], False),
    'K\u2082O':  ('Potassium Oxide',   (210,115,215), [(-14,0,'K'),(0,0,'O'),(14,0,'K')],    [(0,1),(1,2)], False),
    'NaBr':    ('Sodium Bromide',       (185,145,210), [(-12,0,'Na'),(12,0,'Br')],            [(0,1)], False),
    'NaI':     ('Sodium Iodide',        (165,110,210), [(-12,0,'Na'),(12,0,'I')],             [(0,1)], False),
    'KBr':     ('Potassium Bromide',    (200,120,200), [(-12,0,'K'),(12,0,'Br')],             [(0,1)], False),
    'KI':      ('Potassium Iodide',     (175,95,205),  [(-12,0,'K'),(12,0,'I')],             [(0,1)], False),

    # ── New: Sulfates ──
    'Na\u2082SO\u2084': ('Sodium Sulfate',     (195,210,220), [(0,0,'Na'),(-16,10,'S'),(-28,10,'O'),(-16,22,'O'),(-4,22,'O'),(0,0,'Na'),(16,10,'O'),(16,22,'O')], [(0,1),(1,2),(1,3),(1,4),(5,1),(6,7)], False),
    'CaSO\u2084': ('Calcium Sulfate',    (130,210,160), [(0,0,'Ca'),(18,0,'S'),(30,-10,'O'),(30,10,'O'),(42,-10,'O'),(42,10,'O')], [(0,1),(1,2),(1,3),(1,4),(1,5)], False),
    'BaSO\u2084': ('Barium Sulfate',     (120,210,195), [(0,0,'Ba'),(18,0,'S'),(30,-10,'O'),(30,10,'O'),(42,-10,'O'),(42,10,'O')], [(0,1),(1,2),(1,3),(1,4),(1,5)], False),

    # ── New: Other Compounds ──
    'PbI\u2082': ('Lead(II) Iodide',     (120,85,175), [(-14,0,'I'),(0,0,'Pb'),(14,0,'I')],    [(0,1),(1,2)], False),
    'Ba(OH)\u2082':('Barium Hydroxide',  (110,205,185),[(0,0,'Ba'),(-16,-12,'O'),(-28,-12,'H'),(-16,12,'O'),(-28,12,'H')], [(0,1),(1,2),(0,3),(3,4)], False),
    'MnCl\u2082': ('Manganese(II) Chloride',(155,140,195),[(-14,0,'Cl'),(0,0,'Mn'),(14,0,'Cl')],[(0,1),(1,2)], False),
}

# ═══════════════════════════════════════════════════════════════════════════════
#  RECIPES  -  (reactants_dict, products_dict, name, equation)
# ═══════════════════════════════════════════════════════════════════════════════
ALL_RECIPES = []
def _add(r, p, name, eq):
    ALL_RECIPES.append((dict(r), dict(p), name, eq))

# ── Atom Assembly: Diatomic Gases ──
_add({'H':2},  {'H\u2082':1},  'Hydrogen Gas',   '2H \u2192 H\u2082')
_add({'O':2},  {'O\u2082':1},  'Oxygen Gas',     '2O \u2192 O\u2082')
_add({'N':2},  {'N\u2082':1},  'Nitrogen Gas',   '2N \u2192 N\u2082')
_add({'Cl':2}, {'Cl\u2082':1}, 'Chlorine Gas',   '2Cl \u2192 Cl\u2082')

# ── Atom Assembly: Simple Compounds (2-3 atoms) ──
_add({'H':2,'O':1},        {'H\u2082O':1},       'Water',              '2H + O \u2192 H\u2082O')
_add({'C':1,'O':1},        {'CO':1},            'Carbon Monoxide',    'C + O \u2192 CO')
_add({'C':1,'O':2},        {'CO\u2082':1},       'Carbon Dioxide',     'C + 2O \u2192 CO\u2082')
_add({'N':1,'O':1},        {'NO':1},            'Nitric Oxide',       'N + O \u2192 NO')
_add({'N':1,'O':2},        {'NO\u2082':1},       'Nitrogen Dioxide',   'N + 2O \u2192 NO\u2082')
_add({'S':1,'O':2},        {'SO\u2082':1},       'Sulfur Dioxide',     'S + 2O \u2192 SO\u2082')
_add({'Si':1,'O':2},       {'SiO\u2082':1},      'Silicon Dioxide',    'Si + 2O \u2192 SiO\u2082')
_add({'Na':1,'Cl':1},      {'NaCl':1},          'Table Salt',         'Na + Cl \u2192 NaCl')
_add({'Na':1,'F':1},       {'NaF':1},           'Sodium Fluoride',    'Na + F \u2192 NaF')
_add({'K':1,'Cl':1},       {'KCl':1},           'Potassium Chloride', 'K + Cl \u2192 KCl')
_add({'Li':1,'H':1},       {'LiH':1},           'Lithium Hydride',    'Li + H \u2192 LiH')
_add({'H':1,'F':1},        {'HF':1},            'Hydrofluoric Acid',  'H + F \u2192 HF')
_add({'H':1,'Cl':1},       {'HCl':1},           'Hydrochloric Acid',  'H + Cl \u2192 HCl')
_add({'H':1,'Br':1},       {'HBr':1},           'Hydrobromic Acid',   'H + Br \u2192 HBr')
_add({'H':1,'I':1},        {'HI':1},            'Hydroiodic Acid',    'H + I \u2192 HI')
_add({'Ag':1,'Cl':1},      {'AgCl':1},          'Silver Chloride',    'Ag + Cl \u2192 AgCl')
_add({'Ca':1,'O':1},       {'CaO':1},           'Calcium Oxide',      'Ca + O \u2192 CaO')
_add({'Mg':1,'O':1},       {'MgO':1},           'Magnesium Oxide',    'Mg + O \u2192 MgO')
_add({'Cu':1,'O':1},       {'CuO':1},           'Copper(II) Oxide',   'Cu + O \u2192 CuO')
_add({'Zn':1,'O':1},       {'ZnO':1},           'Zinc Oxide',         'Zn + O \u2192 ZnO')
_add({'Na':2,'O':1},       {'Na\u2082O':1},     'Sodium Oxide',       '2Na + O \u2192 Na\u2082O')
_add({'Mg':1,'Cl':2},      {'MgCl\u2082':1},    'Magnesium Chloride', 'Mg + 2Cl \u2192 MgCl\u2082')

# ── Atom Assembly: Medium Molecules (4-5 atoms) ──
_add({'N':1,'H':3},        {'NH\u2083':1},      'Ammonia',            'N + 3H \u2192 NH\u2083')
_add({'C':1,'H':4},        {'CH\u2084':1},       'Methane',            'C + 4H \u2192 CH\u2084')
_add({'P':1,'Cl':3},       {'PCl\u2083':1},     'Phosphorus Trichloride','P + 3Cl \u2192 PCl\u2083')
_add({'Na':1,'O':1,'H':1}, {'NaOH':1},          'Sodium Hydroxide',   'Na + O + H \u2192 NaOH')
_add({'S':1,'O':3},        {'SO\u2083':1},       'Sulfur Trioxide',    'S + 3O \u2192 SO\u2083')
_add({'H':1,'N':1,'O':3}, {'HNO\u2083':1},      'Nitric Acid',        'H + N + 3O \u2192 HNO\u2083')
_add({'C':2,'H':4},        {'C\u2082H\u2084':1}, 'Ethylene',          '2C + 4H \u2192 C\u2082H\u2084')
_add({'C':2,'H':2},        {'C\u2082H\u2082':1}, 'Acetylene',          '2C + 2H \u2192 C\u2082H\u2082')
_add({'Ca':1,'O':2,'H':2},{'Ca(OH)\u2082':1},  'Calcium Hydroxide', 'Ca + 2O + 2H \u2192 Ca(OH)\u2082')
_add({'Mg':1,'O':2,'H':2},{'Mg(OH)\u2082':1},  'Magnesium Hydroxide','Mg + 2O + 2H \u2192 Mg(OH)\u2082')

# ── Atom Assembly: Complex Molecules (6+ atoms) ──
_add({'C':2,'H':6},        {'C\u2082H\u2086':1},  'Ethane',             '2C + 6H \u2192 C\u2082H\u2086')
_add({'C':3,'H':8},        {'C\u2083H\u2088':1},  'Propane',            '3C + 8H \u2192 C\u2083H\u2088')
_add({'H':3,'P':1,'O':4},  {'H\u2083PO\u2084':1},'Phosphoric Acid',    '3H + P + 4O \u2192 H\u2083PO\u2084')
_add({'H':2,'S':1,'O':4},  {'H\u2082SO\u2084':1},'Sulfuric Acid',     '2H + S + 4O \u2192 H\u2082SO\u2084')
_add({'H':2,'O':2},        {'H\u2082O\u2082':1},  'Hydrogen Peroxide', '2H + 2O \u2192 H\u2082O\u2082')
_add({'Ca':1,'C':1,'O':3}, {'CaCO\u2083':1},     'Calcium Carbonate',  'Ca + C + 3O \u2192 CaCO\u2083')
_add({'Fe':2,'O':3},       {'Fe\u2082O\u2083':1},'Iron Oxide',         '2Fe + 3O \u2192 Fe\u2082O\u2083')
_add({'Al':2,'O':3},       {'Al\u2082O\u2083':1},'Aluminum Oxide',     '2Al + 3O \u2192 Al\u2082O\u2083')
_add({'Zn':1,'Cl':2},      {'ZnCl\u2082':1},     'Zinc Chloride',      'Zn + 2Cl \u2192 ZnCl\u2082')

# ── Molecular Reactions ──
_add({'H\u2082':2,'O\u2082':1},           {'H\u2082O':2},              'Water Synthesis',      '2H\u2082 + O\u2082 \u2192 2H\u2082O')
_add({'N\u2082':1,'H\u2082':3},           {'NH\u2083':2},              'Haber Process',        'N\u2082 + 3H\u2082 \u2192 2NH\u2083')
_add({'Na':2,'Cl\u2082':1},               {'NaCl':2},                 'Salt Formation',       '2Na + Cl\u2082 \u2192 2NaCl')
_add({'H\u2082':1,'Cl\u2082':1},          {'HCl':2},                  'HCl Synthesis',        'H\u2082 + Cl\u2082 \u2192 2HCl')
_add({'CH\u2084':1,'O\u2082':2},          {'CO\u2082':1,'H\u2082O':2},'Methane Combustion',   'CH\u2084 + 2O\u2082 \u2192 CO\u2082 + 2H\u2082O')
_add({'H\u2082O':1,'CO\u2082':1},         {'H\u2082CO\u2083':1},      'Carbonic Acid',        'H\u2082O + CO\u2082 \u2192 H\u2082CO\u2083')
_add({'NH\u2083':1,'HCl':1},              {'NH\u2084Cl':1},            'Ammonium Chloride',    'NH\u2083 + HCl \u2192 NH\u2084Cl')
_add({'NaOH':1,'HCl':1},                  {'NaCl':1,'H\u2082O':1},    'Neutralization',       'NaOH + HCl \u2192 NaCl + H\u2082O')

# ── Molecular Reactions: New Chemistry ──
_add({'CaO':1,'H\u2082O':1},              {'Ca(OH)\u2082':1},         'Slaking Lime',         'CaO + H\u2082O \u2192 Ca(OH)\u2082')
_add({'MgO':1,'H\u2082O':1},              {'Mg(OH)\u2082':1},         'MgO Hydration',        'MgO + H\u2082O \u2192 Mg(OH)\u2082')
_add({'Na\u2082O':1,'H\u2082O':1},         {'NaOH':2},                 'Sodium Oxide + Water','Na\u2082O + H\u2082O \u2192 2NaOH')
_add({'SO\u2082':1,'O\u2082':1},           {'SO\u2083':1},             'SO\u2082 Oxidation',    'SO\u2082 + O\u2082 \u2192 SO\u2083')
_add({'CO':1,'O\u2082':1},                {'CO\u2082':1},             'CO Oxidation',         'CO + O\u2082 \u2192 CO\u2082')
_add({'SO\u2083':1,'H\u2082O':1},          {'H\u2082SO\u2084':1},      'Sulfuric Acid (mol)', 'SO\u2083 + H\u2082O \u2192 H\u2082SO\u2084')
_add({'C\u2082H\u2084':1,'H\u2082':1},     {'C\u2082H\u2086':1},      'Ethylene Hydrogenation','C\u2082H\u2084 + H\u2082 \u2192 C\u2082H\u2086')
_add({'C\u2082H\u2082':1,'H\u2082':1},     {'C\u2082H\u2084':1},      'Acetylene Hydrogenation','C\u2082H\u2082 + H\u2082 \u2192 C\u2082H\u2084')

# ── Molecular Reactions: Combustion ──
_add({'C\u2082H\u2084':1,'O\u2082':3},     {'CO\u2082':2,'H\u2082O':2},'Ethylene Combustion', 'C\u2082H\u2084 + 3O\u2082 \u2192 2CO\u2082 + 2H\u2082O')
_add({'C\u2083H\u2088':1,'O\u2082':5},     {'CO\u2082':3,'H\u2082O':4},'Propane Combustion',  'C\u2083H\u2088 + 5O\u2082 \u2192 3CO\u2082 + 4H\u2082O')

# ── Molecular Reactions: Displacement & Redox ──
_add({'Mg':1,'HCl':2},                    {'MgCl\u2082':1,'H\u2082':1},'Mg Displacement',      'Mg + 2HCl \u2192 MgCl\u2082 + H\u2082')
_add({'Zn':1,'HCl':2},                    {'ZnCl\u2082':1,'H\u2082':1},'Zn Displacement',      'Zn + 2HCl \u2192 ZnCl\u2082 + H\u2082')
_add({'CuO':1,'H\u2082':1},               {'Cu':1,'H\u2082O':1},      'CuO Reduction',        'CuO + H\u2082 \u2192 Cu + H\u2082O')
_add({'Fe\u2082O\u2083':1,'CO':3},        {'Fe':2,'CO\u2082':3},     'Blast Furnace',        'Fe\u2082O\u2083 + 3CO \u2192 2Fe + 3CO\u2082')

# ── Atom Assembly: New Metal Oxides ──
_add({'Mn':1,'O':1},       {'MnO':1},           'Manganese(II) Oxide',  'Mn + O \u2192 MnO')
_add({'Mn':1,'O':2},       {'MnO\u2082':1},      'Manganese(IV) Oxide',  'Mn + 2O \u2192 MnO\u2082')
_add({'Cr':2,'O':3},       {'Cr\u2082O\u2083':1},  'Chromium(III) Oxide',  '2Cr + 3O \u2192 Cr\u2082O\u2083')
_add({'Ni':1,'O':1},       {'NiO':1},           'Nickel(II) Oxide',     'Ni + O \u2192 NiO')
_add({'Sn':1,'O':2},       {'SnO\u2082':1},      'Tin(IV) Oxide',       'Sn + 2O \u2192 SnO\u2082')
_add({'Pb':1,'O':1},       {'PbO':1},           'Lead(II) Oxide',       'Pb + O \u2192 PbO')
_add({'Ba':1,'O':1},       {'BaO':1},           'Barium Oxide',         'Ba + O \u2192 BaO')
_add({'Ti':1,'O':2},       {'TiO\u2082':1},      'Titanium(IV) Oxide',   'Ti + 2O \u2192 TiO\u2082')

# ── Atom Assembly: Metal Sulfides ──
_add({'Fe':1,'S':1},       {'FeS':1},           'Iron(II) Sulfide',     'Fe + S \u2192 FeS')
_add({'Cu':1,'S':1},       {'CuS':1},           'Copper(II) Sulfide',   'Cu + S \u2192 CuS')
_add({'Zn':1,'S':1},       {'ZnS':1},           'Zinc Sulfide',         'Zn + S \u2192 ZnS')

# ── Atom Assembly: Metal Chlorides (extended) ──
_add({'Al':1,'Cl':3},      {'AlCl\u2083':1},     'Aluminum Chloride',    'Al + 3Cl \u2192 AlCl\u2083')
_add({'Ca':1,'Cl':2},      {'CaCl\u2082':1},     'Calcium Chloride',     'Ca + 2Cl \u2192 CaCl\u2082')
_add({'Cu':1,'Cl':2},      {'CuCl\u2082':1},     'Copper(II) Chloride',  'Cu + 2Cl \u2192 CuCl\u2082')
_add({'Fe':1,'Cl':2},      {'FeCl\u2082':1},     'Iron(II) Chloride',    'Fe + 2Cl \u2192 FeCl\u2082')
_add({'Fe':1,'Cl':3},      {'FeCl\u2083':1},     'Iron(III) Chloride',   'Fe + 3Cl \u2192 FeCl\u2083')
_add({'Ba':1,'Cl':2},      {'BaCl\u2082':1},     'Barium Chloride',      'Ba + 2Cl \u2192 BaCl\u2082')
_add({'Mn':1,'Cl':2},      {'MnCl\u2082':1},     'Manganese(II) Chloride','Mn + 2Cl \u2192 MnCl\u2082')

# ── Atom Assembly: Alkali Compounds ──
_add({'K':1,'O':1,'H':1},  {'KOH':1},           'Potassium Hydroxide',  'K + O + H \u2192 KOH')
_add({'K':2,'O':1},        {'K\u2082O':1},      'Potassium Oxide',      '2K + O \u2192 K\u2082O')
_add({'Na':1,'Br':1},      {'NaBr':1},          'Sodium Bromide',       'Na + Br \u2192 NaBr')
_add({'Na':1,'I':1},       {'NaI':1},           'Sodium Iodide',        'Na + I \u2192 NaI')
_add({'K':1,'Br':1},       {'KBr':1},           'Potassium Bromide',    'K + Br \u2192 KBr')
_add({'K':1,'I':1},        {'KI':1},            'Potassium Iodide',     'K + I \u2192 KI')
_add({'Ba':1,'O':2,'H':2},{'Ba(OH)\u2082':1}, 'Barium Hydroxide',     'Ba + 2O + 2H \u2192 Ba(OH)\u2082')

# ── Atom Assembly: Sulfates ──
_add({'Na':2,'S':1,'O':4},{'Na\u2082SO\u2084':1},'Sodium Sulfate',       '2Na + S + 4O \u2192 Na\u2082SO\u2084')
_add({'Ca':1,'S':1,'O':4},{'CaSO\u2084':1},    'Calcium Sulfate',       'Ca + S + 4O \u2192 CaSO\u2084')
_add({'Ba':1,'S':1,'O':4},{'BaSO\u2084':1},    'Barium Sulfate',        'Ba + S + 4O \u2192 BaSO\u2084')

# ── Atom Assembly: Other ──
_add({'Pb':1,'I':2},       {'PbI\u2082':1},     'Lead(II) Iodide',       'Pb + 2I \u2192 PbI\u2082')

# ── Molecular Reactions: New Chemistry (extended) ──
_add({'Na\u2082O':1,'SO\u2083':1},           {'Na\u2082SO\u2084':1}, 'Sodium Sulfate (mol)','Na\u2082O + SO\u2083 \u2192 Na\u2082SO\u2084')
_add({'CaO':1,'SO\u2083':1},                  {'CaSO\u2084':1},        'Calcium Sulfate (mol)','CaO + SO\u2083 \u2192 CaSO\u2084')
_add({'BaO':1,'SO\u2083':1},                  {'BaSO\u2084':1},        'Barium Sulfate (mol)','BaO + SO\u2083 \u2192 BaSO\u2084')
_add({'BaO':1,'H\u2082O':1},                  {'Ba(OH)\u2082':1},      'BaO Hydration',       'BaO + H\u2082O \u2192 Ba(OH)\u2082')
_add({'K\u2082O':1,'H\u2082O':1},             {'KOH':2},               'Potassium Oxide + Water', 'K\u2082O + H\u2082O \u2192 2KOH')

# ── Molecular Reactions: Displacement (extended) ──
_add({'Fe':1,'CuCl\u2082':1},                 {'FeCl\u2082':1,'Cu':1},'Fe Displaces Cu',      'Fe + CuCl\u2082 \u2192 FeCl\u2082 + Cu')
_add({'Zn':1,'CuCl\u2082':1},                 {'ZnCl\u2082':1,'Cu':1},'Zn Displaces Cu',      'Zn + CuCl\u2082 \u2192 ZnCl\u2082 + Cu')
_add({'Na':2,'H\u2082O':2},                   {'NaOH':2,'H\u2082':1},  'Sodium + Water',       '2Na + 2H\u2082O \u2192 2NaOH + H\u2082')
_add({'K':2,'H\u2082O':2},                    {'KOH':2,'H\u2082':1},   'Potassium + Water',    '2K + 2H\u2082O \u2192 2KOH + H\u2082')
_add({'BaCl\u2082':1,'Na\u2082SO\u2084':1}, {'BaSO\u2084':1,'NaCl':2},'Precipitation Rxn',   'BaCl\u2082 + Na\u2082SO\u2084 \u2192 BaSO\u2084 + 2NaCl')
_add({'MnO\u2082':1,'HCl':4},                 {'MnCl\u2082':1,'Cl\u2082':1,'H\u2082O':2},'MnO\u2082 + HCl','MnO\u2082 + 4HCl \u2192 MnCl\u2082 + Cl\u2082 + 2H\u2082O')
_add({'PbO':1,'C':1},                          {'Pb':1,'CO':1},         'PbO Reduction (C)',   'PbO + C \u2192 Pb + CO')
_add({'SnO\u2082':1,'C':2},                   {'Sn':1,'CO\u2082':2},  'Sn Smelting (C)',     'SnO\u2082 + 2C \u2192 Sn + 2CO\u2082')

NUM_SLOTS = 12

def find_recipe(reactor_items):
    rc = Counter(reactor_items)
    best = None
    for reactants, products, name, eq in ALL_RECIPES:
        if Counter(reactants) == rc:
            if best is None or sum(reactants.values()) > sum(best[0].values()):
                best = (reactants, products, name, eq)
    return best

# ═══════════════════════════════════════════════════════════════════════════════
#  LEVELS (35 total)
# ═══════════════════════════════════════════════════════════════════════════════
LEVELS = [
    {'name':'First Bonds',
     'desc':'Combine hydrogen atoms to form H\u2082 gas',
     'avail':{'H':6}, 'obj':{'H\u2082':3},
     'hint':'Put 2 Hydrogen atoms in the reactor \u2192 H\u2082'},
    {'name':'Making Water',
     'desc':'Build water molecules from hydrogen and oxygen atoms',
     'avail':{'H':6,'O':3}, 'obj':{'H\u2082O':3},
     'hint':'Put 2H + 1O in the reactor \u2192 H\u2082O'},
    {'name':'Diatomic Gases',
     'desc':'Create hydrogen, oxygen, and nitrogen gases from atoms',
     'avail':{'H':4,'O':4,'N':4}, 'obj':{'H\u2082':1,'O\u2082':1,'N\u2082':1},
     'hint':'Each gas needs 2 atoms of the same element'},
    {'name':'Ammonia Factory',
     'desc':'Build ammonia from nitrogen and hydrogen atoms',
     'avail':{'N':3,'H':12}, 'obj':{'NH\u2083':3},
     'hint':'N + 3H \u2192 NH\u2083'},
    {'name':'Salty Business',
     'desc':'Produce table salt from sodium and chlorine atoms',
     'avail':{'Na':4,'Cl':4}, 'obj':{'NaCl':4},
     'hint':'Na + Cl \u2192 NaCl'},
    {'name':'Methane Synthesis',
     'desc':'Create methane gas from carbon and hydrogen',
     'avail':{'C':2,'H':10}, 'obj':{'CH\u2084':2},
     'hint':'C + 4H \u2192 CH\u2084 (5 items!)'},
    {'name':'Water Synthesis Lab',
     'desc':'React hydrogen and oxygen gases to produce water',
     'avail':{'H\u2082':6,'O\u2082':3}, 'obj':{'H\u2082O':6},
     'hint':'2H\u2082 + O\u2082 \u2192 2H\u2082O (molecular reaction!)'},
    {'name':'Haber Process',
     'desc':'Industrial ammonia synthesis from nitrogen and hydrogen gases',
     'avail':{'N\u2082':2,'H\u2082':6}, 'obj':{'NH\u2083':4},
     'hint':'N\u2082 + 3H\u2082 \u2192 2NH\u2083 (4 items in reactor)'},
    {'name':'Combustion!',
     'desc':'Burn methane with oxygen to produce CO\u2082 and water',
     'avail':{'CH\u2084':3,'O\u2082':6}, 'obj':{'CO\u2082':3,'H\u2082O':6},
     'hint':'CH\u2084 + 2O\u2082 \u2192 CO\u2082 + 2H\u2082O'},
    {'name':'Neutralization',
     'desc':'Mix acid and base for a classic neutralization reaction',
     'avail':{'NaOH':3,'HCl':3}, 'obj':{'NaCl':3,'H\u2082O':3},
     'hint':'NaOH + HCl \u2192 NaCl + H\u2082O'},
    {'name':'Two-Step Water',
     'desc':'Build H\u2082 and O\u2082 from atoms, then react them into water',
     'avail':{'H':10,'O':5}, 'obj':{'H\u2082O':5},
     'hint':'Step 1: H+H\u2192H\u2082, O+O\u2192O\u2082  Step 2: 2H\u2082+O\u2082\u21922H\u2082O'},
    {'name':'Build & React',
     'desc':'Assemble molecules from atoms, then combine them',
     'avail':{'H':14,'O':8,'C':2,'N':3}, 'obj':{'H\u2082O':2,'CO\u2082':2,'NH\u2083':3},
     'hint':'Build from atoms OR use molecular reactions \u2014 your choice!'},
    {'name':'Acid Rain',
     'desc':'Create hydrochloric acid from hydrogen and chlorine gases',
     'avail':{'H\u2082':4,'Cl\u2082':2}, 'obj':{'HCl':4},
     'hint':'H\u2082 + Cl\u2082 \u2192 2HCl'},
    {'name':'Chemical Kitchen',
     'desc':'Multiple molecules needed \u2014 plan your reactions!',
     'avail':{'H':14,'O':10,'C':3,'N':3,'Na':2,'Cl':2},
     'obj':{'H\u2082O':3,'CO\u2082':2,'NH\u2083':2,'NaCl':2},
     'hint':'Mix direct atom assembly and molecular reactions!'},

    # ── NEW LEVELS (15-23) ──
    {'name':'Carbon Monoxide',
     'desc':'Create carbon monoxide from carbon and oxygen',
     'avail':{'C':4,'O':4}, 'obj':{'CO':3,'CO\u2082':1},
     'hint':'C + O \u2192 CO (monoxide) or C + 2O \u2192 CO\u2082 (dioxide)'},
    {'name':'Oxides Galore',
     'desc':'Produce various metal oxides from atoms',
     'avail':{'Ca':2,'Mg':2,'Cu':2,'Zn':2,'O':8}, 'obj':{'CaO':2,'MgO':2,'CuO':2,'ZnO':2},
     'hint':'Each metal oxide needs 1 Metal + 1 Oxygen atom'},
    {'name':'Hydrogen Halides',
     'desc':'Create the hydrogen halide series: HF, HCl, HBr, HI',
     'avail':{'H':8,'F':2,'Cl':2,'Br':2,'I':2}, 'obj':{'HF':2,'HCl':2,'HBr':2,'HI':2},
     'hint':'Each hydrogen halide = 1H + 1 halogen atom'},
    {'name':'Acid Factory',
     'desc':'Produce nitric acid, sulfuric acid, and phosphoric acid',
     'avail':{'H':10,'N':2,'S':2,'P':2,'O':16}, 'obj':{'HNO\u2083':2,'H\u2082SO\u2084':2,'H\u2083PO\u2084':2},
     'hint':'HNO\u2083: H+N+3O | H\u2082SO\u2084: 2H+S+4O | H\u2083PO\u2084: 3H+P+4O'},
    {'name':'Metal Displacement',
     'desc':'Magnesium and Zinc displace hydrogen from HCl!',
     'avail':{'Mg':2,'Zn':2,'HCl':8}, 'obj':{'MgCl\u2082':2,'ZnCl\u2082':2,'H\u2082':4},
     'hint':'Mg + 2HCl \u2192 MgCl\u2082 + H\u2082 (atoms + molecules together!)'},
    {'name':'Fuel Combustion',
     'desc':'Burn ethylene and propane with oxygen',
     'avail':{'C\u2082H\u2084':2,'C\u2083H\u2088':1,'O\u2082':14}, 'obj':{'CO\u2082':7,'H\u2082O':8},
     'hint':'C\u2082H\u2084+3O\u2082\u21922CO\u2082+2H\u2082O | C\u2083H\u2088+5O\u2082\u21923CO\u2082+4H\u2082O'},
    {'name':'Blast Furnace',
     'desc':'Extract iron from iron oxide using carbon monoxide!',
     'avail':{'Fe\u2082O\u2083':2,'CO':6}, 'obj':{'Fe':4,'CO\u2082':6},
     'hint':'Fe\u2082O\u2083 + 3CO \u2192 2Fe + 3CO\u2082 (4 items, run twice)'},
    {'name':'Copper Reduction',
     'desc':'Reduce copper oxide with hydrogen gas to recover copper metal',
     'avail':{'CuO':3,'H\u2082':3}, 'obj':{'Cu':3,'H\u2082O':3},
     'hint':'CuO + H\u2082 \u2192 Cu + H\u2082O (products include atoms!)'},
    {'name':'Hydrocarbon Builder',
     'desc':'Build methane, ethylene, and propane from carbon and hydrogen',
     'avail':{'C':8,'H':18}, 'obj':{'CH\u2084':1,'C\u2082H\u2084':1,'C\u2083H\u2088':1},
     'hint':'CH\u2084: C+4H | C\u2082H\u2084: 2C+4H | C\u2083H\u2088: 3C+8H'},

    # ── NEW LEVELS (24-35) ──
    {'name':'Metal Sulfides',
     'desc':'Create iron, copper, and zinc sulfides from metal and sulfur atoms',
     'avail':{'Fe':3,'Cu':3,'Zn':3,'S':9}, 'obj':{'FeS':3,'CuS':3,'ZnS':3},
     'hint':'Each metal sulfide needs 1 Metal + 1 Sulfur atom'},
    {'name':'Alkali Halides',
     'desc':'Produce sodium and potassium halides from alkali metals and halogens',
     'avail':{'Na':4,'K':4,'F':2,'Cl':2,'Br':2,'I':2},
     'obj':{'NaF':2,'NaBr':2,'KBr':2,'KI':2},
     'hint':'Na+F\u2192NaF, Na+Br\u2192NaBr, K+Br\u2192KBr, K+I\u2192KI'},
    {'name':'Oxide Collection',
     'desc':'Produce a variety of metal oxides from atoms',
     'avail':{'Mn':2,'Cr':2,'Ni':2,'Sn':2,'Pb':2,'Ba':2,'Ti':2,'O':17},
     'obj':{'MnO':1,'MnO\u2082':1,'Cr\u2082O\u2083':1,'NiO':2,'SnO\u2082':1,'PbO':1,'BaO':1,'TiO\u2082':1},
     'hint':'Most need Metal+O. MnO\u2082/SnO\u2082/TiO\u2082 need Metal+2O. Cr\u2082O\u2083 needs 2Cr+3O'},
    {'name':'Aluminum & Iron Chlorides',
     'desc':'Produce various metal chlorides from atoms',
     'avail':{'Al':3,'Fe':4,'Ca':2,'Cl':17}, 'obj':{'AlCl\u2083':3,'FeCl\u2082':2,'FeCl\u2083':2,'CaCl\u2082':2},
     'hint':'AlCl\u2083: Al+3Cl | FeCl\u2082: Fe+2Cl | FeCl\u2083: Fe+3Cl | CaCl\u2082: Ca+2Cl'},
    {'name':'Alkali Hydroxides',
     'desc':'Create NaOH and KOH using atom assembly and molecular reactions',
     'avail':{'Na':4,'K':4,'O':6,'H':6,'H\u2082O':2},
     'obj':{'NaOH':4,'KOH':4},
     'hint':'Na+O+H\u2192NaOH or K\u2082O+H\u2082O\u21922KOH'},
    {'name':'Sulfate Factory',
     'desc':'Build sodium, calcium, and barium sulfates from atoms',
     'avail':{'Na':2,'Ca':1,'Ba':1,'S':3,'O':12}, 'obj':{'Na\u2082SO\u2084':1,'CaSO\u2084':1,'BaSO\u2084':1},
     'hint':'Na\u2082SO\u2084: 2Na+S+4O | CaSO\u2084: Ca+S+4O | BaSO\u2084: Ba+S+4O'},
    {'name':'Precipitation Lab',
     'desc':'Create BaCl\u2082 and Na\u2082SO\u2084, then react them for a precipitate!',
     'avail':{'Ba':2,'Cl':6,'Na':4,'S':2,'O':10},
     'obj':{'BaSO\u2084':2,'NaCl':4},
     'hint':'Build BaCl\u2082 (Ba+2Cl) and Na\u2082SO\u2084 (2Na+S+4O), then: BaCl\u2082+Na\u2082SO\u2084\u2192BaSO\u2084+2NaCl'},
    {'name':'Alkali Metal + Water',
     'desc':'React sodium and potassium metals with water!',
     'avail':{'Na':4,'K':4,'H\u2082O':8}, 'obj':{'NaOH':4,'KOH':4,'H\u2082':4},
     'hint':'2Na + 2H\u2082O \u2192 2NaOH + H\u2082 | 2K + 2H\u2082O \u2192 2KOH + H\u2082'},
    {'name':'Displacement Series',
     'desc':'Iron and Zinc displace copper from copper(II) chloride!',
     'avail':{'Fe':2,'Zn':2,'CuCl\u2082':4}, 'obj':{'FeCl\u2082':2,'ZnCl\u2082':2,'Cu':4},
     'hint':'Fe + CuCl\u2082 \u2192 FeCl\u2082 + Cu | Zn + CuCl\u2082 \u2192 ZnCl\u2082 + Cu'},
    {'name':'Lead & Tin Smelting',
     'desc':'Reduce lead and tin oxides using carbon!',
     'avail':{'PbO':3,'SnO\u2082':2,'C':7}, 'obj':{'Pb':3,'Sn':2,'CO':3,'CO\u2082':2},
     'hint':'PbO + C \u2192 Pb + CO | SnO\u2082 + 2C \u2192 Sn + 2CO\u2082'},
    {'name':'MnO\u2082 Reactions',
     'desc':'Use manganese(IV) oxide in reactions with hydrochloric acid!',
     'avail':{'MnO\u2082':2,'HCl':8}, 'obj':{'MnCl\u2082':2,'Cl\u2082':2,'H\u2082O':4},
     'hint':'MnO\u2082 + 4HCl \u2192 MnCl\u2082 + Cl\u2082 + 2H\u2082O (5 items in reactor)'},
    {'name':'Ultimate Chemistry',
     'desc':'A grand challenge using atoms, molecules, and multi-step synthesis!',
     'avail':{'Fe':3,'Zn':3,'Cu':2,'Na':4,'K':2,'H':10,'O':12,'C':4,'S':2,'Cl':8},
     'obj':{'FeS':1,'ZnS':1,'NaOH':2,'KOH':2,'CO\u2082':2,'H\u2082O':2,'NaCl':2,'H\u2082':2},
     'hint':'Use displacement (Fe+CuCl\u2082), alkali+water (2Na+2H\u2082O), combustion (CH\u2084+2O\u2082), salt formation (2Na+Cl\u2082)!'},
]

# ═══════════════════════════════════════════════════════════════════════════════
#  DRAWING HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def rrect(surf, col, rect, rad=10, w=0):
    pygame.draw.rect(surf, col, rect, width=w, border_radius=rad)

def draw_mol_vis(surf, formula, cx, cy, scale=1.0):
    if formula not in MOL: return
    _, col, atoms, bonds, is_atom = MOL[formula]
    pts = [(cx+dx*scale, cy+dy*scale, e) for dx,dy,e in atoms]
    for i,j in bonds:
        x1,y1,_=pts[i]; x2,y2,_=pts[j]
        c = tuple(max(0,min(255,v-60)) for v in col)
        pygame.draw.line(surf,c,(int(x1),int(y1)),(int(x2),int(y2)),max(1,int(2*scale)))
    for x,y,e in pts:
        r = int(AR.get(e,8)*scale)
        ec = EC.get(e,(180,180,180))
        pygame.draw.circle(surf,ec,(int(x),int(y)),r)
        if scale >= 0.7:
            ts = FX.render(e,True,(0,0,0) if sum(ec)>400 else (255,255,255))
            surf.blit(ts,(int(x)-ts.get_width()//2, int(y)-ts.get_height()//2))

def draw_card(surf, formula, x, y, w=115, h=58, count=0, hover=False, ghost=False):
    if formula not in MOL: return pygame.Rect(x,y,w,h)
    name, col, atoms, bonds, is_atom = MOL[formula]
    r = pygame.Rect(x,y,w,h)
    bg = tuple(min(255,c+40) for c in col) if hover else tuple(min(255,c+20) for c in col)
    if ghost:
        s=pygame.Surface((w,h),pygame.SRCALPHA); s.fill((*bg,150)); surf.blit(s,(x,y))
    else:
        rrect(surf,bg,r,8); rrect(surf,tuple(min(255,c+70) for c in col),r,8,2)
    if is_atom:
        draw_mol_vis(surf, formula, x+w//2, y+h//2, scale=1.3)
    else:
        draw_mol_vis(surf, formula, x+w-28, y+20, scale=0.6)
        ft = FF.render(formula, True, (255,255,255))
        surf.blit(ft, (x+8, y+(h-ft.get_height())//2-4))
    if count > 1 and not ghost:
        br = pygame.Rect(x+w-18, y-2, 22, 18)
        rrect(surf, YELLOW, br, 9)
        ct = FSB.render(str(count), True, (20,20,20))
        surf.blit(ct, (br.centerx-ct.get_width()//2, br.centery-ct.get_height()//2))
    return r

def dtxt(surf, text, font, col, cx, cy):
    t=font.render(text,True,col); surf.blit(t,(cx-t.get_width()//2, cy-t.get_height()//2))

def dtxt_l(surf, text, font, col, x, y):
    t=font.render(text,True,col); surf.blit(t,(x,y)); return t.get_rect(topleft=(x,y))

# ═══════════════════════════════════════════════════════════════════════════════
#  PARTICLES
# ═══════════════════════════════════════════════════════════════════════════════
class Particle:
    __slots__=['x','y','vx','vy','life','ml','color','r']
    def __init__(self,x,y,color):
        a=random.uniform(0,6.283); s=random.uniform(80,260)
        self.x=x;self.y=y;self.vx=math.cos(a)*s;self.vy=math.sin(a)*s
        self.life=self.ml=random.uniform(0.4,1.1);self.color=color;self.r=random.uniform(2,5)
    def update(self,dt):
        self.x+=self.vx*dt;self.y+=self.vy*dt;self.vy+=130*dt;self.life-=dt;return self.life>0
    def draw(self,surf):
        a=max(0,min(255,int(255*(self.life/self.ml)))); r=max(1,int(self.r*(self.life/self.ml)))
        s=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(s,(*self.color,a),(r,r),r); surf.blit(s,(int(self.x)-r,int(self.y)-r))

particles=[]
def spawn_p(x,y,col,n=30):
    for _ in range(n): particles.append(Particle(x,y,col))

class FAtom:
    def __init__(self):
        self.x=random.uniform(0,W);self.y=random.uniform(0,H)
        self.e=random.choice(list(EC.keys()))
        self.r=AR.get(self.e,8)*random.uniform(1.5,3)
        self.vx=random.uniform(-18,18);self.vy=random.uniform(-18,18)
        self.ph=random.uniform(0,6.283)
    def update(self,dt,t):
        self.x+=self.vx*dt;self.y+=self.vy*dt+math.sin(t*0.5+self.ph)*0.3
        if self.x<-20:self.x=W+20
        if self.x>W+20:self.x=-20
        if self.y<-20:self.y=H+20
        if self.y>H+20:self.y=-20
    def draw(self,surf,t):
        a=int(40+20*math.sin(t+self.ph));c=EC.get(self.e,(150,150,150))
        s=pygame.Surface((int(self.r*2+4),int(self.r*2+4)),pygame.SRCALPHA)
        pygame.draw.circle(s,(*c,a),(int(self.r+2),int(self.r+2)),int(self.r))
        surf.blit(s,(int(self.x-self.r-2),int(self.y-self.r-2)))

fatoms=[FAtom() for _ in range(30)]

# ═══════════════════════════════════════════════════════════════════════════════
#  GAME STATE
# ═══════════════════════════════════════════════════════════════════════════════
ST_TITLE=0; ST_LEVELS=1; ST_PLAY=2; ST_WIN=3
state=ST_TITLE; cur_lv=0
inventory={}; reactor=[None]*NUM_SLOTS
objectives={}; msg_text=""; msg_timer=0; msg_color=GREEN
hint_vis=False; show_rec=False; win_timer=0; time_tot=0.0
dragging=False; drag_formula=None; drag_src=None; drag_off=(0,0); mpos=(0,0)

inv_rects={}; slot_rects=[pygame.Rect(0,0,0,0)]*NUM_SLOTS
react_btn=pygame.Rect(0,0,0,0); clear_btn=pygame.Rect(0,0,0,0)
reset_btn=pygame.Rect(0,0,0,0); hint_btn=pygame.Rect(0,0,0,0)
recipe_btn=pygame.Rect(0,0,0,0); level_rects=[]
back_btn=pygame.Rect(0,0,0,0); next_btn=pygame.Rect(0,0,0,0)
menu_btn=pygame.Rect(0,0,0,0)

INV_X,INV_Y,INV_W,INV_H = 10,65,255,700
REA_X,REA_Y,REA_W,REA_H = 275,65,730,700
OBJ_X,OBJ_Y,OBJ_W,OBJ_H = 1015,65,255,700
CARD_W,CARD_H = 118,56
SLOT_W,SLOT_H = 108,82

def load_lv(idx):
    global inventory,reactor,objectives,hint_vis,win_timer,time_tot
    lv=LEVELS[idx]; inventory=dict(lv['avail']); reactor=[None]*NUM_SLOTS
    objectives={f:(n,0) for f,n in lv['obj'].items()}
    hint_vis=False; win_timer=0; time_tot=0.0

def show_msg(t,c=GREEN,d=2.0):
    global msg_text,msg_timer,msg_color; msg_text=t;msg_timer=d;msg_color=c

def get_recipe():
    items=[r for r in reactor if r]
    return find_recipe(items) if items else None

def is_complete():
    return all(m>=n for n,m in objectives.values())

# ═══════════════════════════════════════════════════════════════════════════════
#  EVENTS
# ═══════════════════════════════════════════════════════════════════════════════
def handle_ev(ev):
    global state,cur_lv,dragging,drag_formula,drag_src,drag_off,mpos
    global hint_vis,show_rec
    if ev.type==pygame.MOUSEMOTION: mpos=ev.pos
    if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
        mx,my=ev.pos
        if state==ST_TITLE: state=ST_LEVELS
        elif state==ST_LEVELS:
            if back_btn.collidepoint(mx,my): state=ST_TITLE
            for i,r in enumerate(level_rects):
                if r.collidepoint(mx,my): cur_lv=i; load_lv(i); state=ST_PLAY
        elif state==ST_PLAY:
            if hint_btn.collidepoint(mx,my): hint_vis=not hint_vis; return
            if recipe_btn.collidepoint(mx,my): show_rec=not show_rec; return
            if clear_btn.collidepoint(mx,my): clear_reactor(); return
            if reset_btn.collidepoint(mx,my): load_lv(cur_lv); return
            if react_btn.collidepoint(mx,my): do_react(); return
            for formula,rect in inv_rects.items():
                if rect.collidepoint(mx,my) and inventory.get(formula,0)>0:
                    dragging=True;drag_formula=formula;drag_src='inv'
                    drag_off=(mx-rect.x,my-rect.y);inventory[formula]-=1;return
            for i,sr in enumerate(slot_rects):
                if sr.collidepoint(mx,my) and reactor[i]:
                    dragging=True;drag_formula=reactor[i];drag_src=('slot',i)
                    drag_off=(mx-sr.x,my-sr.y);reactor[i]=None;return
        elif state==ST_WIN:
            if next_btn.collidepoint(mx,my):
                if cur_lv+1<len(LEVELS): cur_lv+=1;load_lv(cur_lv);state=ST_PLAY
                else: state=ST_LEVELS
            if menu_btn.collidepoint(mx,my): state=ST_LEVELS
    if ev.type==pygame.MOUSEBUTTONUP and ev.button==1 and dragging:
        mx,my=ev.pos; placed=False
        for i,sr in enumerate(slot_rects):
            if sr.collidepoint(mx,my) and reactor[i] is None:
                reactor[i]=drag_formula;placed=True;break
        if not placed: inventory[drag_formula]=inventory.get(drag_formula,0)+1
        dragging=False;drag_formula=None;drag_src=None
    if ev.type==pygame.KEYDOWN:
        if state==ST_PLAY:
            if ev.key==pygame.K_h: hint_vis=not hint_vis
            elif ev.key==pygame.K_r: load_lv(cur_lv)
            elif ev.key==pygame.K_TAB: show_rec=not show_rec
            elif ev.key==pygame.K_ESCAPE:
                if show_rec: show_rec=False
                else: state=ST_LEVELS
        elif state in (ST_TITLE,ST_LEVELS,ST_WIN):
            if ev.key==pygame.K_ESCAPE: state=ST_TITLE

def clear_reactor():
    global dragging,drag_formula
    for i in range(NUM_SLOTS):
        if reactor[i]: inventory[reactor[i]]=inventory.get(reactor[i],0)+1; reactor[i]=None
    dragging=False;drag_formula=None

def do_react():
    global state,win_timer
    r=get_recipe()
    if not r: show_msg("No reaction! Try a different combination.",RED,1.5); return
    reactants,products,name,eq=r
    rcx=REA_X+REA_W//2; rcy=REA_Y+REA_H//2-50
    for pf,qty in products.items():
        col=MOL[pf][1] if pf in MOL else ACCENT
        spawn_p(rcx,rcy,col,25)
    spawn_p(rcx,rcy,(255,255,200),15)
    for i in range(NUM_SLOTS): reactor[i]=None
    for pf,qty in products.items():
        inventory[pf]=inventory.get(pf,0)+qty
    for pf,qty in products.items():
        if pf in objectives:
            n,m=objectives[pf]; objectives[pf]=(n,min(n,m+qty))
    r_str = " + ".join(f"{v}{k}" if v>1 else k for k,v in reactants.items())
    p_str = " + ".join(f"{v}{k}" if v>1 else k for k,v in products.items())
    show_msg(f"{name}: {r_str} \u2192 {p_str}",GREEN,2.5)
    if is_complete(): win_timer=1.5

# ═══════════════════════════════════════════════════════════════════════════════
#  UPDATE & DRAW
# ═══════════════════════════════════════════════════════════════════════════════
def update(dt):
    global particles,win_timer,msg_timer,state,time_tot
    particles=[p for p in particles if p.update(dt)]
    if msg_timer>0: msg_timer-=dt
    if win_timer>0:
        win_timer-=dt
        if win_timer<=0: state=ST_WIN
    if state==ST_PLAY: time_tot+=dt

def draw():
    screen.fill(BG)
    t=pygame.time.get_ticks()/1000.0
    if state==ST_TITLE: draw_title(t)
    elif state==ST_LEVELS: draw_levels(t)
    elif state==ST_PLAY: draw_game(t)
    elif state==ST_WIN: draw_game(t); draw_win(t)
    pygame.display.flip()

def draw_title(t):
    for a in fatoms: a.update(1/FPS,t); a.draw(screen,t)
    g=int(180+60*math.sin(t*2))
    dtxt(screen,"CHEMISTRY LAB",FT,(g,g,255),W//2,H//2-110)
    dtxt(screen,"Molecule Combiner",FL,(150,160,200),W//2,H//2-60)
    dtxt(screen,"Build molecules from atoms \u2022 React molecules together!",FM,TXT_D,W//2,H//2-15)
    dtxt(screen,"31 elements \u2022 80+ molecules \u2022 100+ recipes \u2022 35 levels",FS,ACCENT,W//2,H//2+15)
    al=int(128+127*math.sin(t*3))
    s=pygame.Surface((320,44),pygame.SRCALPHA)
    rrect(s,(0,175,255,al),(0,0,320,44),22); screen.blit(s,(W//2-160,H//2+60))
    dtxt(screen,"Click to Start",FMB,(255,255,255),W//2,H//2+82)

def draw_levels(t):
    global level_rects,back_btn
    dtxt(screen,"Select a Level",FT,ACCENT,W//2,45)
    cols,cw,ch,gap=4,260,95,12
    tw=cols*cw+(cols-1)*gap; sx=(W-tw)//2; sy=90
    level_rects=[]; mx,my=mpos
    for i,lv in enumerate(LEVELS):
        row,col=divmod(i,cols); x=sx+col*(cw+gap); y=sy+row*(ch+gap)
        r=pygame.Rect(x,y,cw,ch); level_rects.append(r)
        hov=r.collidepoint(mx,my)
        rrect(screen,BTN_H if hov else BTN,r,12)
        rrect(screen,ACCENT if hov else BORDER,r,12,2)
        dtxt(screen,f"Level {i+1}",FMB,ACCENT,r.centerx,r.y+18)
        dtxt(screen,lv['name'],FS,TXT,r.centerx,r.y+42)
        objs=", ".join(lv['obj'].keys())
        dtxt(screen,objs,FX,TXT_D,r.centerx,r.y+62)
        items_sum=sum(lv['avail'].values())
        dtxt(screen,f"{items_sum} items \u2022 {len(lv['obj'])} obj",FX,TXT_D,r.centerx,r.y+78)
    # Page navigation hint
    total_pages = (len(LEVELS) + cols - 1) // cols
    cur_page = 0  # simple: show all for now
    back_btn=pygame.Rect(W//2-80,H-60,160,42)
    hov=back_btn.collidepoint(mx,my)
    rrect(screen,BTN_H if hov else BTN,back_btn,10)
    dtxt(screen,"Back",FMB,TXT,back_btn.centerx,back_btn.centery)

def draw_game(t):
    global inv_rects,slot_rects,react_btn,clear_btn,reset_btn,hint_btn,recipe_btn
    mx,my=mpos; lv=LEVELS[cur_lv]
    # Top bar
    rrect(screen,PANEL,(0,0,W,55),0); pygame.draw.line(screen,BORDER,(0,55),(W,55),1)
    dtxt_l(screen,f"Level {cur_lv+1}: {lv['name']}",FL,ACCENT,18,12)
    mins,secs=divmod(int(time_tot),60)
    dtxt_l(screen,f"Time: {mins:02d}:{secs:02d}",FS,TXT_D,W-170,18)

    # Inventory panel
    rrect(screen,PANEL,(INV_X,INV_Y,INV_W,INV_H),10)
    dtxt_l(screen,"Inventory",FMB,ACCENT,INV_X+12,INV_Y+8)
    pygame.draw.line(screen,BORDER,(INV_X+8,INV_Y+30),(INV_X+INV_W-8,INV_Y+30),1)
    inv_rects={}
    def sort_key(f):
        return (0, f) if f in MOL and MOL[f][4] else (1, f)
    items=sorted([(f,c) for f,c in inventory.items() if c>0 and f in MOL], key=lambda x: sort_key(x[0]))
    cy=INV_Y+38
    for formula,count in items:
        if cy+CARD_H > INV_Y+INV_H-10: break
        r=pygame.Rect(INV_X+8,cy,CARD_W,CARD_H)
        inv_rects[formula]=r
        hov=r.collidepoint(mx,my) and not dragging
        draw_card(screen,formula,r.x,r.y,CARD_W,CARD_H,count=count,hover=hov)
        if hov and formula in MOL:
            name=MOL[formula][0]
            nts=FX.render(name,True,(255,255,255))
            ts=pygame.Surface((nts.get_width()+12,nts.get_height()+6),pygame.SRCALPHA)
            rrect(ts,(10,10,20,210),(0,0,ts.get_width(),ts.get_height()),6)
            ts.blit(nts,(6,3)); screen.blit(ts,(r.right+4, r.y+5))
        cy+=CARD_H+6
    if not items and not dragging:
        dtxt(screen,"Empty!",FM,TXT_D,INV_X+INV_W//2,INV_Y+INV_H//2-10)
        dtxt(screen,"Reset or clear reactor",FX,TXT_D,INV_X+INV_W//2,INV_Y+INV_H//2+12)

    # Objectives panel
    rrect(screen,PANEL,(OBJ_X,OBJ_Y,OBJ_W,OBJ_H),10)
    dtxt_l(screen,"Objectives",FMB,GREEN,OBJ_X+12,OBJ_Y+8)
    pygame.draw.line(screen,BORDER,(OBJ_X+8,OBJ_Y+30),(OBJ_X+OBJ_W-8,OBJ_Y+30),1)
    oy=OBJ_Y+38
    for formula,(needed,made) in objectives.items():
        done=made>=needed; col=GREEN if done else TXT
        cr=pygame.Rect(OBJ_X+8,oy,OBJ_W-16,68)
        rrect(screen,(20,50,30) if done else PANEL2,cr,8)
        rrect(screen,GREEN if done else BORDER,cr,8,2 if done else 1)
        if formula in MOL:
            is_at=MOL[formula][4]
            draw_mol_vis(screen,formula,OBJ_X+38,oy+22,scale=0.75 if not is_at else 1.0)
            dtxt_l(screen,formula,FMB,col,OBJ_X+60,oy+5)
            dtxt_l(screen,MOL[formula][0],FX,TXT_D if not done else (100,220,140),OBJ_X+60,oy+24)
        bar_r=pygame.Rect(OBJ_X+60,oy+44,OBJ_W-80,12)
        rrect(screen,(30,35,50),bar_r,6)
        fill_w=int(bar_r.w * min(1.0, made/max(1,needed)))
        if fill_w>0: rrect(screen,GREEN if done else ACCENT,(bar_r.x,bar_r.y,fill_w,bar_r.h),6)
        dtxt(screen,f"{made}/{needed}",FX,col,bar_r.centerx,bar_r.centery)
        if done: dtxt_l(screen,"\u2713",FL,GREEN,OBJ_X+OBJ_W-35,oy+18)
        oy+=76

    # Reactor panel
    rrect(screen,PANEL,(REA_X,REA_Y,REA_W,REA_H),10)
    dtxt(screen,"Reactor",FMB,YELLOW,REA_X+REA_W//2,REA_Y+15)
    dtxt(screen,lv['desc'],FS,TXT_D,REA_X+REA_W//2,REA_Y+40)

    # Slot grid 4x3
    scx=REA_X+REA_W//2; scy=REA_Y+145
    cols=4; rows=3; sx_gap=12; sy_gap=10
    total_w=cols*SLOT_W+(cols-1)*sx_gap; grid_x=scx-total_w//2
    new_slots=[]
    for idx in range(NUM_SLOTS):
        row,col=divmod(idx,cols)
        sx=grid_x+col*(SLOT_W+sx_gap); sy=scy-sy_gap//2+row*(SLOT_H+sy_gap)
        new_slots.append(pygame.Rect(sx,sy,SLOT_W,SLOT_H))
    slot_rects[:]=new_slots

    items_in_reactor=[r for r in reactor if r]
    if items_in_reactor:
        dtxt(screen,f"{len(items_in_reactor)}/{NUM_SLOTS} slots",FX,TXT_D,scx,scy+SLOT_H+sy_gap+6)

    for i,sr in enumerate(slot_rects):
        if reactor[i]:
            hov=sr.collidepoint(mx,my) and not dragging
            rrect(screen,PANEL2,sr,8); rrect(screen,BORDER,sr,8,1)
            formula=reactor[i]
            if formula in MOL:
                is_atom=MOL[formula][4]
                if is_atom:
                    draw_mol_vis(screen,formula,sr.centerx,sr.centery,scale=1.4)
                    dtxt(screen,formula,FSB,TXT,sr.centerx,sr.bottom-14)
                else:
                    draw_mol_vis(screen,formula,sr.centerx,sr.y+25,scale=0.9)
                    ft=FF.render(formula,True,(255,255,255))
                    screen.blit(ft,(sr.centerx-ft.get_width()//2, sr.bottom-30))
            if hov: dtxt(screen,"click to remove",FX,RED,sr.centerx,sr.bottom-2)
        else:
            hov=sr.collidepoint(mx,my) and dragging
            col=SLOT_H if hov else SLOT_E
            rrect(screen,col,sr,8); rrect(screen,BORDER,sr,8,1)
            dtxt(screen,"+",FS,TXT_D if not hov else ACCENT,sr.centerx,sr.centery)

    # Result preview
    recipe=get_recipe()
    preview_y=scy+SLOT_H+sy_gap+25
    if recipe:
        reactants,products,name,eq=recipe
        dtxt(screen,"\u2193",FL,YELLOW,scx,preview_y-5)
        px=REA_X+30
        for pf,qty in products.items():
            if pf in MOL:
                draw_card(screen,pf,px,preview_y+3,115,48,ghost=True)
                if qty>1: dtxt(screen,f"x{qty}",FSB,YELLOW,px+60,preview_y+56)
                px+=125
        r_str=" + ".join(f"{v}{k}" if v>1 else k for k,v in reactants.items())
        p_str=" + ".join(f"{v}{k}" if v>1 else k for k,v in products.items())
        dtxt(screen,f"{r_str}  \u2192  {p_str}",FS,YELLOW,scx,preview_y+68)
        dtxt(screen,name,FX,TXT_D,scx,preview_y+86)
    elif items_in_reactor:
        na=int(120+60*math.sin(t*6))
        dtxt(screen,"No matching recipe",FMB,(255,na,na),scx,preview_y+15)
        dtxt(screen,"Try adding or removing items",FX,TXT_D,scx,preview_y+35)

    # REACT button
    react_btn=pygame.Rect(scx-95,REA_Y+REA_H-95,190,48)
    can=recipe is not None; hov=react_btn.collidepoint(mx,my) and can
    if can:
        ga=int(30+20*math.sin(t*5))
        gs=pygame.Surface((200,58),pygame.SRCALPHA)
        rrect(gs,(*YELLOW,ga),(0,0,200,58),15); screen.blit(gs,(react_btn.x-5,react_btn.y-5))
        rrect(screen,(200,160,0) if hov else (170,140,0),react_btn,12)
        dtxt(screen,"REACT!",FL,(255,255,220),react_btn.centerx,react_btn.centery)
    else:
        rrect(screen,BTN_D,react_btn,12)
        dtxt(screen,"REACT!",FL,TXT_D,react_btn.centerx,react_btn.centery)

    by=REA_Y+REA_H-42
    clear_btn=pygame.Rect(scx-280,by,120,36)
    reset_btn=pygame.Rect(scx-145,by,120,36)
    hint_btn=pygame.Rect(scx+55,by,100,36)
    recipe_btn=pygame.Rect(scx+170,by,110,36)
    for btn,label,lc in [(clear_btn,"Clear",TXT),(reset_btn,"Reset (R)",TXT),(hint_btn,"Hint (H)",YELLOW),(recipe_btn,"Recipes",CYAN)]:
        hov=btn.collidepoint(mx,my)
        rrect(screen,BTN_H if hov else BTN,btn,8)
        dtxt(screen,label,FS,lc,btn.centerx,btn.centery)

    if hint_vis:
        hb=pygame.Rect(REA_X+15,REA_Y+REA_H-140,REA_W-30,40)
        s=pygame.Surface((hb.w,hb.h),pygame.SRCALPHA)
        rrect(s,(40,40,10,200),(0,0,hb.w,hb.h),8); screen.blit(s,hb.topleft)
        rrect(screen,YELLOW,hb,8,1)
        dtxt(screen,f"Hint: {lv['hint']}",FS,YELLOW,hb.centerx,hb.centery)

    if show_rec: draw_recipe_ref()

    if dragging and drag_formula and drag_formula in MOL:
        gx,gy=mx-drag_off[0],my-drag_off[1]
        draw_card(screen,drag_formula,gx,gy,CARD_W,CARD_H,ghost=True)
    for p in particles: p.draw(screen)
    if msg_timer>0:
        al=min(255,int(msg_timer*200))
        ms=FM.render(msg_text,True,msg_color)
        ms_s=pygame.Surface((ms.get_width()+30,ms.get_height()+14),pygame.SRCALPHA)
        rrect(ms_s,(10,10,20,min(200,al)),(0,0,ms_s.get_width(),ms_s.get_height()),10)
        ms_s.blit(ms,(15,7)); screen.blit(ms_s,(scx-ms_s.get_width()//2, REA_Y+REA_H-140))

def draw_recipe_ref():
    ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,180)); screen.blit(ov,(0,0))
    atom_r=[r for r in ALL_RECIPES if all(k in EC for k in r[0])]
    mol_r=[r for r in ALL_RECIPES if r not in atom_r]
    pw=1200; ph=80+max(len(atom_r),len(mol_r))*32+10
    px,py=(W-pw)//2,max(10,(H-ph)//2)
    rrect(screen,(20,22,40),(px,py,pw,ph),14); rrect(screen,CYAN,(px,py,pw,ph),14,2)
    dtxt(screen,"Recipe Reference  (TAB to close)",FL,CYAN,W//2,py+22)
    c1=px+15; c2=px+pw//2+5
    dtxt_l(screen,"Atom Assembly ("+str(len(atom_r))+")",FMB,ACCENT,c1,py+46)
    dtxt_l(screen,"Molecular Reactions ("+str(len(mol_r))+")",FMB,YELLOW,c2,py+46)
    pygame.draw.line(screen,BORDER,(c1,py+64),(c1+pw//2-20,py+64),1)
    pygame.draw.line(screen,BORDER,(c2,py+64),(c2+pw//2-20,py+64),1)
    ry=py+70
    for reactants,products,name,eq in atom_r:
        r_s=" + ".join(f"{v}{k}" if v>1 else k for k,v in reactants.items())
        p_s=" + ".join(f"{v}{k}" if v>1 else k for k,v in products.items())
        dtxt_l(screen,f"{r_s} \u2192 {p_s}",FS,TXT,c1+3,ry)
        dtxt_l(screen,name,FX,TXT_D,c1+3,ry+16)
        ry+=32
    ry=py+70
    for reactants,products,name,eq in mol_r:
        r_s=" + ".join(f"{v}{k}" if v>1 else k for k,v in reactants.items())
        p_s=" + ".join(f"{v}{k}" if v>1 else k for k,v in products.items())
        dtxt_l(screen,f"{r_s} \u2192 {p_s}",FS,TXT,c2+3,ry)
        dtxt_l(screen,name,FX,TXT_D,c2+3,ry+16)
        ry+=32

def draw_win(t):
    global next_btn,menu_btn
    mx,my=mpos
    ov=pygame.Surface((W,H),pygame.SRCALPHA); ov.fill((0,0,0,160)); screen.blit(ov,(0,0))
    bw,bh=480,300; bx,by=(W-bw)//2,(H-bh)//2
    rrect(screen,(25,30,55),(bx,by,bw,bh),16); rrect(screen,GREEN,(bx,by,bw,bh),16,3)
    for i in range(3):
        sx=bx+90+i*120; sy=by+42; r=int(18+4*math.sin(t*3+i))
        pts=[]
        for j in range(10):
            a=-math.pi/2+j*math.pi/5; rad=r if j%2==0 else r*0.4
            pts.append((sx+math.cos(a)*rad,sy+math.sin(a)*rad))
        pygame.draw.polygon(screen,YELLOW,pts); pygame.draw.polygon(screen,(255,240,150),pts,2)
    dtxt(screen,"Level Complete!",FT,GREEN,W//2,by+90)
    mins,secs=divmod(int(time_tot),60)
    dtxt(screen,f"Time: {mins:02d}:{secs:02d}",FM,TXT,W//2,by+130)
    obj_s="  |  ".join(f"{f}:{objectives[f][1]}/{objectives[f][0]}" for f in objectives)
    dtxt(screen,obj_s,FS,ACCENT,W//2,by+158)
    has_next=cur_lv+1<len(LEVELS)
    if has_next:
        next_btn=pygame.Rect(bx+40,by+210,190,48)
        hov=next_btn.collidepoint(mx,my)
        rrect(screen,BTN_H if hov else BTN,next_btn,10); rrect(screen,GREEN,next_btn,10,2)
        dtxt(screen,"Next Level",FMB,GREEN,next_btn.centerx,next_btn.centery)
    menu_btn=pygame.Rect(bx+bw-230,by+210,190,48)
    hov=menu_btn.collidepoint(mx,my)
    rrect(screen,BTN_H if hov else BTN,menu_btn,10)
    dtxt(screen,"Level Select",FMB,TXT,menu_btn.centerx,menu_btn.centery)

def main():
    while True:
        dt=clock.tick(FPS)/1000.0
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            handle_ev(ev)
        update(dt); draw()

if __name__=="__main__":
    main()