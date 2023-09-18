from enum import Enum

from pydantic import BaseModel


class Zone(BaseModel):
    name: str
    id: int


class Dungeons(Enum):
    HOV: str = "hov"
    SBG: str = "sbg"
    TJS: str = "tjs"
    RLP: str = "rlp"
    NO: str = "no"
    COS: str = "cos"
    AA: str = "aa"
    AV: str = "av"
    ULD: str = "uld"
    BH: str = "bh"
    NLT: str = "nlt"
    HOI: str = "hoi"
    NL: str = "nl"
    FH: str = "fh"
    UNDR: str = "undr"
    TVP: str = "tvp"
    TOT: str = "tot"
    TEB: str = "teb"
    WCM: str = "wcm"
    AD: str = "ad"
    UDI: str = "udi"
    DDI: str = "ddi"
    BRH: str = "brh"
    BHT: str = "bht"


DungCurrentSeason: list[Dungeons] = [
    Dungeons.ULD,
    Dungeons.BH,
    Dungeons.NLT,
    Dungeons.HOI,
    Dungeons.NL,
    Dungeons.FH,
    Dungeons.UNDR,
]

WLogsMapping: dict = {
    "hov": 61477,
    "sbg": 61176,
    "tjs": 10960,
    "rlp": 12521,
    "no": 12516,
    "cos": 61571,
    "aa": 12526,
    "av": 12515,
    "uld": 12451,
    "bh": 12520,
    "nlt": 12519,
    "hoi": 12527,
    "nl": 61458,
    "fh": 61754,
    "undr": 61841,
    "tvp": 10657,
}

RioMapping: dict = {
    "hov": 7672,
    "sbg": 6932,
    "tjs": 5965,
    "rlp": 14063,
    "no": 13982,
    "cos": 8079,
    "aa": 14032,
    "av": 13954,
    "uld": 13968,
    "bh": 13991,
    "nlt": 14011,
    "hoi": 14082,
    "nl": 7546,
    "fh": 9164,
    "undr": 9193,
    "tvp": 5035,
}


class RaidDiffuclty(Enum):
    All = 0
    Normal = 3
    Heroic = 4
    Mythic = 5


class Raids(Enum):
    VOTI = "voti"
    ATSC = "atsc"


WlogsVOTIMapping: dict = {
    "era": 2587,
    "ter": 2639,
    "tpc": 2590,
    "sen": 2592,
    "dat": 2635,
    "kur": 2605,
    "diu": 2614,
    "raz": 2607,
}

WlogsATSCMapping: dict = {
    "kzr": 2688,
    "tac": 2687,
    "tfe": 2693,
    "atz": 2682,
    "rte": 2680,
    "zkr": 2689,
    "mgm": 2683,
    "eon": 2684,
    "scs": 2685,
}


RaidsDict: dict = {
    "voti": WlogsVOTIMapping,
    "atsc": WlogsATSCMapping,
}


RaidCurrent: Raids = Raids.ATSC
