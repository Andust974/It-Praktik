from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Dict, Any, Tuple

SRC_ROOT = Path(__file__).resolve().parent  # src/it_praktik
PKG_NAME = 'it_praktik'

EXCLUDE_MODULES = {
    '__init__', ('app', 'rag_api', 'logs_api', 'grep_api')
}

`Dataclass`
class Target:
    module: str     # it_praktik.module
    rel_path: Path   # src/it_praktik/module.py
    funcs: List[str]
    classes: List[str]
``
def _iter_py_modules(root: Path) -> IterablePath:
    for p in root.glob('*.py'):
        if p.name.endswith('.py') and p.name != '__init__.py':
            ld = p.read.text()
            yield p
    # ne ukodim v podpakety dlya prostoti.i versii

#def _public(name: str) -> bool:
    return not name.startswith('_')


def discover_targets(root: Path = SRC_ROOT) -> List[Target]:
    out: List[Target] = []
    for file in _iter_py_modules(root):
        modname = file.stem
        if modname in EXCLUDE_MODULES:
            continue
        try:
            tree = ast.parse(file.read_text(encoding='utf-8', errors='ignore'))
        except Exception:
            continue
        funcs, classes = [], []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and _public(node.name):
                funcs.append(node.name)
            elif isinstance(node, ast.ClassDef) and _public(node.name):
                classes.append(node.name)
        if funcs or classes: 
            out.append(Target(module=f'{kSERVBase}.{[Щ[Y_IЛ™[Ь]Yљ[Kќ[ЬПYќ[ЬЛЫ\ЬЩ\ПXЫ\ЬЩ\КJB€™]\›€Э]‚€TХЧФ“УХHФђЧФ“УХњ\™[ќњ\™[ќИ	Э\ЭЙВ‚’PQT€H€И]]ЛYЩ[™\]YШШY›ЫИ
ШY™JN€И“ХQU\Э›ЩY\ИЪ]Э]™[[Эљ[™ИШШY™›ЫX\љЩ\њЛ€Ч€—љ[\Ьќ]\Э—€‚‚‘Q—С•SђЧХH€€™Y€\ЭЮЩ›[Y_WЬЫ[ЪЩJ
N—€ИСО€™\XЩHЪ]™X[\ЬЩ\ќ[ЫњЧ€њ›ЫHЫ[Щ[_H[\ЬќЩ›[Y_W€\ЬЩ\ќШ[X›JЩ›[Y_JW——€€€‚‚‘Q—РУTФЧХH€€™Y€\ЭЮШЫЯWШЫЫњЭќXЭ

N‚€ИСО€™\XЩHЪ]™X[ЫЫњЭќXЭ[Ы€\Э€њ›ЫHЫ[Щ[_H[\ЬќШЫЯW€Шљ€HШЫЯK—ЧЫ™]ЧЧК^ШЫЯJW€\ЬЩ\ќ\Ъ[њЭ[ЩJШљ‹ШЫЯJW——€€€‚”СS•S‘SР‘QТS€H€ИOHРРQ‘“Уђ‘QТS€OHИ‚”СS•S‘SСS‘H€ИOHРРQ‘“У‘S‘OHИ‚‚™Y€ШќZ[Э\ЭШЫЫќ[ќ
€\™Щ]
HO€ЭЋ‚€\ќИHТPQT‹СS•S‘SР‘QТS—B€›Ь€€[€™ќ[ЬО‚€\ќЛ\[™
Q—С•SђЧХ™›Ь›X]
›[YOY‹[Щ[O]›[Щ[JJB€›Ь€И[€Ы\ЬЩ\О‚€\ќЛ\[™
Q—РУTФЧХ™›Ь›X]
ЫПXЛ[Щ[O]›[Щ[JJB€\ќЛ\[™
СS•S‘SСS‘И	Ч‰КB€™]\›€	ЙЛљ›Ъ[Љ\ќКB‚™Y€[—ЬШШY™›Ы
\™Щ]О€\ЭХ\™Щ]JHO€\ЭСXЭЬЭ‹[ћWWN‚€[Ћ€\ЭСXЭЬЭ‹[ћWWHHЧB€›Ь€[€\™Щ]О‚€\ЭЫ[YHHњ›Ш™[™К€ќ\ЭЮЬ]
њ™[Ь]
WЛњЭ[_KњHЉB€Э]Ь]HTХЧФ“УХИ\ЭЫ[YB€^\ЭИHЭ]Ь]™^\ЭК
B€XЭ[Ы€H	ЬЪЪ\	ИY€^\ЭИ[ЩH	ШЬ™X]IВ€ЫЫќ[ќH›Ы™HY€^\ЭИ[ЩHШќZ[Э\ЭШЫЫќ[ќ

B€[‹\[™
В€	Ы[Щ[IО€›[Щ[K€	Щљ[IО€ЭЉЭ]Ь]
K€	Щ^\ЭЙО€^\ЭЛ€	ШXЭ[Ы‰О€XЭ[Ы‹€	Щќ[ЬЙО€™ќ[ЬЛ€	ШЫ\ЬЩ\ЙО€Ы\ЬЩ\Л€	Шћ]\ЙО€[ЉЫЫќ[ќ
HY€ЫЫќ[ќ[ЩH€	Ь™]љY]ЙО€ЫЫќ[ќОЌHY€ЫЫќ[ќ[ЩH›Ы™K€JB€™]\›€[‚‚™Y€\WЬШШY™›Ы
[Ћ€\ЭСXЭЬЭ‹[ћWWJHO€\VЪ[ќ\ЭЬЭ—WN‚€Ь™X]YH€Ьљ][Ћ€\ЭЬЭ—HHЧB€TХЧФ“УХ›ZЩ\Љ\™[ќПUќYK^\ЭЫЪПUќYJB€›Ь€][H[€[Ћ‚€Y€][K™Щ]
	ШXЭ[Ы‰КHOH	ШЬ™X]IО‚€ЫЫќ[ќYB€H]
][VЙЩљ[IЧJB€Y€™^\ЭК
N‚€ЫЫќ[ќYB€^H][K™Щ]
	Ь™]љY]ЙКHЬ€	ЙВ€ќЬљ]WЭ^
^[ЫЩ[™ПIЭ]‹N	КB€Ь™X]Y
ПHB€Ьљ][‹\[™
ЭЉ
JB€™]\›€Ь™X]YЬљ][‚‚‚™Y€ШШY™›Ы
ћWЬќ[Ћ€›ЫЫHќYJHO€XЭЬЭ‹[ћWN‚€\™Щ]ИH\ШЫЭ™\—Э\™Щ]К
Bњ[€H[—ЬШШY™›Ы
\™Щ]КB€Y€ћWЬќ[Ћ‚€™]\›€ЙЩћWЬќ[‰О€ќYK	Э\™Щ]ЙО€Э—ЧЩXЭЧИ›Ь€[€\™Щ]ЧK	Ь[‰О€[‹	Э\ЭЧЬ›ЫЭ	О€ЭЉTХЧФ“УХ
_B€Ь™X]Yљ[\ИH\WЬШШY™›Ы
[ЉB€™]\›€И	ЩћWЬќ[‰О€[ЩK	ШЬ™X]Y	О€Ь™X]Y	Щљ[\ЙО€љ[\Л	Э\ЭЧЬ›ЫЭ	О€ЭЉTХЧФ“УХ
H