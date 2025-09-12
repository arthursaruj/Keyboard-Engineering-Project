
import pygame, json, os, math, random
import pygame.freetype as ft

pygame.init()
TITLE = "KEYBOARD INPUT TESTER"
W, H = 1400, 900
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
title_font = ft.SysFont("Segoe UI, Arial", 40, bold=True)
title_font.render_to(screen, (24, 20), TITLE, (255, 255, 255))

_grid_cache = {}

# ---------- THEMES ----------
THEMES = {
    "Midnight": {
        "BG":(12,16,24),"CARD":(20,26,38),"KEY_UP":(24,32,50),"KEY_BORDER":(52,72,110),
        "KEY_LIT":(36,52,84),"KEY_PRESSED":(30,44,72),"ACCENT":(128,168,255),
        "TEXT":(230,238,255),"MUTED":(160,176,200),"BTN":(28,36,56),"BTN_BORDER":(60,80,120)
    },
    "Carbon":   {
        "BG":(14,14,16),"CARD":(24,24,28),"KEY_UP":(20,20,24),"KEY_BORDER":(60,60,68),
        "KEY_LIT":(38,38,52),"KEY_PRESSED":(34,34,46),"ACCENT":(160,160,255),
        "TEXT":(235,235,240),"MUTED":(165,165,180),"BTN":(34,34,48),"BTN_BORDER":(72,72,90)
    },
    "Ocean":    {
        "BG":(7,18,22),"CARD":(12,32,39),"KEY_UP":(14,42,51),"KEY_BORDER":(18,68,82),
        "KEY_LIT":(20,92,110),"KEY_PRESSED":(18,82,98),"ACCENT":(140,220,255),
        "TEXT":(220,245,255),"MUTED":(150,200,215),"BTN":(18,50,60),"BTN_BORDER":(24,86,100)
    }
}
# ---------- BACKGROUNDS ----------

# ---------- SETTINGS ----------
DEFAULTS = {"unit":60, "gap":4, "layout":"Full-size", "theme":"Midnight", "fit_to_window": True}
SETTINGS_FILE = "keyboard_input_tester_settings.json"

def load_settings():
    d = DEFAULTS.copy()
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                d.update({k:data.get(k,v) for k,v in DEFAULTS.items()})
        except Exception:
            pass
    # sanitize old names
    if d.get("layout") in ("Layout_60","layout_60","Sixty"): d["layout"] = "60%"
    if d.get("theme") not in THEMES: d["theme"] = "Midnight"
    return d

def save_settings(s):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(s, f, indent=2)
    except Exception:
        pass

S = load_settings()

# ---------- FONTS ----------
FONT      = pygame.font.SysFont("segoeui,arial", 18)
FONT_SMALL= pygame.font.SysFont("segoeui,arial", 14)
FONT_BIG  = pygame.font.SysFont("segoeui,arial", 28)

def C(): return THEMES[S["theme"]]

# ---------- HELPERS ----------
def key(label, w, *codes, spacer=False):
    return {"label":label, "w":w, "codes":[c for c in codes if isinstance(c,int)], "spacer":spacer}

from pygame.locals import *

def any_key_const(names):
    for n in names:
        v = getattr(pygame, n, None)
        if isinstance(v, int): return v
    return None

K_LWIN = any_key_const(["K_LGUI","K_LSUPER","K_LMETA"])
K_RWIN = any_key_const(["K_RGUI","K_RSUPER","K_RMETA"])
K_MENU = getattr(pygame, "K_MENU", None) or getattr(pygame, "K_APPLICATION", None)

# ---------- LAYOUTS ----------
FROW = [
    key("Esc",1.2, K_ESCAPE),
    key("F1",1.0, K_F1), key("F2",1.0, K_F2), key("F3",1.0, K_F3), key("F4",1.0, K_F4),
    key("F5",1.0, K_F5), key("F6",1.0, K_F6), key("F7",1.0, K_F7), key("F8",1.0, K_F8),
    key("F9",1.0, K_F9), key("F10",1.0, K_F10), key("F11",1.0, K_F11), key("F12",1.0, K_F12),
    key("PrtSc",1.1, K_PRINTSCREEN), key("ScrLk",1.1, K_SCROLLLOCK), key("Pause",1.1, K_PAUSE),
]

