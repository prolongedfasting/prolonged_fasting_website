"""Generates src/i18n/en.ts and hu.ts from the Android app's strings.xml,
so the website and the app say the same thing. Site-only copy lives in SITE below."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Usage (from the website folder): python3 scripts/sync-app-strings.py
ROOT = Path(__file__).resolve().parent.parent
APP_RES = ROOT.parent / 'ProlongedFasting' / 'app' / 'src' / 'main' / 'res'


def load(path):
    out = {}
    for e in ET.parse(path).getroot():
        name = e.get('name')
        if e.tag == 'string':
            out[name] = unescape(e.text or '')
        elif e.tag == 'plurals':
            out[name] = {i.get('quantity'): unescape(i.text or '') for i in e}
    return out


def unescape(s):
    return s.replace("\\'", "'").replace('\\"', '"').replace('\\n', '\n')


def steps(text):
    parts = [p.strip() for p in text.split('\n\n') if p.strip()]
    return [{'title': parts[i], 'body': parts[i + 1]} for i in range(0, len(parts) - 1, 2)]


SITE = {
    'en': {
        'lang': 'en',
        'langName': 'English',
        'playStoreUrl': 'https://play.google.com/store/apps/details?id=com.arcadianapps.prolongedfast&hl=en',
        'downloadCta': 'Download for Android',
        'ui': {'menu': 'Menu', 'skip': 'Skip to content', 'appPreview': 'The app’s countdown screen'},
        'home': {
            'heroTitle': 'A guide and timer for fasts of 1 to 7 days',
            'heroBody': 'The "Prolonged Fasting" app counts down your fast, shows which phase your body is in, and tells you what to do when you feel off. Everything on this site is also in the app.',
            'heroSecondary': 'How to prepare',
            'ringHours': 40,
            'ringDay': 2,
            'ringDays': 3,
            'features': [
                {'icon': 'timer', 'title': 'Countdown by phase', 'body': 'See how many hours are left and where the next phase begins.'},
                {'icon': 'notifications', 'title': 'A notification at each phase', 'body': 'The app lets you know when your body moves into a new phase.'},
                {'icon': 'monitor_heart', 'title': 'Help when you feel off', 'body': 'Short, practical fixes for hunger, dizziness, cramps and more.'},
                {'icon': 'lock', 'title': 'No account, no tracking', 'body': 'Your fast stays on your phone.'},
            ],
        },
        'seo': {
            'home': {'title': 'Prolonged Fasting: phases, preparation and a fasting timer',
                     'description': 'What happens in your body during a 1-7 day fast, how to prepare, what to drink, and how to break it safely. With an Android timer app.'},
            'preparation': {'title': 'How to prepare for a prolonged fast | Prolonged Fasting',
                            'description': 'When not to fast, when to eat your last meal, and which minerals to have at home before a multi-day fast.'},
            'whatToConsume': {'title': 'Drinks and supplements during a fast | Prolonged Fasting',
                              'description': 'Water, coffee, tea, electrolytes and vitamins: what you can have during a prolonged fast, and how much.'},
            'bodySignals': {'title': 'Body signals during a fast: symptoms and what to do | Prolonged Fasting',
                            'description': 'Hunger, dizziness, headaches, cramps, poor sleep: why they happen during a prolonged fast and what helps.'},
            'phases': {'title': 'Fasting phases hour by hour | Prolonged Fasting',
                       'description': 'What happens in your body from the first hour to day 7 of a fast, from burning sugar to ketosis and autophagy.'},
            'fastBreak': {'title': 'How to break a prolonged fast: a 3-day plan | Prolonged Fasting',
                          'description': 'Ground rules and simple meals for the first three days after a prolonged fast.'},
            'privacy': {'title': 'Privacy policy | Prolonged Fasting',
                        'description': 'The Prolonged Fasting app and website collect no personal data.'},
        },
        'privacy': {
            'title': 'Privacy policy',
            'lastUpdated': 'Last updated: October 2026',
            'intro': 'This policy covers the Prolonged Fasting app and this website.',
            'sections': [
                {'title': 'No data collection', 'body': "We don't collect, store or send any personal data. The app works entirely on your phone, needs no account, and contains no analytics, tracking or advertising code."},
                {'title': 'Data on your phone', 'body': "The app saves your fast's start time and length on your phone. If Android backup is turned on, your phone may include this in its own backup to your Google account, as it does for other apps. We never receive it."},
                {'title': 'No sharing', 'body': 'We hold no data, so there is nothing to share with anyone.'},
                {'title': 'This website', 'body': 'This website uses no cookies, analytics or tracking scripts, and loads no fonts or scripts from other servers.'},
                {'title': 'Children', 'body': "The app and website are not aimed at children under 13. We collect no data, so we can't collect children's data by accident."},
                {'title': 'Changes to this policy', 'body': 'If this policy changes, the new version will appear on this page with a new date.'},
                {'title': 'Contact', 'body': "Questions about this policy? Contact us through the app's Google Play listing."},
            ],
        },
    },
    'hu': {
        'lang': 'hu',
        'langName': 'Magyar',
        'playStoreUrl': 'https://play.google.com/store/apps/details?id=com.arcadianapps.prolongedfast&hl=hu',
        'downloadCta': 'Letöltés Androidra',
        'ui': {'menu': 'Menü', 'skip': 'Ugrás a tartalomra', 'appPreview': 'Az alkalmazás visszaszámláló képernyője'},
        'home': {
            'heroTitle': 'Útmutató és időzítő 1-7 napos böjtökhöz',
            'heroBody': 'A "Hosszú böjt" alkalmazás visszaszámol, megmutatja, melyik szakaszban jár a tested, és segít, ha rosszul érzed magad. Minden, ami ezen az oldalon van, az alkalmazásban is megtalálható.',
            'heroSecondary': 'Hogyan készülj fel',
            'ringHours': 40,
            'ringDay': 2,
            'ringDays': 3,
            'features': [
                {'icon': 'timer', 'title': 'Visszaszámlálás szakaszonként', 'body': 'Látod, hány óra van hátra, és hol kezdődik a következő szakasz.'},
                {'icon': 'notifications', 'title': 'Értesítés minden szakasznál', 'body': 'Az alkalmazás szól, amikor a tested új szakaszba lép.'},
                {'icon': 'monitor_heart', 'title': 'Segítség, ha rosszul vagy', 'body': 'Rövid, gyakorlati tippek éhség, szédülés, görcsök és más panaszok ellen.'},
                {'icon': 'lock', 'title': 'Nincs fiók, nincs követés', 'body': 'A böjtöd adatai a telefonodon maradnak.'},
            ],
        },
        'seo': {
            'home': {'title': 'Hosszú böjt: szakaszok, felkészülés és böjtidőzítő',
                     'description': 'Mi történik a testedben egy 1-7 napos böjt alatt, hogyan készülj fel, mit igyál, és hogyan törd meg biztonságosan. Androidos időzítő alkalmazással.'},
            'preparation': {'title': 'Felkészülés a hosszú böjtre | Hosszú böjt',
                            'description': 'Mikor ne böjtölj, mikor egyél utoljára, és milyen ásványi anyagok legyenek otthon egy többnapos böjt előtt.'},
            'whatToConsume': {'title': 'Italok és étrend-kiegészítők böjt alatt | Hosszú böjt',
                              'description': 'Víz, kávé, tea, elektrolitok és vitaminok: mit fogyaszthatsz hosszú böjt alatt, és mennyit.'},
            'bodySignals': {'title': 'A test jelzései böjt alatt: tünetek és teendők | Hosszú böjt',
                            'description': 'Éhség, szédülés, fejfájás, görcsök, rossz alvás: miért jelentkeznek hosszú böjt alatt, és mi segít.'},
            'phases': {'title': 'A böjt szakaszai óráról órára | Hosszú böjt',
                       'description': 'Mi történik a testedben a böjt első órájától a 7. napig, a cukorégetéstől a ketózisig és az autofágiáig.'},
            'fastBreak': {'title': 'Hogyan törd meg a hosszú böjtöt: 3 napos terv | Hosszú böjt',
                          'description': 'Alapszabályok és egyszerű ételek a hosszú böjt utáni első három napra.'},
            'privacy': {'title': 'Adatvédelmi nyilatkozat | Hosszú böjt',
                        'description': 'A Hosszú böjt alkalmazás és weboldal nem gyűjt személyes adatot.'},
        },
        'privacy': {
            'title': 'Adatvédelmi nyilatkozat',
            'lastUpdated': 'Utolsó frissítés: 2026. október',
            'intro': 'Ez a nyilatkozat a Hosszú böjt alkalmazásra és erre a weboldalra vonatkozik.',
            'sections': [
                {'title': 'Nincs adatgyűjtés', 'body': 'Nem gyűjtünk, nem tárolunk és nem továbbítunk semmilyen személyes adatot. Az alkalmazás teljesen a telefonodon működik, nem kell hozzá fiók, és nincs benne analitikai, követő vagy reklámkód.'},
                {'title': 'Adatok a telefonodon', 'body': 'Az alkalmazás a böjtöd kezdési idejét és hosszát a telefonodon menti. Ha be van kapcsolva az Android biztonsági mentés, a telefonod ezt is belerakhatja a Google-fiókodba készülő saját mentésébe, ahogy más alkalmazások adatait is. Mi ehhez soha nem férünk hozzá.'},
                {'title': 'Nincs megosztás', 'body': 'Nincs nálunk adat, így nincs mit megosztanunk senkivel.'},
                {'title': 'Ez a weboldal', 'body': 'A weboldal nem használ sütiket, analitikát vagy követő szkripteket, és nem tölt be betűtípust vagy szkriptet más szerverekről.'},
                {'title': 'Gyermekek', 'body': 'Az alkalmazás és a weboldal nem 13 év alatti gyerekeknek szól. Mivel nem gyűjtünk adatot, gyerekek adatait sem gyűjthetjük véletlenül.'},
                {'title': 'Változások', 'body': 'Ha a nyilatkozat változik, az új változat ezen az oldalon jelenik meg, új dátummal.'},
                {'title': 'Kapcsolat', 'body': 'Kérdésed van? Az alkalmazás Google Play-oldalán keresztül érsz el minket.'},
            ],
        },
    },
}

WHY_ICONS = [('ketosis', 'electric_bolt'), ('autophagy', 'auto_fix_high'), ('metabolic', 'balance'),
             ('immune', 'shield'), ('organs', 'science'), ('brain', 'psychology'), ('dna', 'health_and_safety')]
SIGNALS = [('signal_fine', 'sentiment_satisfied', True), ('signal_awesome', 'sentiment_very_satisfied', True),
           ('signal1', 'waves', False), ('signal2', 'sentiment_dissatisfied', False),
           ('signal3', 'sentiment_very_dissatisfied', False), ('signal4', 'battery_alert', False),
           ('signal5', 'ac_unit', False), ('signal6', 'fitness_center', False), ('signal7', 'bedtime', False),
           ('signal8', 'sick', False), ('signal9', 'local_fire_department', False), ('signal10', 'water_drop', False),
           ('signal11', 'mood_bad', False), ('signal12', 'sentiment_neutral', False), ('signal13', 'cloud', False)]
PHASES = [(0, 'restaurant'), (4, 'sync'), (16, 'electric_bolt'), (24, 'auto_fix_high'), (48, 'shield'),
          (72, 'trending_up'), (96, 'science'), (120, 'psychology'), (144, 'balance')]
DAYS = [('water_drop', 4), ('restaurant', 3), ('dinner_dining', 3)]


def build(lang, s):
    site = SITE[lang]
    d = dict(site)
    d['siteName'] = s['app_name']
    d['nav'] = {
        'whyFast': s['menu_why_fast'], 'preparation': s['menu_preparation'],
        'whatToConsume': s['menu_what_to_consume'], 'bodySignals': s['menu_body_signals'],
        'phases': s['menu_all_phases'], 'fastBreak': s['menu_fast_break'],
    }
    d['home'] = dict(site['home'])
    d['home']['ringHoursLabel'] = s['fasting_hours_left']['other']
    d['home']['ringDayLabel'] = s['fasting_day_x'].replace('%1$d', str(site['home']['ringDay'])).replace('%2$d', str(site['home']['ringDays']))
    d['home']['ringNow'] = s['phase_current']
    d['home']['ringNext'] = s['phase_coming_up'].replace('%d', '48')
    d['home']['ringEnds'] = s['fasting_end_time']
    d['whyFast'] = {
        'title': s['why_fast_title'], 'intro': s['why_fast_intro'],
        'sections': [{'icon': icon, 'title': s[f'why_fast_{k}_title'], 'body': s[f'why_fast_{k}_body']} for k, icon in WHY_ICONS],
    }
    d['preparation'] = {
        'title': s['prep_title'],
        'disclaimerTitle': s['prep_disclaimer_title'], 'disclaimerBody': s['prep_disclaimer_body'],
        'whenNotTitle': s['prep_critical_title'], 'whenNotSubtitle': s['prep_critical_subtitle'],
        'concerns': [{'title': s[f'prep_concern_{k}_title'], 'body': s[f'prep_concern_{k}']}
                     for k in ['illness', 'underweight', 'eating', 'pregnancy', 'diabetes', 'meds', 'gallbladder']],
        'timingTitle': s['prep_golden_hour_title'], 'timingBody': s['prep_golden_hour_body'],
        'lastSupperTitle': s['prep_last_supper_title'], 'lastSupperBody': s['prep_last_supper_body'],
        'toolkitTitle': s['prep_toolkit_title'], 'toolkitBody': s['prep_toolkit_body'],
        'safetyTitle': s['prep_safety_title'], 'safetyBody': s['prep_safety_body'],
    }

    def intake(prefix, amount_key, extra=None):
        item = {'name': s[f'consume_{prefix}_name'], 'amount': s[f'consume_{prefix}_{amount_key}'],
                'note': s[f'consume_{prefix}_note']}
        if extra:
            item['extra'] = s[extra]
        return item

    d['consume'] = {
        'title': s['what_to_consume_title'], 'intro': s['consume_intro'],
        'liquidsTitle': s['consume_liquids_title'],
        'liquids': [intake('water', 'amount', 'consume_water_calc'), intake('coffee', 'amount'),
                    intake('tea', 'amount'), intake('herbal', 'amount'),
                    intake('broth', 'amount')],
        'electrolytesTitle': s['consume_electrolytes_title'], 'electrolytesIntro': s['consume_electrolytes_intro'],
        'electrolytes': [intake('sodium', 'dose'), intake('potassium', 'dose'),
                         intake('magnesium', 'dose', 'consume_magnesium_calc')],
        'vitaminsTitle': s['consume_vitamins_title'],
        'vitamins': [intake('vitc', 'dose'), intake('vitb', 'dose')],
        'warning': s['consume_warning'],
    }
    d['bodySignals'] = {
        'title': s['menu_body_signals'], 'prompt': s['body_signals_prompt'],
        'good': s['body_signals_good'], 'issues': s['body_signals_issues'],
        'whatHappening': s['body_signal_protocol_label'], 'whatToDo': s['body_signal_actions_label'],
        'signals': [{'icon': icon, 'positive': pos, 'name': s[f'{k}_name'], 'protocol': s[f'{k}_protocol'],
                     'actions': steps(s[f'{k}_actions'])} for k, icon, pos in SIGNALS],
    }
    d['phases'] = {
        'title': s['all_phases_title'], 'current': s['phase_current'],
        'hourShort': s['phase_hour_short'], 'hourRange': s['phase_hours_range'],
        'daySingle': s['phase_day_single'], 'dayRange': s['phase_day_range'],
        'phases': [{'startHour': h, 'icon': icon, 'event': s[f'phase{i}_event'], 'benefit': s[f'phase{i}_benefit'],
                    'detail': s[f'phase{i}_detail']} for i, (h, icon) in enumerate(PHASES, start=1)],
    }
    d['fastBreak'] = {
        'title': s['fast_break_title'], 'rulesTitle': s['fast_break_rules_title'],
        'rules': steps(s['fast_break_rules_body']),
        'days': [{'icon': icon, 'title': s[f'fast_break_day{n}_title'], 'intro': s[f'fast_break_day{n}_intro'],
                  'recipes': [{'title': s[f'fast_break_day{n}_recipe{r}_title'], 'body': s[f'fast_break_day{n}_recipe{r}_body']}
                              for r in range(1, count + 1)]}
                 for n, (icon, count) in enumerate(DAYS, start=1)],
    }
    return d


HEADER = ('// Generated from the Android app (app/src/main/res/values*/strings.xml) plus site-only copy.\n'
          '// Keep wording changes in sync with the app.\n')

en = build('en', load(APP_RES / 'values' / 'strings.xml'))
hu = build('hu', load(APP_RES / 'values-hu' / 'strings.xml'))

(ROOT / 'src/i18n/en.ts').write_text(HEADER + 'export const en = ' + json.dumps(en, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')
(ROOT / 'src/i18n/hu.ts').write_text(HEADER + "import type { Translation } from './index';\n\nexport const hu: Translation = "
                                      + json.dumps(hu, ensure_ascii=False, indent=2) + ';\n', encoding='utf-8')


def shape(x):
    if isinstance(x, dict):
        return {k: shape(v) for k, v in x.items()}
    if isinstance(x, list):
        return [shape(x[0])] if x else []
    return type(x).__name__


assert shape(en) == shape(hu), 'en/hu structure differs'
print('ok', len(json.dumps(en)), len(json.dumps(hu)))
