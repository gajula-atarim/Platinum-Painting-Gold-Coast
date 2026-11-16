#!/usr/bin/env python3
"""Generate Elementor JSON for the Platinum Painting homepage, UAE header and footer.

Output: build/out/home.json, header.json, footer.json
Everything visible (text, images, buttons, links, icons) is a native Elementor widget.
Layout/animation helpers are referenced by CSS class (see build/theme/assets/pp.css + pp.js).
"""
import json, os, hashlib, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
FR = json.load(open(os.path.join(HERE, 'fragments.json')))
UP = 'https://platinum-painting-gold-coast.wsdfy.com/wp-content/uploads/2026/11/'

MEDIA = {
    'logo': (6, 'pp-logo.webp'), 'logo_white': (7, 'pp-logo-white.webp'), 'cans': (8, 'pp-paint-cans-splash.webp'),
    'brush_blue': (9, 'pp-brush-blue.webp'), 'brush_purple': (10, 'pp-brush-purple.webp'), 'brush_red': (11, 'pp-brush-red.webp'),
    'brush_teal': (12, 'pp-brush-teal.webp'), 'brush_yellow': (13, 'pp-brush-yellow.webp'), 'stroke': (14, 'pp-paint-stroke-white.webp'),
    'hero_bg': (15, 'pp-hero-house.webp'), 'ba': (16, 'pp-before-after-house.webp'), 'q1': (17, 'pp-hero-painter-exterior.jpg'),
    'roller': (18, 'pp-roller-tape-detail.jpg'), 'q4': (19, 'pp-interior-repaint.jpg'), 'about1': (20, 'pp-painter-at-work.jpg'),
    'g1': (21, 'pp-gallery-burleigh-heads.jpg'), 'g2': (22, 'pp-gallery-southport.jpg'), 'g3': (23, 'pp-gallery-robina.jpg'),
    'g4': (24, 'pp-gallery-palm-beach.jpg'), 'g5': (25, 'pp-gallery-broadbeach.jpg'), 'g6': (26, 'pp-gallery-hope-island.jpg'),
    'i_interior': (29, 'pp-icon-interior.webp'), 'i_exterior': (30, 'pp-icon-exterior.webp'), 'i_commercial': (31, 'pp-icon-commercial.webp'),
    'i_strata': (32, 'pp-icon-strata.webp'), 'i_roof': (33, 'pp-icon-roof.webp'), 'i_render': (34, 'pp-icon-render.webp'),
    'i_prep': (35, 'pp-icon-prep.webp'), 'i_coast': (36, 'pp-icon-coast.webp'),
}

NAVY, BLUE, INK, TEXT, MIST, GREY, BG, LINE = '#0B2B55', '#1359AC', '#0E0E10', '#3A3D42', '#E3ECF7', '#C8CDD3', '#F3F5F8', '#E3E7EC'
CINZEL, FIG, CORM = 'Cinzel', 'Figtree', 'Cormorant Garamond'
PHONE, PHONE_TEL, EMAIL = '0400 000 000', 'tel:0400000000', 'hello@platinumpainting.com.au'

_ctr = itertools.count(1)
def uid(seed=''):
    return hashlib.md5(f'{seed}{next(_ctr)}'.encode()).hexdigest()[:7]

def media(key):
    i, f = MEDIA[key]
    return {'url': UP + f, 'id': i, 'size': '', 'source': 'library'}