MAINBLOCK = [
    [ key("`",1.0, K_BACKQUOTE), key("1",1.0,K_1), key("2",1.0,K_2), key("3",1.0,K_3), key("4",1.0,K_4),
      key("5",1.0,K_5), key("6",1.0,K_6), key("7",1.0,K_7), key("8",1.0,K_8), key("9",1.0,K_9),
      key("0",1.0,K_0), key("-",1.0,K_MINUS), key("=",1.0,K_EQUALS), key("Backspace",2.0,K_BACKSPACE) ],
    [ key("Tab",1.6,K_TAB), key("Q",1.0,K_q), key("W",1.0,K_w), key("E",1.0,K_e), key("R",1.0,K_r),
      key("T",1.0,K_t), key("Y",1.0,K_y), key("U",1.0,K_u), key("I",1.0,K_i), key("O",1.0,K_o),
      key("P",1.0,K_p), key("[",1.0,K_LEFTBRACKET), key("]",1.0,K_RIGHTBRACKET), key("\\",1.4,K_BACKSLASH) ],
    [ key("Caps",1.9,K_CAPSLOCK), key("A",1.0,K_a), key("S",1.0,K_s), key("D",1.0,K_d), key("F",1.0,K_f),
      key("G",1.0,K_g), key("H",1.0,K_h), key("J",1.0,K_j), key("K",1.0,K_k), key("L",1.0,K_l),
      key(";",1.0,K_SEMICOLON), key("'",1.0,K_QUOTE), key("Enter",2.2,K_RETURN) ],
    [ key("Shift",2.4,K_LSHIFT), key("Z",1.0,K_z), key("X",1.0,K_x), key("C",1.0,K_c), key("V",1.0,K_v),
      key("B",1.0,K_b), key("N",1.0,K_n), key("M",1.0,K_m), key(",",1.0,K_COMMA), key(".",1.0,K_PERIOD),
      key("/",1.0,K_SLASH), key("RShift",2.8,K_RSHIFT) ],
    [ key("LCtrl",1.2,K_LCTRL), key("LWin",1.2,K_LWIN), key("LAlt",1.2,K_LALT),
      key("Space",7.1,K_SPACE), key("RAlt",1.2,K_RALT), key("RWin",1.2,K_RWIN), key("Menu",1.2,K_MENU), key("RCtrl",1.2,K_RCTRL) ],
]

ARROWS = [
    [ key("",1.0, spacer=True), key("",1.0,spacer=True), key("",1.0, spacer=True) ],
    [ key("",1.0, spacer=True), key("↑",1.0,K_UP), key("",1.0, spacer=True) ],
    [ key("←",1.0,K_LEFT), key("↓",1.0,K_DOWN), key("→",1.0,K_RIGHT) ]
]

NAVBLOCK = [
    [ key("Ins",1.1,K_INSERT), key("Home",1.1,K_HOME), key("PgUp",1.1,K_PAGEUP) ],
    [ key("Del",1.1,K_DELETE), key("End",1.1,K_END), key("PgDn",1.1,K_PAGEDOWN) ],
] + ARROWS

NUMPAD = [
    [ key("Num",1.1,K_NUMLOCK), key("/",1.1,K_KP_DIVIDE), key("*",1.1,K_KP_MULTIPLY), key("-",1.1,K_KP_MINUS) ],
    [ key("7",1.1,K_KP7), key("8",1.1,K_KP8), key("9",1.1,K_KP9), key("+",1.1,K_KP_PLUS) ],
    [ key("4",1.1,K_KP4), key("5",1.1,K_KP5), key("6",1.1,K_KP6), key("+",1.1) ],
    [ key("1",1.1,K_KP1), key("2",1.1,K_KP2), key("3",1.1,K_KP3), key("Enter",1.1,K_KP_ENTER) ],
    [ key("0",2.3,K_KP0), key(".",1.1,K_KP_PERIOD), key("Enter",1.1) ],
]

