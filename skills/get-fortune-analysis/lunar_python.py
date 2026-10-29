# Requires: pip install lunar_python
import datetime
from lunar_python import Lunar, Solar

# lunar_python returns Heavenly Stems / Earthly Branches as Chinese characters.
# Below, those characters are written as \uXXXX escapes to keep this source file
# ASCII-only; at runtime the keys still match the library's output exactly.
STEM_OF = {
    "\u7532": "Jia", "\u4e59": "Yi", "\u4e19": "Bing", "\u4e01": "Ding",
    "\u620a": "Wu", "\u5df1": "Ji", "\u5e9a": "Geng", "\u8f9b": "Xin",
    "\u58ec": "Ren", "\u7678": "Gui",
}
BRANCH_OF = {
    "\u5b50": "Zi", "\u4e11": "Chou", "\u5bc5": "Yin", "\u536f": "Mao",
    "\u8fb0": "Chen", "\u5df3": "Si", "\u5348": "Wu", "\u672a": "Wei",
    "\u7533": "Shen", "\u9149": "You", "\u620c": "Xu", "\u4ea5": "Hai",
}


def get_cyber_divination_data(birth_year, birth_month, birth_day, birth_hour=0, birth_minute=0):
    """
    Cyber fortune-telling core algorithm v2.1
    - Output is tailored for HTML front-end rendering
    """

    # --- Base configuration (simplified) ---
    ELEMENT_OF_STEM = {
        "Jia": "Wood", "Yi": "Wood", "Bing": "Fire", "Ding": "Fire",
        "Wu": "Earth", "Ji": "Earth", "Geng": "Metal", "Xin": "Metal",
        "Ren": "Water", "Gui": "Water",
    }
    ELEMENT_OF_BRANCH = {
        "Zi": "Water", "Chou": "Earth", "Yin": "Wood", "Mao": "Wood",
        "Chen": "Earth", "Si": "Fire", "Wu": "Fire", "Wei": "Earth",
        "Shen": "Metal", "You": "Metal", "Xu": "Earth", "Hai": "Water",
    }
    RELATIONSHIP = {
        "Wood": {"Wood": "same", "Fire": "generates", "Earth": "controls", "Metal": "controlled", "Water": "generated"},
        "Fire": {"Wood": "generated", "Fire": "same", "Earth": "generates", "Metal": "controls", "Water": "controlled"},
        "Earth": {"Wood": "controlled", "Fire": "generated", "Earth": "same", "Metal": "generates", "Water": "controls"},
        "Metal": {"Wood": "controls", "Fire": "controlled", "Earth": "generated", "Metal": "same", "Water": "generates"},
        "Water": {"Wood": "generates", "Fire": "controls", "Earth": "controlled", "Metal": "generated", "Water": "same"},
    }
    TEN_GODS = {
        "same_same": "BiJian (Friend)", "diff_same": "JieCai (Rob)",
        "same_generates": "ShiShen (Artist)", "diff_generates": "ShangGuan (Rebel)",
        "same_controls": "PianCai (Windfall)", "diff_controls": "ZhengCai (Salary)",
        "same_controlled": "QiSha (7-Killings)", "diff_controlled": "ZhengGuan (Officer)",
        "same_generated": "PianYin (Owl)", "diff_generated": "ZhengYin (Seal)",
    }
    YANG_STEMS = ["Jia", "Bing", "Wu", "Geng", "Ren"]
    YANG_SIGNS = ["Jia", "Bing", "Wu", "Geng", "Ren", "Yin", "Shen", "Si", "Hai"]

    # --- 1. Chart casting ---
    solar = Solar.fromYmdHms(birth_year, birth_month, birth_day, birth_hour, birth_minute, 0)
    lunar = Lunar.fromSolar(solar)
    ba_zi = lunar.getEightChar()
    day_master = STEM_OF.get(ba_zi.getDayGan(), ba_zi.getDayGan())
    dm_element = ELEMENT_OF_STEM[day_master]
    dm_yin_yang = "yang" if day_master in YANG_STEMS else "yin"

    # --- 2. Helper functions ---
    def get_ten_god(target_stem):
        if not target_stem: return ""
        target_element = ELEMENT_OF_STEM.get(target_stem) or ELEMENT_OF_BRANCH.get(target_stem)
        rel = RELATIONSHIP[dm_element].get(target_element, "same")

        # simplified yin/yang determination
        target_yy = "yang" if target_stem in YANG_SIGNS else "yin"
        is_same = (dm_yin_yang == target_yy)
        key = f"{'same' if is_same else 'diff'}_{rel if rel in ['generates', 'controls', 'generated', 'controlled'] else 'same'}"
        return TEN_GODS.get(key, "unknown")

    # --- 3. Hard rules for body strength ---
    score = 0
    month_branch = BRANCH_OF.get(ba_zi.getMonthZhi(), ba_zi.getMonthZhi())
    m_ele = ELEMENT_OF_BRANCH[month_branch]

    # in season (+40)
    if RELATIONSHIP[dm_element][m_ele] in ["same", "generated"]: score += 40
    elif RELATIONSHIP[dm_element][m_ele] == "controlled": score -= 20

    # rooted (+15/each)
    for zhi in [ba_zi.getYearZhi(), ba_zi.getDayZhi(), ba_zi.getTimeZhi()]:
        if ELEMENT_OF_BRANCH[BRANCH_OF.get(zhi, zhi)] == dm_element: score += 15

    strength = "strong" if score >= 40 else "weak"

    # --- 4. Annual fortune ---
    current_year = datetime.datetime.now().year
    # Simplified annual-pillar calculation (a real implementation would use
    # Li Chun / Start of Spring as the boundary; here we simply take the
    # current lunar year's stem-branch).
    # Correction: get the current year's stem-branch directly from Lunar
    current_lunar = Lunar.fromYmd(current_year, 6, 1)
    annual_stem = STEM_OF.get(current_lunar.getYearGan(), current_lunar.getYearGan())
    annual_branch = BRANCH_OF.get(current_lunar.getYearZhi(), current_lunar.getYearZhi())

    annual_god = get_ten_god(annual_stem)

    return {
        "meta": {
            "solar_date": f"{birth_year}-{birth_month}-{birth_day}",
            "lunar_date": f"lunar year {lunar.getYearInChinese()}, month {lunar.getMonthInChinese()}, day {lunar.getDayInChinese()}"
        },
        "bazi": {
            "day_master": day_master,
            "element": dm_element,
            "strength": strength,
            "score": score
        },
        "fortune": {
            "current_year": f"{current_year} ({annual_stem}{annual_branch})",
            "year_god": annual_god.split(" ")[0], # keep only the name, e.g. "QiSha"
            "lucky_direction": lunar.getDayPositionCaiDesc() # Wealth God direction
        }
    }