def px(v, unit='px'): return {'unit': unit, 'size': v, 'sizes': []}
def dims(t, r=None, b=None, l=None, unit='px'):
    r = t if r is None else r; b = t if b is None else b; l = r if l is None else l
    return {'unit': unit, 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': len({t, r, b, l}) == 1}
def gap(c, r=None):
    r = c if r is None else r
    return {'column': str(c), 'row': str(r), 'isLinked': c == r, 'unit': 'px', 'size': c}
def shadow(h, v, blur, spread, color):
    return {'horizontal': h, 'vertical': v, 'blur': blur, 'spread': spread, 'color': color}

def typo(prefix='typography', family=None, size=None, weight=None, lh=None, ls=None, transform=None, style=None,
         size_t=None, size_m=None, lh_unit='em', ls_unit='em'):
    s = {f'{prefix}_typography': 'custom'}
    if family: s[f'{prefix}_font_family'] = family
    if size is not None: s[f'{prefix}_font_size'] = px(size)
    if size_t is not None: s[f'{prefix}_font_size_tablet'] = px(size_t)
    if size_m is not None: s[f'{prefix}_font_size_mobile'] = px(size_m)
    if weight: s[f'{prefix}_font_weight'] = str(weight)
    if lh is not None: s[f'{prefix}_line_height'] = px(lh, lh_unit)
    if ls is not None: s[f'{prefix}_letter_spacing'] = px(ls, ls_unit)
    if transform: s[f'{prefix}_text_transform'] = transform
    if style: s[f'{prefix}_font_style'] = style
    return s

# ---------------------------------------------------------------- element builders
def con(children=(), cls='', direction='column', full=True, boxed=None, gap_=0, pad=None, pad_t=None, pad_m=None,
        bg=None, radius=None, align=None, justify=None, wrap=None, tag=None, link=None, css_id=None, width=None,
        width_t=None, width_m=None, shadow_=None, overflow=None, direction_t=None, direction_m=None, grid=None, extra=None):
    s = {'content_width': 'full' if full else 'boxed', 'flex_direction': direction}
    if boxed: s['content_width'] = 'boxed'; s['boxed_width'] = px(boxed)
    if direction_t: s['flex_direction_tablet'] = direction_t
    if direction_m: s['flex_direction_mobile'] = direction_m
    if gap_ is not None: s['flex_gap'] = gap(*gap_) if isinstance(gap_, tuple) else gap(gap_)
    s['padding'] = pad if pad is not None else dims(0)
    if pad_t is not None: s['padding_tablet'] = pad_t
    if pad_m is not None: s['padding_mobile'] = pad_m
    if bg: s['background_background'] = 'classic'; s['background_color'] = bg
    if radius is not None: s['border_radius'] = dims(radius) if not isinstance(radius, dict) else radius
    if align: s['flex_align_items'] = align
    if justify: s['flex_justify_content'] = justify
    if wrap: s['flex_wrap'] = wrap
    if tag: s['html_tag'] = tag
    if link: s['link'] = {'url': link, 'is_external': '', 'nofollow': '', 'custom_attributes': ''}
    if css_id: s['_element_id'] = css_id
    if width is not None: s['width'] = px(width, '%') if isinstance(width, (int, float)) and width <= 100 else px(width)
    if width_t is not None: s['width_tablet'] = px(width_t, '%')
    if width_m is not None: s['width_mobile'] = px(width_m, '%')
    if shadow_: s['box_shadow_box_shadow_type'] = 'yes'; s['box_shadow_box_shadow'] = shadow_
    if overflow: s['overflow'] = overflow
    if grid:
        s['container_type'] = 'grid'
        cols, rows, g = grid['cols'], grid.get('rows', 1), grid.get('gap', 20)
        s['grid_columns_grid'] = px(cols, 'fr'); s['grid_rows_grid'] = px(rows, 'fr')
        s['grid_gaps'] = {'column': str(g), 'row': str(grid.get('rgap', g)), 'isLinked': True, 'unit': 'px'}
        if 'cols_t' in grid: s['grid_columns_grid_tablet'] = px(grid['cols_t'], 'fr')
        if 'cols_m' in grid: s['grid_columns_grid_mobile'] = px(grid['cols_m'], 'fr')
        if 'rows_t' in grid: s['grid_rows_grid_tablet'] = px(grid['rows_t'], 'fr')
        if 'rows_m' in grid: s['grid_rows_grid_mobile'] = px(grid['rows_m'], 'fr')
        s['grid_auto_flow'] = 'row'
    if cls: s['css_classes'] = cls
    if extra: s.update(extra)
    return {'id': uid('c'), 'elType': 'container', 'isInner': False, 'settings': s, 'elements': list(children)}

def widget(kind, settings, cls=''):
    if cls: settings['_css_classes'] = cls
    return {'id': uid('w'), 'elType': 'widget', 'widgetType': kind, 'isInner': False, 'settings': settings, 'elements': []}

def heading(text, tag='h2', cls='', color=INK, align=None, link=None, **t):
    s = {'title': text, 'header_size': tag, 'title_color': color}
    if align: s['align'] = align
    if link: s['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    s.update(typo(**t) if t else {})
    return widget('heading', s, cls)

def eyebrow(text, color=BLUE, cls='', align=None):
    return heading(text, 'div', cls, color, align, family=FIG, size=12, weight=700, ls=0.16, transform='uppercase', lh=1.3)

def text(html, cls='', color=TEXT, align=None, **t):
    s = {'editor': html, 'text_color': color}
    if align: s['align'] = align
    s.update(typo(**t) if t else {})
    return widget('text-editor', s, cls)

def image(key, cls='', width=None, size='full', link=None, alt_lazy=True):
    s = {'image': media(key), 'image_size': size}
    if width: s['width'] = px(width)
    if link: s['link_to'] = 'custom'; s['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    return widget('image', s, cls)

def button(label, url, cls='', style='solid', size=16, pad=(16, 30), icon=None, icon_after=False, bg=BLUE, fg='#FFFFFF',
           hover_bg=NAVY, hover_fg='#FFFFFF', border=None, hover_border=None, weight=600):
    s = {'text': label, 'link': {'url': url, 'is_external': '', 'nofollow': ''}, 'size': 'md',
         'button_text_color': fg, 'hover_color': hover_fg,
         'background_background': 'classic', 'background_color': bg,
         'button_background_hover_background': 'classic', 'button_background_hover_color': hover_bg,
         'border_radius': dims(999), 'text_padding': dims(pad[0], pad[1])}
    if border:
        s.update({'border_border': 'solid', 'border_width': dims(1.5), 'border_color': border})
        if hover_border: s['button_hover_border_color'] = hover_border
    if icon:
        s['selected_icon'] = {'value': icon[0], 'library': icon[1]}
        s['icon_align'] = 'row-reverse' if icon_after else 'row'
        s['icon_indent'] = px(8)
    s.update(typo(family=FIG, size=size, weight=weight, lh=1.2))
    return widget('button', s, cls)

def html(markup, cls=''):
    return widget('html', {'html': markup}, cls)

def deco(children, cls):
    """Decorative floating element: positioned + revealed container, float animation on the child."""
    return con(children, cls=f'pp-deco {cls}')

def deco_img(key, cls, rot=None):
    c = 'pp-float pp-deco-img' + (f' pp-rot-{rot}' if rot is not None else '')
    return image(key, c)

def icon_w(value, lib, cls='', view='stacked', shape='square', bg=BLUE, fg='#FFFFFF', size=20, padding=14, radius=None):
    s = {'selected_icon': {'value': value, 'library': lib}, 'view': view, 'shape': shape,
         'primary_color': bg, 'secondary_color': fg, 'size': px(size), 'icon_padding': px(padding)}
    if radius is not None: s['border_radius'] = dims(radius)
    return widget('icon', s, cls)

# ================================================================ HOMEPAGE
SEC_PAD_X = (48, 40, 20)

def section_pad(top, bottom, t=None, m=None):
    t = t or (top, bottom); m = m or (top, bottom)
    return dict(pad=dims(top, SEC_PAD_X[0], bottom, SEC_PAD_X[0]), pad_t=dims(t[0], SEC_PAD_X[1], t[1], SEC_PAD_X[1]),
                pad_m=dims(m[0], SEC_PAD_X[2], m[1], SEC_PAD_X[2]))

# ---- hero
hero_words = heading('More Than Looks. Protection That Lasts.', 'h1', 'pp-hero-title pp-split', INK,
                     family=CINZEL, size=64, size_t=51, size_m=38, weight=600, lh=1.08)
hero_left = con([
    heading('Gold Coast Painters · Residential · Commercial · Strata', 'div', 'pp-pill pp-hero-pill pp-r-up', BLUE,
            family=FIG, size=13, weight=700, ls=0.06, lh=1.3),
    hero_words,
    text('<p>Painting is about more than looks. It is a protective coating that helps surfaces last longer in all weather conditions.</p>',
         'pp-hero-lead pp-r-up pp-d4', TEXT, family=FIG, size=18, lh=1.65, size_m=17),
    con([
        button('Get a Free Quote', '#quote', 'pp-btn-lift pp-btn-lift3'),
        button('View Our Work', '#work', 'pp-btn-ghost', bg='rgba(0,0,0,0)', fg=INK, hover_bg=INK, hover_fg='#FFFFFF',
               border=INK, hover_border=INK, pad=(14.5, 28)),
    ], 'pp-r-up pp-d5', direction='row', gap_=12, wrap='wrap'),
    heading('The Platinum Standard In Painting', 'div', 'pp-r-up pp-d6', BLUE, family=CORM, size=24, weight=500, style='italic', lh=1.3),
], 'pp-hero-copy', gap_=24, width=50, width_t=100)

hero_visual = con([
    con([
        con([image('q1', 'pp-cover')], 'pp-q pp-q1 pp-r-tl', overflow='hidden'),
        html('<div class="pp-rings" aria-hidden="true"><span class="pp-ring pp-ring-1 pp-r-ring pp-d1"></span>'
             '<span class="pp-ring pp-ring-2 pp-r-ring pp-d3"></span><span class="pp-ring pp-ring-3 pp-r-ring pp-d5"></span></div>', 'pp-q pp-q2'),
        con([image('roller', 'pp-cover')], 'pp-q pp-q3 pp-r-bl pp-d2', overflow='hidden'),
        con([image('q4', 'pp-cover')], 'pp-q pp-q4 pp-r-br pp-d3', overflow='hidden'),
    ], 'pp-quad'),
    html('<div class="pp-hero-hub pp-r-zoom pp-d6" aria-hidden="true"><span class="pp-hub-pulse" data-pulse="1"></span>'
         '<span class="pp-hub-ring"><span class="pp-hub-dot"><svg width="30" height="30" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M12 3 2 11.5h3V21h5.5v-6h3v6H19v-9.5h3z"></path></svg></span></span></div>'
         '<div class="pp-twinkles" aria-hidden="true">'
         '<svg data-twinkle="1" viewBox="0 0 40 40" width="46" height="46" style="position:absolute;left:0;top:18px"><path d="M20 2C21 14 26 19 38 20 26 21 21 26 20 38 19 26 14 21 2 20 14 19 19 14 20 2Z" fill="none" stroke="#7FA7DB" stroke-width="2" stroke-linejoin="round"></path></svg>'
         '<svg data-twinkle="2" viewBox="0 0 40 40" width="34" height="34" style="position:absolute;left:40px;top:0"><path d="M20 2C21 14 26 19 38 20 26 21 21 26 20 38 19 26 14 21 2 20 14 19 19 14 20 2Z" fill="none" stroke="#7FA7DB" stroke-width="2" stroke-linejoin="round"></path></svg>'
         '<svg data-twinkle="3" viewBox="0 0 40 40" width="30" height="30" style="position:absolute;left:44px;top:50px"><path d="M20 2C21 14 26 19 38 20 26 21 21 26 20 38 19 26 14 21 2 20 14 19 19 14 20 2Z" fill="none" stroke="#7FA7DB" stroke-width="2" stroke-linejoin="round"></path></svg></div>'
         '<svg class="pp-scribble" viewBox="0 0 80 30" width="70" height="26" aria-hidden="true"><path data-draw="1" d="M4 22C14 6 22 6 22 16S34 26 40 12 56 4 58 16 70 22 76 10" fill="none" stroke="#0E0E10" stroke-width="3" stroke-linecap="round"></path></svg>',
         'pp-hero-deco'),
    con([image('cans', 'pp-float pp-hero-cans-img')], 'pp-hero-cans pp-r-right pp-d6'),
    con([con([
        heading('Free on-site quotes', 'div', '', BLUE, family=FIG, size=12, weight=700, ls=0.08, transform='uppercase', lh=1.3),
        heading('Written &amp; itemised', 'div', '', INK, family=FIG, size=15, weight=600, lh=1.4),
    ], 'pp-hero-card pp-r-up pp-d7', gap_=2, bg='#FFFFFF', radius=18, pad=dims(14, 18),
        shadow_=shadow(0, 16, 40, 0, 'rgba(11,43,85,0.18)'))], 'pp-hero-card-wrap pp-float'),
], 'pp-hero-visual', width=50, width_t=100)

hero = con([
    con([], 'pp-hero-bg pp-parallax-bg', extra={'background_background': 'classic', 'background_image': media('hero_bg'),
                                               'background_position': 'center center', 'background_size': 'cover'}),
    con([hero_left, hero_visual], 'pp-hero-inner', direction='row', direction_t='column', boxed=1280, full=False,
        gap_=56, align='center', pad=dims(176, 48, 112, 48), pad_t=dims(155, 40, 82, 40), pad_m=dims(144, 20, 64, 20)),
], 'pp-hero', bg=MIST, overflow='hidden')

# ---- offers
def offer(label, title, btn, badge_top, badge_bottom, variant, d):
    blue = variant == 'blue'
    fg = '#FFFFFF' if blue else NAVY
    if blue:
        b = button(btn, '#quote', 'pp-offer-btn', bg='#FFFFFF', fg=NAVY, hover_bg=NAVY, hover_fg='#FFFFFF', size=15, pad=(14.5, 25))
    else:
        b = button(btn, '#quote', 'pp-offer-btn', bg='rgba(0,0,0,0)', fg=NAVY, hover_bg=NAVY, hover_fg='#FFFFFF',
                   border=NAVY, hover_border=NAVY, size=15, pad=(13, 24))
    badge_fg = NAVY if blue else '#FFFFFF'
    return con([
        heading(label, 'div', '', fg, family=FIG, size=15, weight=500, lh=1.4),
        heading(title, 'div', 'pp-offer-title', fg, family=CINZEL, size=21, weight=600, lh=1.3),
        con([
            b,
            con([
                heading(badge_top, 'div', '', badge_fg, align='center', family=FIG, size=20, weight=700, lh=1.05),
                heading(badge_bottom, 'div', '', badge_fg, align='center', family=FIG, size=15, weight=700, lh=1.05),
            ], f'pp-badge pp-badge--{"light" if blue else "dark"}', justify='center', align='center'),
        ], 'pp-offer-foot', direction='row', justify='space-between', align='flex-end', gap_=16),
    ], f'pp-offer pp-offer--{variant} pp-lift pp-r-up pp-d{d}', gap_=14, bg=BLUE if blue else '#FFFFFF', radius=18,
        pad=dims(30, 28, 28, 28), shadow_=shadow(0, 10, 30, 0, 'rgba(11,43,85,0.08)'), overflow='hidden')

offers = con([
    offer('Free Quote', 'Your Property. Our Expertise. A Finish Built to Last.', 'Book Now', 'Free', 'Quote', 'white', 0),
    offer('Limited Offer', 'Roof Restorations Before Storm Season', 'Claim Offer', '10%', 'Off', 'blue', 1),
    offer('Special Offer', 'Free Colour Consultation With Every Full Repaint', 'Book Now', 'Free', 'Consult', 'white', 2),
], 'pp-offers', bg=BG, boxed=1280, full=False, grid={'cols': 3, 'cols_t': 1, 'cols_m': 1, 'gap': 24},
    **section_pad(80, 80, (61, 61), (48, 48)))

# ---- marquee
marquee_items = ['Interior Painting', 'Exterior Painting', 'Commercial', 'Strata / Body Corp', 'Roof Restorations', 'Render Coatings']
marquee = con([
    widget('icon-list', {
        'view': 'inline',
        'icon_list': [{'_id': uid('li'), 'text': t, 'selected_icon': {'value': '', 'library': ''}} for t in marquee_items],
        'text_color': '#FFFFFF',
        **typo('icon_typography', family=CINZEL, size=24, weight=600, lh=1.2),
    }, 'pp-marquee-list'),
], 'pp-marquee', overflow='hidden')

# ---- about
acc_item = lambda icon, title, body, open_, d: con([
    image(icon, 'pp-acc-icon'),
    con([
        heading(title, 'h3', 'pp-acc-title', NAVY, family=CINZEL, size=19, weight=600, lh=1.3),
        text(f'<p>{body}</p>', 'pp-acc-body', TEXT, family=FIG, size=15, lh=1.6),
    ], 'pp-acc-text'),
], f'pp-acc-item{" is-open" if open_ else ""} pp-r-up pp-d{d}', direction='row', gap_=18, align='flex-start')

about = con([
    deco([con([html('<div class="pp-stroke-brush" aria-hidden="true"><svg viewBox="0 0 200 44" width="160" height="35" style="display:block;overflow:visible"><path d="M6 26C50 10 130 6 196 12l-6 18C130 26 60 30 10 40z" fill="#F4A261"></path><g stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="0.45"><path d="M30 28C80 18 130 15 170 17M40 34C90 26 130 23 165 24"></path></g></svg></div>', 'pp-deco-stroke'),
          image('brush_red', 'pp-deco-stroke-brush pp-rot-40')], 'pp-float pp-stroke-box')], 'pp-deco-about pp-r-zoom'),
    con([
        con([
            image('stroke', 'pp-ab-stroke pp-r-left'),
            con([image('about1', 'pp-cover pp-par-up')], 'pp-ab-img pp-ab-img1 pp-r-left', overflow='hidden'),
            con([image('roller', 'pp-cover pp-par-down')], 'pp-ab-img pp-ab-img2 pp-r-up pp-d2', overflow='hidden'),
            con([con([
                heading('Coastal-rated', 'div', '', '#FFFFFF', family=CINZEL, size=20, weight=600, lh=1.3),
                text('<p>Coating systems chosen for sun, salt and storms</p>', '', GREY, family=FIG, size=13, lh=1.4),
            ], 'pp-ab-card pp-r-zoom pp-d3', gap_=4, bg=INK, radius=20, pad=dims(18, 22))], 'pp-ab-card-wrap pp-float'),
            html('<div class="pp-fan pp-r-zoom pp-d4" aria-hidden="true">' + FR['fan'] + '</div>', 'pp-ab-fan'),
        ], 'pp-about-visual', width=50, width_t=100),
        con([
            eyebrow('About Us', cls='pp-r-up'),
            heading("We Don't Just Paint. We Protect What You've Built.", 'h2', 'pp-r-up pp-d1', INK,
                    family=CINZEL, size=44, size_t=35, size_m=28, weight=600, lh=1.12),
            text('<p>Platinum Painting is a Gold Coast team painting homes, businesses and strata buildings. Every job starts with what the surface needs to last, then how it should look.</p>',
                 'pp-r-up pp-d2', TEXT, family=FIG, size=17, lh=1.65),
            con([
                acc_item('i_prep', 'Prepared Properly', 'Cleaning, repairs, sanding and priming before any topcoat goes on. Good prep is what makes a coating last.', False, 3),
                acc_item('i_coast', 'Built for the Coast', 'Products and systems chosen for Gold Coast UV, salt air and summer rain, so your finish keeps protecting for years.', True, 4),
            ], 'pp-acc'),
            button('More About Us', '#', 'pp-btn-lift pp-btn-lift3 pp-r-up pp-d5', pad=(15, 28)),
        ], 'pp-about-copy', gap_=22, width=50, width_t=100),
    ], 'pp-about-inner', direction='row', direction_t='column', boxed=1280, full=False, gap_=64, align='center',
        pad=dims(128, 48), pad_t=dims(92, 40), pad_m=dims(80, 20)),
], 'pp-about', bg=BG, overflow='hidden')

# ---- before / after
before_after = con([
    con([
        deco([image('cans', 'pp-float pp-deco-img')], 'pp-deco-ba pp-r-zoom'),
        con([
            con([
                heading('Before &amp; After', 'div', 'pp-pill pp-pill--white pp-r-up', NAVY, family=FIG, size=13, weight=600, lh=1.3),
                heading('From Weathered to Protected', 'h2', 'pp-r-up pp-d1', '#FFFFFF', family=CINZEL, size=48, size_t=39, size_m=30, weight=600, lh=1.12),
            ], '', gap_=16),
            text('<p>Sun, salt and rain wear an exterior down year after year. A full repaint with the right preparation and coating system restores the colour and seals the surface again. Drag the handle to see the difference.</p>',
                 'pp-ba-lead pp-r-up pp-d2', MIST, family=FIG, size=16, lh=1.65),
        ], 'pp-ba-head', grid={'cols': 2, 'cols_t': 1, 'cols_m': 1, 'gap': 56, 'rgap': 24}),
        con([
            image('ba', 'pp-ba-after pp-cover'),
            image('ba', 'pp-ba-before pp-cover'),
            heading('Before', 'div', 'pp-ba-tag pp-ba-tag--before', '#FFFFFF', family=FIG, size=12, weight=700, ls=0.12, transform='uppercase'),
            heading('After', 'div', 'pp-ba-tag pp-ba-tag--after', '#FFFFFF', family=FIG, size=12, weight=700, ls=0.12, transform='uppercase'),
        ], 'pp-ba pp-r-up pp-d2', overflow='hidden'),
    ], 'pp-ba-panel', boxed=1360, full=False, gap_=40, bg='#0B3A75', radius=36, overflow='hidden',
        pad=dims(80, 64), pad_t=dims(61, 41), pad_m=dims(48, 20)),
], 'pp-ba-section', bg='#FFFFFF', pad=dims(80, 24, 0, 24), pad_t=dims(61, 20, 0, 20), pad_m=dims(48, 12, 0, 12))

# ---- services
SVC = [('i_interior', 'Interior House Painting', 'Washable, low-odour finishes that resist scuffs, moisture and everyday wear.'),
       ('i_exterior', 'Exterior House Painting', 'Coatings rated for UV, salt air and summer storms.'),
       ('i_commercial', 'Commercial Painting', 'Durable, specified finishes scheduled around your trading hours.'),
       ('i_strata', 'Strata / Body Corp Painting', 'Planned repaint programs that protect shared buildings.'),
       ('i_roof', 'Roof Restorations', 'Cleaning, repairs and membrane coatings that seal out water.'),
       ('i_render', 'Render Coatings', 'Flexible systems that bridge hairline cracks and stay weathertight.')]
services = con([
    deco([image('cans', 'pp-float pp-deco-img')], 'pp-deco-svc-cans pp-r-zoom'),
    deco([con([image('brush_yellow', 'pp-deco-img pp-tilt-l'), image('brush_purple', 'pp-deco-img pp-tilt-r')], 'pp-float pp-brush-pair', direction='row', gap_=10, align='flex-end')],
         'pp-deco-svc-brushes pp-r-zoom pp-d1'),
    con([
        con([
            heading('Our Services', 'div', 'pp-pill pp-pill--white pp-pill--lg pp-r-up', NAVY, family=FIG, size=14, weight=600, lh=1.3),
            heading('Painting Services That Protect and Impress', 'h2', 'pp-svc-title pp-r-up pp-d1', NAVY, 'center',
                    family=CINZEL, size=48, size_t=39, size_m=30, weight=600, lh=1.15),
        ], '', gap_=18, align='center'),
        con([con([
            image(ic, 'pp-svc-icon'),
            heading(t, 'h3', '', NAVY, 'center', family=CINZEL, size=22, weight=600, lh=1.25),
            text(f'<p>{d}</p>', 'pp-svc-text', TEXT, 'center', family=FIG, size=15, lh=1.55),
            button('Learn More', '#', 'pp-svc-link', bg='rgba(0,0,0,0)', fg=BLUE, hover_bg='rgba(0,0,0,0)', hover_fg=NAVY, size=15, pad=(0, 0),
                   icon=('fas fa-arrow-right', 'fa-solid'), icon_after=True, weight=700),
        ], f'pp-svc pp-r-up pp-d{i % 3}', gap_=16, align='center', radius=24, pad=dims(44, 32, 38, 32)) for i, (ic, t, d) in enumerate(SVC)],
            'pp-svc-grid', grid={'cols': 3, 'cols_t': 2, 'cols_m': 1, 'gap': 16}),
        text('<p>We also restore timber decks and pergolas and offer colour consultations.</p>', '', TEXT, 'center', family=FIG, size=15, lh=1.6),
    ], 'pp-svc-inner', boxed=1280, full=False, gap_=56, pad=dims(120, 48), pad_t=dims(92, 40), pad_m=dims(80, 20)),
], 'pp-services', bg=BG, overflow='hidden')

# ---- why it matters (word fill + threats)
def threat(scene, num, title, body, d):
    return con([
        html('<div class="pp-scene pp-scene--' + scene + '" aria-hidden="true">' + FR['scenes'][scene] + '</div>', 'pp-scene-w'),
        con([
            con([
                heading(num, 'div', 'pp-num', '#FFFFFF', 'center', family=CINZEL, size=15, weight=700, lh=1),
                heading(title, 'h3', '', INK, family=CINZEL, size=24, weight=600, lh=1.2),
            ], '', direction='row', gap_=12, align='center'),
            text(f'<p>{body}</p>', '', TEXT, family=FIG, size=15, lh=1.6),
        ], '', gap_=10, pad=dims(4, 18, 0, 18)),
    ], f'pp-threat pp-lift pp-r-up pp-d{d}', gap_=16, bg='#FFFFFF', radius=28, pad=dims(12, 12, 30, 12),
        shadow_=shadow(0, 10, 30, 0, 'rgba(11,43,85,0.06)'))

why = con([
    deco([image('brush_blue', 'pp-float pp-deco-img pp-rot-m24')], 'pp-deco-why-brush pp-r-zoom'),
    deco([image('cans', 'pp-float pp-deco-img')], 'pp-deco-why-cans pp-r-zoom pp-d1'),
    con([
        eyebrow('Why It Matters', align='center'),
        text('<p>Painting is about more than looks. It is a protective coating that helps surfaces last longer in all weather conditions.</p>',
             'pp-wordfill', GREY, 'center', family=CINZEL, size=52, size_t=41, size_m=28, weight=600, lh=1.2),
    ], 'pp-why-head', boxed=1100, full=False, gap_=28, align='center', pad=dims(160, 48, 80, 48), pad_t=dims(113, 40, 61, 40), pad_m=dims(96, 20, 56, 20)),
    con([
        threat('sun', 'I', 'Sun', 'Strong Queensland UV breaks down unprotected surfaces, causing chalking, fading and cracking. We use UV-stable coatings that hold their colour.', 0),
        threat('salt', 'II', 'Salt Air', 'Coastal salt speeds up corrosion on metal and wears down finishes. The right primers and topcoats slow it right down.', 1),
        threat('storm', 'III', 'Storms', 'Heavy summer rain finds every gap. Sealed timber, render and roofing keep water out and stop rot and mould before they start.', 2),
    ], 'pp-threats', boxed=1280, full=False, grid={'cols': 3, 'cols_t': 1, 'cols_m': 1, 'gap': 22},
        pad=dims(0, 48, 128, 48), pad_t=dims(0, 40, 92, 40), pad_m=dims(0, 20, 80, 20)),
], 'pp-why', bg='#FFFFFF', overflow='hidden')

# ---- gallery
GAL = [('g1', 'Exterior Repaint', 'Burleigh Heads'), ('g2', 'Interior', 'Southport'), ('g3', 'Roof Restoration', 'Robina'),
       ('g4', 'Render Coating', 'Palm Beach'), ('g5', 'Strata Repaint', 'Broadbeach'), ('g6', 'Deck Restoration', 'Hope Island')]
gallery = con([
    deco([con([html('<div class="pp-stroke-brush" aria-hidden="true"><svg viewBox="0 0 200 44" width="190" height="42" style="display:block;overflow:visible"><path d="M6 26C50 10 130 6 196 12l-6 18C130 26 60 30 10 40z" fill="#4CC3D9"></path><g stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="0.45"><path d="M30 28C80 18 130 15 170 17M40 34C90 26 130 23 165 24"></path></g></svg></div>', 'pp-deco-stroke'),
          image('brush_yellow', 'pp-deco-stroke-brush pp-rot-40')], 'pp-float pp-stroke-box pp-stroke-box--gal')], 'pp-deco-gal pp-r-zoom'),
    con([
        con([
            con([eyebrow('Recent Projects', cls='pp-r-up'),
                 heading('Our Work Across the Coast', 'h2', 'pp-r-up pp-d1', INK, family=CINZEL, size=44, size_t=35, size_m=28, weight=600, lh=1.12)],
                '', gap_=14),
            button('View Full Gallery', '#', 'pp-r-up', bg='rgba(0,0,0,0)', fg=INK, hover_bg=INK, hover_fg='#FFFFFF', border=INK, hover_border=INK, pad=(13, 26)),
        ], 'pp-gal-head', direction='row', justify='space-between', align='flex-end', wrap='wrap', gap_=24),
        con([con([
            image(k, 'pp-cover pp-gimg'),
            heading(tp, 'div', 'pp-gtag', BLUE, family=FIG, size=12, weight=700, lh=1.2),
            con([
                heading(pl, 'h3', '', '#FFFFFF', family=CINZEL, size=21, weight=600, lh=1.2),
                icon_w('fas fa-arrow-right', 'fa-solid', 'pp-garrow', shape='circle', bg='#FFFFFF', fg=NAVY, size=14, padding=13),
            ], 'pp-gfoot', direction='row', justify='space-between', align='center', gap_=12),
        ], f'pp-gcard pp-r-up pp-d{i % 3}', overflow='hidden', radius=24) for i, (k, tp, pl) in enumerate(GAL)],
            'pp-gal-grid', grid={'cols': 3, 'cols_t': 2, 'cols_m': 1, 'gap': 20, 'rows': 2, 'rows_t': 3, 'rows_m': 6}),
    ], 'pp-gal-inner', boxed=1280, full=False, gap_=48, pad=dims(128, 48), pad_t=dims(92, 40), pad_m=dims(80, 20)),
], 'pp-gallery', bg=BG, css_id='work', overflow='hidden')

# ---- testimonials
REV = [('The prep work was thorough and the finish is spotless. The team left the place cleaner than they found it.', 'Customer Name', 'Exterior painting · Suburb', 'C'),
       ('Our roof had leaked for two seasons. Since the restoration we haven’t had a drop come through.', 'Customer Name', 'Roof restoration · Suburb', 'C'),
       ('Clear quote, finished on schedule and minimal disruption for residents. We’ll use them again.', 'Strata Manager', 'Strata painting · Suburb', 'S'),
       ('They talked us through the render system and why it mattered. Two summers on, no cracks.', 'Customer Name', 'Render coating · Suburb', 'C'),
       ('Fast, tidy and honest about what our deck actually needed. It looks brand new.', 'Customer Name', 'Deck restoration · Suburb', 'C')]
def tcard(q, name, meta, ini):
    return con([con([
        widget('star-rating', {'rating_scale': '5', 'rating': 5, 'star_style': 'star_unicode', 'unmarked_star_style': 'solid',
                               'stars_color': BLUE, 'stars_size': px(18), 'icon_space': px(3), 'title': ''}, 'pp-tstars'),
        text(f'<p>"{q}"</p>', 'pp-tquote', NAVY, family=CORM, size=23, weight=500, style='italic', lh=1.32),
        con([
            heading(ini, 'div', 'pp-tinit', BLUE, 'center', family=FIG, size=16, weight=700, lh=1),
            con([heading(name, 'div', '', INK, family=FIG, size=15, weight=700, lh=1.3),
                 heading(meta, 'div', '', '#5A5F66', family=FIG, size=14, weight=400, lh=1.3)], '', gap_=2),
        ], 'pp-tcap', direction='row', gap_=12, align='center'),
    ], 'pp-tfig', gap_=22, justify='space-between', bg='#FFFFFF', radius=26, pad=dims(30))], 'pp-tcard')

testimonials = con([
    deco([image('brush_teal', 'pp-float pp-deco-img pp-rot-m55')], 'pp-deco-t-brush pp-r-zoom'),
    deco([image('cans', 'pp-float pp-deco-img')], 'pp-deco-t-cans pp-r-zoom pp-d1'),
    con([
        con([
            con([eyebrow('Testimonials', GREY),
                 heading('From Our Walls to Yours', 'h2', '', '#FFFFFF', family=CINZEL, size=44, size_t=35, size_m=28, weight=600, lh=1.12)], '', gap_=14),
            con([
                button('←', '#', 'pp-tnav pp-tprev', bg='rgba(0,0,0,0)', fg='#FFFFFF', hover_bg='#FFFFFF', hover_fg=NAVY,
                       border='rgba(255,255,255,0.5)', hover_border='#FFFFFF', size=20, pad=(0, 0), weight=400),
                button('→', '#', 'pp-tnav pp-tnext', bg=BLUE, fg='#FFFFFF', hover_bg='#FFFFFF', hover_fg=NAVY, size=20, pad=(0, 0), weight=400),
            ], '', direction='row', gap_=10),
        ], 'pp-t-head', direction='row', justify='space-between', align='flex-end', wrap='wrap', gap_=24),
        con([con([tcard(*r) for r in REV], 'pp-ttrack', direction='row', wrap='nowrap')], 'pp-tslider', overflow='hidden'),
    ], 'pp-t-panel pp-r-up', boxed=1360, full=False, gap_=40, bg=NAVY, radius=36, overflow='hidden',
        pad=dims(88, 56), pad_t=dims(72, 41), pad_m=dims(56, 20)),
], 'pp-testimonials', pad=dims(190, 24, 0, 24), pad_t=dims(150, 20, 0, 20), pad_m=dims(150, 12, 0, 12), overflow='hidden')

# ---- quote / contact form
def contact_card(label, value, url, icon, bg, value_size):
    return con([
        icon_w(icon[0], icon[1], 'pp-cc-icon', bg=bg, size=20, padding=14, radius=14),
        con([heading(label, 'div', '', '#5A5F66', family=FIG, size=12, weight=700, ls=0.12, transform='uppercase', lh=1.3),
             heading(value, 'div', 'pp-cc-value', INK, family=FIG, size=value_size, weight=700, lh=1.3)], '', gap_=2),
    ], 'pp-cc', direction='row', gap_=14, align='center', bg='#FFFFFF', radius=20, pad=dims(16, 18), tag='a', link=url,
        shadow_=shadow(0, 8, 24, 0, 'rgba(11,43,85,0.06)'))

quote = con([
    deco([con([image('cans', 'pp-deco-img pp-cans-sm'), image('brush_blue', 'pp-deco-img pp-rot-18')], 'pp-float pp-cans-brush', direction='row', gap_=6, align='flex-end')],
         'pp-deco-quote pp-r-zoom'),
    con([
        con([
            eyebrow('Free Quote', cls='pp-r-up'),
            heading('Protect Your Property Before the Next Season Hits', 'h2', 'pp-r-up pp-d1', INK, family=CINZEL, size=48, size_t=39, size_m=30, weight=600, lh=1.1),
            text("<p>Tell us about your project and we'll arrange a free on-site inspection and a written, itemised quote.</p>", 'pp-quote-lead pp-r-up pp-d2', TEXT, family=FIG, size=17, lh=1.6),
            con([
                contact_card('Call Us', PHONE, PHONE_TEL, ('fas fa-phone-alt', 'fa-solid'), BLUE, 17),
                contact_card('Email Us', 'hello@<wbr>platinumpainting.com.au', 'mailto:' + EMAIL, ('far fa-envelope', 'fa-regular'), INK, 15),
            ], 'pp-cc-grid pp-r-up pp-d3', grid={'cols': 2, 'cols_t': 2, 'cols_m': 1, 'gap': 14}),
        ], 'pp-quote-copy', gap_=20, width=50, width_t=100),
        con([widget('shortcode', {'shortcode': '[contact-form-7 id="__CF7_ID__" title="Homepage Quote Form" html_class="pp-cf7"]'})],
            'pp-formbox pp-r-right', bg=BG, radius=32, pad=dims(40), pad_t=dims(31), pad_m=dims(24), width=50, width_t=100),
    ], 'pp-quote-inner', direction='row', direction_t='column', boxed=1280, full=False, gap_=48, align='center',
        pad=dims(128, 48), pad_t=dims(92, 40), pad_m=dims(80, 20)),
], 'pp-quote', bg='#FFFFFF', css_id='quote', overflow='hidden')

HOME = [hero, offers, marquee, about, before_after, services, why, gallery, testimonials, quote]

# ================================================================ HEADER (UAE / HFE template)
NAV_PAGES = [('Home', '/'), ('About Us', '/about/'), ('Services', '/services/'), ('Gallery', '/gallery/'), ('Testimonials', '/testimonials/'), ('Contact Us', '/contact/')]
header = [con([
    con([
        image('logo', 'pp-logo', link='/'),
        widget('navigation-menu', {
            'menu': 'primary-menu', 'layout': 'horizontal', 'navmenu_align': 'center', 'pointer': 'none', 'dropdown': 'tablet',
            'resp_align': 'left', 'full_width_dropdown': 'yes',
            'padding_horizontal_menu_item': px(14), 'padding_vertical_menu_item': px(10),
            **typo('menu_typography', family=FIG, size=15, weight=500, lh=1.2),
            'color_menu_item': NAVY, 'color_menu_item_hover': BLUE, 'color_menu_item_active': BLUE,
            'color_dropdown_item': NAVY, 'background_color_dropdown_item': '#FFFFFF', 'color_dropdown_item_hover': BLUE,
            'background_color_dropdown_item_hover': MIST, 'color_dropdown_item_active': BLUE, 'background_color_dropdown_item_active': '#FFFFFF',
            **typo('dropdown_typography', family=FIG, size=16, weight=500),
            'toggle_color': NAVY, 'toggle_background_color': MIST, 'toggle_hover_color': NAVY, 'toggle_hover_background_color': MIST,
            'toggle_size': px(22), 'toggle_border_width': px(0), 'toggle_border_radius': px(50),
            'dropdown_icon': {'value': 'fas fa-bars', 'library': 'fa-solid'}, 'dropdown_close_icon': {'value': 'fas fa-times', 'library': 'fa-solid'},
            'distance_from_menu': px(18), 'dropdown_divider_border': 'none',
        }, 'pp-nav'),
        con([
            widget('hfe-search-button', {'layout': 'icon', 'placeholder': 'Search…', 'toggle_color': NAVY, 'toggle_color_hover': BLUE,
                                         'toggle_icon_size': px(20), 'hide_tablet': 'hidden-tablet', 'hide_mobile': 'hidden-mobile'}, 'pp-hsearch'),
            con([], 'pp-hdiv', extra={'hide_tablet': 'hidden-tablet', 'hide_mobile': 'hidden-mobile'}),
            button(PHONE, PHONE_TEL, 'pp-hphone pp-btn-lift', size=15, pad=(15, 26), icon=('fas fa-phone-alt', 'fa-solid')),
        ], 'pp-hright', direction='row', gap_=14, align='center'),
    ], 'pp-header-pill', direction='row', justify='space-between', align='center', gap_=20, wrap='nowrap', bg='#FFFFFF', radius=999,
        pad=dims(10, 10, 10, 24), pad_m=dims(8, 8, 8, 16), boxed=1280, full=False),
], 'pp-header', pad=dims(16, 32), pad_t=dims(16, 24), pad_m=dims(12, 12))]

# ================================================================ FOOTER
def link_list(items, color=GREY, cls='pp-flinks'):
    return widget('icon-list', {
        'icon_list': [{'_id': uid('li'), 'text': t, 'selected_icon': {'value': '', 'library': ''},
                       'link': {'url': u, 'is_external': '', 'nofollow': ''}} for t, u in items],
        'space_between': px(12), 'text_color': color, 'text_color_hover': '#FFFFFF',
        **typo('icon_typography', family=FIG, size=15, lh=1.45),
    }, cls)

def fhead(t): return heading(t, 'div', 'pp-fhead', '#FFFFFF', family=CINZEL, size=17, weight=600, lh=1.3)

footer = [con([
    con([
        con([
            con([heading('Ready to Protect Your Property?', 'div', '', '#FFFFFF', family=CINZEL, size=32, size_t=27, size_m=24, weight=600, lh=1.2),
                 text('<p>Free on-site inspection and a written, itemised quote.</p>', '', MIST, family=FIG, size=16, lh=1.5)], '', gap_=6),
            con([
                button('Get a Free Quote', '/contact/', 'pp-btn-lift pp-btn-lift3', bg='#FFFFFF', fg=NAVY, hover_bg='#FFFFFF', hover_fg=NAVY, pad=(15, 28)),
                button(PHONE, PHONE_TEL, '', bg='rgba(0,0,0,0)', fg='#FFFFFF', hover_bg='#FFFFFF', hover_fg=NAVY, border='#FFFFFF', hover_border='#FFFFFF', pad=(13.5, 26)),
            ], '', direction='row', gap_=12, wrap='wrap'),
        ], 'pp-fcta', direction='row', justify='space-between', align='center', wrap='wrap', gap_=24, bg=BLUE,
            pad=dims(48, 56), pad_t=dims(37, 41), pad_m=dims(32, 20)),
        con([
            con([
                con([
                    image('logo_white', 'pp-flogo', link='/'),
                    text('<p>Painting that protects homes, businesses and strata buildings across the Gold Coast.</p>', 'pp-ftag', GREY, family=FIG, size=15, lh=1.6),
                    widget('social-icons', {
                        'social_icon_list': [
                            {'_id': uid('s'), 'social_icon': {'value': 'fab fa-facebook-f', 'library': 'fa-brands'}, 'link': {'url': '#', 'is_external': '', 'nofollow': ''}, 'item_icon_color': 'default'},
                            {'_id': uid('s'), 'social_icon': {'value': 'fab fa-instagram', 'library': 'fa-brands'}, 'link': {'url': '#', 'is_external': '', 'nofollow': ''}, 'item_icon_color': 'default'},
                            {'_id': uid('s'), 'social_icon': {'value': 'fab fa-google', 'library': 'fa-brands'}, 'link': {'url': '#', 'is_external': '', 'nofollow': ''}, 'item_icon_color': 'default'},
                        ],
                        'shape': 'circle', 'align': 'left', 'icon_color': 'custom', 'icon_primary_color': 'rgba(0,0,0,0)', 'icon_secondary_color': '#FFFFFF',
                        'icon_size': px(18), 'icon_padding': px(0.72, 'em'), 'icon_spacing': px(10),
                        'image_border_border': 'solid', 'image_border_width': dims(1), 'image_border_color': '#2A2C30',
                        'hover_primary_color': BLUE, 'hover_secondary_color': '#FFFFFF', 'hover_border_color': BLUE,
                    }, 'pp-fsocial'),
                ], '', gap_=20),
                con([fhead('Services'), link_list([(t, '/services/') for t in ['Interior House Painting', 'Exterior House Painting', 'Commercial Painting', 'Strata / Body Corp Painting', 'Roof Restorations', 'Render Coatings']])], '', gap_=20),
                con([fhead('Company'), link_list([('About Us', '/about/'), ('Gallery', '/gallery/'), ('Testimonials', '/testimonials/'), ('Contact Us', '/contact/')])], '', gap_=20),
                con([fhead('Get in Touch'), widget('icon-list', {
                    'icon_list': [dict({'_id': uid('li'), 'text': t, 'selected_icon': {'value': v, 'library': l}}, **({'link': {'url': u, 'is_external': '', 'nofollow': ''}} if u else {})) for t, v, l, u in [
                        (PHONE, 'fas fa-phone-alt', 'fa-solid', PHONE_TEL), (EMAIL, 'far fa-envelope', 'fa-regular', 'mailto:' + EMAIL),
                        ('Gold Coast, QLD', 'fas fa-map-marker-alt', 'fa-solid', None), ('Mon–Fri 7am–5pm', 'far fa-clock', 'fa-regular', None)]],
                    'text_color_hover': '#FFFFFF',
                    'space_between': px(14), 'icon_color': '#7FA7DB', 'icon_size': px(16), 'text_color': GREY, 'text_indent': px(12),
                    **typo('icon_typography', family=FIG, size=15, lh=1.45),
                }, 'pp-fcontact')], '', gap_=20),
            ], 'pp-fgrid', grid={'cols': 4, 'cols_t': 2, 'cols_m': 1, 'gap': 40, 'rgap': 48}),
            con([
                text('<p>© 2026 Platinum Painting Gold Coast · QBCC Licence 0000000</p>', '', '#8A8F96', family=FIG, size=13, lh=1.5),
                widget('icon-list', {'view': 'inline', 'icon_list': [
                    {'_id': uid('li'), 'text': 'Privacy Policy', 'selected_icon': {'value': '', 'library': ''}, 'link': {'url': '#', 'is_external': '', 'nofollow': ''}},
                    {'_id': uid('li'), 'text': 'Terms', 'selected_icon': {'value': '', 'library': ''}, 'link': {'url': '#', 'is_external': '', 'nofollow': ''}}],
                    'space_between': px(24), 'text_color': '#8A8F96', 'text_color_hover': '#FFFFFF', **typo('icon_typography', family=FIG, size=13, lh=1.5)}, 'pp-flegal'),
            ], 'pp-fbottom', direction='row', justify='space-between', wrap='wrap', gap_=16, align='center'),
        ], 'pp-fmain', gap_=48, pad=dims(64, 56, 28, 56), pad_t=dims(56, 41, 28, 41), pad_m=dims(48, 20, 28, 20)),
    ], 'pp-fpanel', boxed=1360, full=False, bg=INK, radius=36, overflow='hidden'),
], 'pp-footer', pad=dims(0, 24, 24, 24), pad_t=dims(0, 20, 20, 20), pad_m=dims(0, 12, 12, 12))]

for name, data in (('home', HOME), ('header', header), ('footer', footer)):
    json.dump(data, open(os.path.join(OUT, name + '.json'), 'w'), ensure_ascii=False)
    print(name, len(json.dumps(data)))
json.dump(NAV_PAGES, open(os.path.join(OUT, 'nav.json'), 'w'))