LAYOUT_60 = [
    MAINBLOCK[0],
    MAINBLOCK[1],
    MAINBLOCK[2],
    MAINBLOCK[3],
    [ key("LCtrl",1.2,K_LCTRL), key("LWin",1.2,K_LWIN), key("LAlt",1.2,K_LALT),
      key("Space",8.0,K_SPACE),
      key("Alt",1.2,K_RALT), key("Win",1.2,K_RWIN), key("Fn",1.2), key("Ctrl",1.2,K_RCTRL) ]
]

LAYOUTS = {
    "Full-size": {
        "columns": [
            {"rows":[FROW]},
            {"rows": MAINBLOCK, "offset_y": 160},
            {"rows": NAVBLOCK,  "offset_y": 160, "gap_x": 16},
            {"rows": NUMPAD,    "offset_y": 160, "gap_x": 16},
        ]
    },
    "TKL": {
        "columns": [
            {"rows":[FROW]},
            {"rows": MAINBLOCK, "offset_y": 160},
            {"rows": NAVBLOCK,  "offset_y": 160, "gap_x": 16},
        ]
    },
    "75%": {
        "columns": [
            {"rows":[FROW]},
            {"rows": MAINBLOCK, "offset_y": 160},
        ]
    },
    "60%": {
        "columns": [
            {"rows":[FROW]},
            {"rows": LAYOUT_60, "offset_y": 160},
        ]
    }
}

# ---------- GEOMETRY / FIT ----------
row_h = 64
key_rects = []
code_to_rects = {}

def measure_and_build(unit_px, gap_px, start_pos=None):
    # Build geometry relative to (0,0), or offset by start_pos if provided.
    global row_h
    row_h = max(40, int(unit_px*1.05))
    rects = []
    code_map = {}
    columns = LAYOUTS[S["layout"]]["columns"]

    # FROW (if present)
    x = 0; y = 0
    if columns and columns[0]["rows"] and columns[0]["rows"][0] == FROW:
        for item in FROW:
            w = int(item["w"] * unit_px)
            rect = pygame.Rect(x, y, w, row_h)
            rects.append({"rect":rect,"label":item["label"],"codes":item["codes"],"spacer":item.get("spacer",False)})
            for c in item["codes"]: code_map.setdefault(c,[]).append(len(rects)-1)
            x += w + gap_px
        columns_iter = columns[1:]
        frow_w = x - gap_px if FROW else 0
        frow_h = row_h
    else:
        columns_iter = columns
        frow_w = 0; frow_h = 0

    # Other columns
    cur_x = 0
    max_x = frow_w
    max_y = frow_h
    for col in columns_iter:
        y = col.get("offset_y", 0)
        x = cur_x
        for row in col["rows"]:
            rx = x
            for item in row:
                w = int(item["w"] * unit_px)
                rect = pygame.Rect(rx, y, w, row_h)
                rects.append({"rect":rect,"label":item["label"],"codes":item["codes"],"spacer":item.get("spacer",False)})
                for c in item["codes"]:
                    code_map.setdefault(c,[]).append(len(rects)-1)
                rx += w + gap_px
            y += row_h + gap_px
        # column width = widest row
        col_w = max(sum(int(it["w"] * unit_px) for it in r) + (len(r)-1)*gap_px for r in col["rows"])
        cur_x += col_w + col.get("gap_x", 32)
        max_x = max(max_x, cur_x)
        # column bottom
        col_rows = len(col["rows"])
        col_h = col.get("offset_y", 0) + col_rows*row_h + (col_rows-1)*gap_px
        max_y = max(max_y, col_h)

    # Apply start offset
    if start_pos:
        ox, oy = start_pos
        for r in rects:
            r["rect"].x += ox
            r["rect"].y += oy

    return rects, max_x, max_y, code_map

