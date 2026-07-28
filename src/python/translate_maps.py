import re
import unicodedata
from typing import Dict


def _normalize_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


TITLE_FR_MAP: Dict[str, str] = {
    "phd": "Doctorat",
    "doctoral student": "Doctorant",
    "doctorate student": "Doctorant",
    "master s": "Maitrise",
    "master student": "Étudiant à la maîtrise",
    "master s student": "Étudiant à la maîtrise",
    "ma student": "Étudiant à la maîtrise",
    "student": "Étudiant",
    "postdoctoral fellow": "Stagiaire postdoctoral",
    "postdoctoral researcher": "Chercheur postdoctoral",
    "postdoctoral scholar": "Stagiaire postdoctoral",
    "postdoc": "Postdoctorat",
    "professor": "Professeur",
    "associate professor": "Professeur agrégé",
    "assistant professor": "Professeur adjoint",
    "web developer": "Developpeuse web",
    "administrator": "Administratrice",
    "james mcgill professor academic lead of the mcgill csdc": "Professeur James McGill, Responsable académique du CSDC McGill",
    "professor inaugural diamond brown chair in democratic studies": "Professeur, Titulaire inaugural de la Chaire Diamond-Brown en études démocratiques",
    "associate professor member of the steering committee of the csdc at": "Professeur agrégé, Membre du Comité directeur du CSDC à",
    "associate professor member of the steering committee of the csdc at laval": "Professeur agrégé, Membre du Comité directeur du CSDC à Laval",
}


DEPARTMENT_FR_MAP: Dict[str, str] = {
    "political science": "Science politique",
    "sociology": "Sociologie",
    "communication studies": "Communication",
    "computer science": "Informatique",
    "geography": "Géographie",
    "psychology": "Psychologie",
    "economics": "Économie",
    "neurology and neurosurgery": "Neurologie et neurochirurgie",
    "institute for information systems engineering": "Institut de génie des systèmes d'information",
}


def _strip_department_prefix(text: str) -> str:
    patterns = [
        r"^department of\s+",
        r"^departement de\s+",
        r"^departement d\s+",
        r"^departement des\s+",
        r"^departement du\s+",
        r"^departement\s+",
    ]
    out = text
    for pattern in patterns:
        out = re.sub(pattern, "", out)
    return out.strip()


def translate_title_to_fr(title: str) -> str:
    if title is None:
        return title
    cleaned = str(title).strip()
    if not cleaned:
        return cleaned

    key = _normalize_text(cleaned)
    return TITLE_FR_MAP.get(key, cleaned)


def translate_department_to_fr(department: str) -> str:
    if department is None:
        return department
    cleaned = str(department).strip()
    if not cleaned:
        return cleaned

    key = _normalize_text(cleaned)
    direct = DEPARTMENT_FR_MAP.get(key)
    if direct:
        return direct

    stripped_key = _strip_department_prefix(key)
    mapped = DEPARTMENT_FR_MAP.get(stripped_key)
    if mapped:
        return mapped

    return cleaned