def fit_unit_to_window(requested_unit):
    # Keyboard container
    left, top, right, bottom = 24, 180, W-24, H-24
    allowed_w = right - left
    allowed_h = bottom - top
    # Measure at requested unit
    rects, bw, bh, _ = measure_and_build(requested_unit, S["gap"])
    # Padding
    pad_w = 40; pad_h = 40
    need_w = bw + pad_w
    need_h = bh + pad_h
    scale = 1.0
    if need_w > allowed_w: scale = min(scale, allowed_w/need_w)
    if need_h > allowed_h: scale = min(scale, allowed_h/need_h)
    unit_eff = max(36, int(requested_unit * scale))
    return unit_eff, (left, top, allowed_w, allowed_h)

# ---------- DRAW ----------
def draw_card(rect, title=None):
    pygame.draw.rect(screen, C()["CARD"], rect, border_radius=14)
    pygame.draw.rect(screen, C()["KEY_BORDER"], rect, width=1, border_radius=14)
    if title:
        screen.blit(FONT.render(title, True, C()["TEXT"]), (rect.x+12, rect.y+10))

def draw_button(rect, label):
    pygame.draw.rect(screen, C()["BTN"], rect, border_radius=8)
    pygame.draw.rect(screen, C()["BTN_BORDER"], rect, width=1, border_radius=8)
    t = FONT.render(label, True, C()["TEXT"])
    screen.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))



def draw_settings_bar():
    rect = pygame.Rect(24, 84, W-48, 80)
    draw_card(rect, title="")
    labels = [
        ("Layout", S["layout"]),
        ("Size", f"{S['unit']} px"),
        ("Theme", S["theme"]),
    ]
    x = rect.x + 16
    for lbl, val in labels:
        screen.blit(FONT_SMALL.render(lbl, True, C()["MUTED"]), (x, rect.y+18))
        screen.blit(FONT.render(val, True, C()["TEXT"]), (x, rect.y+40))
        x += 260

    global BTN_LAYOUT_L, BTN_LAYOUT_R, BTN_SIZE_MINUS, BTN_SIZE_PLUS, BTN_THEME_L, BTN_THEME_R, BTN_FIT, BTN_RESET
    bx = rect.right - 560
    by = rect.y + 18
    BTN_LAYOUT_L = pygame.Rect(bx, by, 36, 28); bx += 40
    BTN_LAYOUT_R = pygame.Rect(bx, by, 36, 28); bx += 60
    BTN_SIZE_MINUS= pygame.Rect(bx, by, 36, 28); bx += 40
    BTN_SIZE_PLUS = pygame.Rect(bx, by, 36, 28); bx += 60
    BTN_THEME_L   = pygame.Rect(bx, by, 36, 28); bx += 40
    BTN_THEME_R   = pygame.Rect(bx, by, 36, 28); bx += 60
    BTN_FIT       = pygame.Rect(bx, by-4, 100, 36); bx += 120
    BTN_RESET     = pygame.Rect(bx, by-8, 130, 36)

    draw_button(BTN_LAYOUT_L, "<"); draw_button(BTN_LAYOUT_R, ">")
    label = FONT_SMALL.render("LAYOUTS", True, C()["MUTED"])
    lx = (BTN_LAYOUT_L.centerx + BTN_LAYOUT_R.centerx) // 2 - label.get_width() // 2
    ly = max(BTN_LAYOUT_L.bottom, BTN_LAYOUT_R.bottom) + 6
    screen.blit(label, (lx, ly))
    draw_button(BTN_SIZE_MINUS, "-"); draw_button(BTN_SIZE_PLUS, "+")
    draw_button(BTN_THEME_L, "<"); draw_button(BTN_THEME_R, ">")
    draw_button(BTN_FIT, "Fit: " + ("ON" if S["fit_to_window"] else "OFF"))
    draw_button(BTN_RESET, "Reset")

def draw_keycap(rect, lit, pressed):
    shadow = rect.move(0, 3)
    pygame.draw.rect(screen, (0,0,0,60), shadow, border_radius=12)
    color = C()["KEY_PRESSED"] if pressed else (C()["KEY_LIT"] if lit else C()["KEY_UP"])
    border= C()["ACCENT"] if (lit or pressed) else C()["KEY_BORDER"]
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, border, rect, width=2, border_radius=12)


def draw_keyboard_container(rect):
    draw_card(rect, title="Keyboard")
    inner = rect.inflate(-20, -20)
    pygame.draw.rect(screen, (0,0,0,24), inner, border_radius=12)

def render_keyboard(unit_eff, container_rect):
    rects_raw, bw, bh, cmap = measure_and_build(unit_eff, S["gap"])
    inner = container_rect.inflate(-40, -40)
    start_x = inner.x + (inner.w - bw)//2
    start_y = inner.y + (inner.h - bh)//2
    rects, _, _, cmap = measure_and_build(unit_eff, S["gap"], start_pos=(start_x, start_y))
    return rects, cmap

# ---------- STATE ----------
lit_codes = set()
held_codes = set()

# ---------- CONTROLS ----------
def cycle_layout(delta):
    names = list(LAYOUTS.keys())
    i = names.index(S["layout"]) if S["layout"] in names else 0
    S["layout"] = names[(i+delta) % len(names)]
    save_settings(S)

def cycle_theme(delta):
    names = list(THEMES.keys())
    i = names.index(S["theme"]) if S["theme"] in names else 0
    S["theme"] = names[(i+delta) % len(names)]
    save_settings(S)

def nudge_size(delta):
    S["unit"] = max(36, min(100, S["unit"] + delta))
    save_settings(S)

# ---------- MAIN LOOP ----------
running = True
BTN_LAYOUT_L=BTN_LAYOUT_R=BTN_SIZE_MINUS=BTN_SIZE_PLUS=BTN_THEME_L=BTN_THEME_R=BTN_FIT=BTN_RESET=pygame.Rect(0,0,0,0)

while running:
    dt = clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            held_codes.add(event.key); lit_codes.add(event.key)
        elif event.type == pygame.KEYUP:
            held_codes.discard(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if BTN_LAYOUT_L.collidepoint(event.pos): cycle_layout(-1)
            elif BTN_LAYOUT_R.collidepoint(event.pos): cycle_layout(+1)
            elif BTN_SIZE_MINUS.collidepoint(event.pos): nudge_size(-2)
            elif BTN_SIZE_PLUS.collidepoint(event.pos): nudge_size(+2)
            elif BTN_THEME_L.collidepoint(event.pos): cycle_theme(-1)
            elif BTN_THEME_R.collidepoint(event.pos): cycle_theme(+1)
            elif BTN_FIT.collidepoint(event.pos): S["fit_to_window"] = not S["fit_to_window"]; save_settings(S)
            elif BTN_RESET.collidepoint(event.pos): lit_codes.clear(); held_codes.clear()

    draw_settings_bar()

    unit_eff = S["unit"]
    kb_container = pygame.Rect(24, 180, W-48, H-204)
    if S["fit_to_window"]:
        unit_eff, _ = fit_unit_to_window(S["unit"])
    draw_keyboard_container(kb_container)

    key_rects, code_to_rects = render_keyboard(unit_eff, kb_container)

    for k in key_rects:
        if k["spacer"]: continue
        r = k["rect"]
        lit = any((code in lit_codes) for code in k["codes"]) if k["codes"] else False
        pressed = any((code in held_codes) for code in k["codes"]) if k["codes"] else False
        r_draw = r.move(0, 1 if pressed else 0)
        draw_keycap(r_draw, lit, pressed)
        t = FONT.render(k["label"], True, C()["TEXT"])
        screen.blit(t, (r_draw.centerx - t.get_width()//2, r_draw.centery - t.get_height()//2))

    pygame.display.flip()

pygame.quit()
