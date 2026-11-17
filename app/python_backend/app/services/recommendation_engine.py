from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Recommendation:
    skin_type: str
    disease: str
    concern: str
    active_ingredients: list[str]
    morning_routine: list[str]
    night_routine: list[str]
    product_suggestions: list[dict]
    tips: list[str]


# Curated combinations: key = "SkinType|Disease|Concern"
_MAPPING: Dict[str, Dict[str, Any]] = {
    "Oily|Acne|pores": {
        "active_ingredients": ["Salicylic Acid (BHA)", "Niacinamide 5–10%", "Zinc PCA", "Lightweight non-comedogenic moisturizer"],
        "morning_routine": [
            "Gentle foaming cleanser with salicylic acid (leave on 30–60 sec)",
            "Alcohol-free toner with niacinamide to minimize pores",
            "Oil-free gel moisturizer; wait 2 min before SPF",
            "Broad-spectrum SPF 50, non-comedogenic, reapply if outdoors",
        ],
        "night_routine": [
            "Double cleanse if wearing sunscreen/makeup (oil-free first step, then foaming)",
            "BHA leave-on (2% salicylic acid) 2–3x/week; avoid on same night as retinoids",
            "Niacinamide serum; optional lightweight retinol 2x/week for pores",
            "Lightweight gel or lotion moisturizer",
        ],
        "product_suggestions": [
            {"name": "Salicylic Acid 2% Cleanser", "type": "cleanser", "url": "#"},
            {"name": "Niacinamide 10% + Zinc", "type": "serum", "url": "#"},
            {"name": "Oil-Free SPF 50", "type": "sunscreen", "url": "#"},
        ],
        "tips": [
            "Do not over-exfoliate: max 2–3x/week BHA to avoid barrier damage.",
            "Introduce one active at a time and patch-test.",
            "If using prescription retinoids, use BHA on alternate nights only.",
        ],
    },
    "Oily|Acne|acne": {
        "active_ingredients": ["Salicylic Acid", "Benzoyl Peroxide (spot)", "Niacinamide", "Azelaic Acid"],
        "morning_routine": [
            "Gentle foaming cleanser",
            "Niacinamide serum (helps oil and post-inflammatory marks)",
            "Lightweight moisturizer; benzoyl peroxide 2.5–5% on spots only if tolerated",
            "Oil-free SPF 50",
        ],
        "night_routine": [
            "Cleanser; double cleanse if needed",
            "Alternate: BHA 2–3x/week or adapalene (start 2x/week, build tolerance)",
            "Azelaic acid 10% can be used with retinoids for marks and mild acne",
            "Lightweight moisturizer",
        ],
        "product_suggestions": [
            {"name": "BHA 2% Liquid", "type": "treatment", "url": "#"},
            {"name": "Benzoyl Peroxide 2.5%", "type": "spot treatment", "url": "#"},
            {"name": "Niacinamide Serum", "type": "serum", "url": "#"},
        ],
        "tips": [
            "Prescription options (e.g. adapalene, tretinoin) may be more effective; consult a dermatologist.",
            "Avoid picking; use pimple patches for isolated spots.",
        ],
    },
    "Dry|Unknown|wrinkles": {
        "active_ingredients": ["Hyaluronic Acid", "Ceramides", "Retinol/Retinoids", "Peptides", "Vitamin C"],
        "morning_routine": [
            "Cream or milky cleanser (non-stripping)",
            "Vitamin C serum (L-ascorbic or gentle derivatives)",
            "Hyaluronic acid serum on damp skin, then moisturizer",
            "Rich moisturizer with ceramides; SPF 50 (essential for anti-aging)",
        ],
        "night_routine": [
            "Gentle cleanse",
            "Retinol 2–3x/week (start low concentration); off nights use peptide or barrier serum",
            "Ceramide-rich moisturizer; optional thin occlusive on very dry areas",
        ],
        "product_suggestions": [
            {"name": "Hyaluronic Acid Serum", "type": "serum", "url": "#"},
            {"name": "Ceramide Moisturizer", "type": "moisturizer", "url": "#"},
            {"name": "Retinol 0.3%", "type": "treatment", "url": "#"},
        ],
        "tips": [
            "Dry skin tolerates retinol better when applied over moisturizer (buffer).",
            "SPF daily is non-negotiable to protect collagen and prevent further wrinkles.",
        ],
    },
    "Sensitive|Unknown|Unknown": {
        "active_ingredients": ["Panthenol", "Allantoin", "Ceramides", "Niacinamide (low %)", "Fragrance-free formulas"],
        "morning_routine": [
            "Fragrance-free gentle cleanser (cream or gel)",
            "Soothing serum with panthenol or allantoin",
            "Barrier moisturizer with ceramides",
            "Mineral SPF 50 (zinc/titanium) if tolerated; otherwise seek dermatologist recommendation",
        ],
        "night_routine": [
            "Same gentle cleanser",
            "Barrier repair moisturizer",
            "Introduce actives only after skin is stable; one at a time, patch test 1 week",
        ],
        "product_suggestions": [
            {"name": "Gentle Cream Cleanser", "type": "cleanser", "url": "#"},
            {"name": "Barrier Repair Cream", "type": "moisturizer", "url": "#"},
            {"name": "Mineral SPF 50", "type": "sunscreen", "url": "#"},
        ],
        "tips": [
            "Avoid fragrance, essential oils, and high concentrations of acids/retinoids until barrier is strong.",
            "If reactions persist, see a dermatologist for patch testing.",
        ],
    },
    "Normal|Unknown|Blackheads": {
        "active_ingredients": ["Salicylic Acid (BHA)", "Niacinamide", "Clay masks", "Non-comedogenic products"],
        "morning_routine": [
            "Gentle cleanser with BHA or separate BHA toner 2–3x/week",
            "Niacinamide serum",
            "Lightweight moisturizer; SPF 50",
        ],
        "night_routine": [
            "Cleanser",
            "BHA leave-on 2–3x/week; clay mask 1x/week on oily areas",
            "Moisturizer",
        ],
        "product_suggestions": [
            {"name": "BHA 2% Toner", "type": "treatment", "url": "#"},
            {"name": "Clay Mask", "type": "mask", "url": "#"},
            {"name": "Niacinamide Serum", "type": "serum", "url": "#"},
        ],
        "tips": [
            "Blackheads respond to consistent BHA; results take 4–8 weeks.",
            "Do not over-use clay or BHA to avoid dryness.",
        ],
    },
}


def _build_key(skin_type: str, disease: str, concern: str) -> str:
    return f"{skin_type}|{disease}|{concern}"


def _generic_ingredients_for_type(skin_type: str) -> list[str]:
    if skin_type == "Oily":
        return ["Niacinamide", "Salicylic Acid", "Lightweight non-comedogenic moisturizer"]
    if skin_type == "Dry":
        return ["Ceramides", "Hyaluronic Acid", "Glycerin"]
    if skin_type == "Sensitive":
        return ["Panthenol", "Allantoin", "Fragrance-free formulas"]
    return ["Balanced moisturizers", "Broad spectrum SPF 50"]


def _generic_for_disease(disease: str) -> list[str]:
    if disease == "Acne":
        return ["Benzoyl Peroxide (spot use)", "Adapalene/Retinoids (as tolerated)", "Non-comedogenic moisturizer"]
    if disease == "Atopic Dermatitis":
        return ["Ceramide-rich moisturizers", "Colloidal oatmeal", "Avoid fragrance and harsh surfactants"]
    if disease == "Melanoma":
        return ["Urgent in-person dermatology evaluation is recommended"]
    if disease == "Tinea Ringworm Candidiasis":
        return ["Antifungal therapy may be required; seek medical guidance"]
    return []


def _generic_for_concern(concern: str) -> list[str]:
    if concern == "wrinkles":
        return ["Retinoids (start low, go slow)", "Daily SPF 50", "Peptides", "Vitamin C (AM)"]
    if concern == "Blackheads":
        return ["Salicylic Acid (BHA)", "Clay masks 1–2x/week", "Non-comedogenic products"]
    if concern == "pores":
        return ["Niacinamide", "BHA exfoliants", "Oil-control formulations"]
    if concern == "acne":
        return ["Salicylic Acid", "Azelaic Acid", "Benzoyl Peroxide (spot use)"]
    return []

def _generic_routine_for_type(skin_type: str) -> tuple[list[str], list[str]]:
    if skin_type == "Oily":
        morning = [
            "Gentle foaming cleanser",
            "Niacinamide serum",
            "Oil-free moisturizer (light gel)",
            "Broad spectrum SPF 50",
        ]
        night = [
            "Cleanser (double cleanse if sunscreen/makeup)",
            "BHA exfoliant 2–3x/week (salicylic acid)",
            "Lightweight moisturizer",
        ]
        return morning, night
    if skin_type == "Dry":
        morning = [
            "Cream cleanser (non-stripping)",
            "Hydrating serum (hyaluronic acid/glycerin)",
            "Ceramide moisturizer",
            "Broad spectrum SPF 50",
        ]
        night = [
            "Gentle cleanse",
            "Barrier-supporting moisturizer (ceramides)",
            "Optional: occlusive layer for very dry areas",
        ]
        return morning, night
    if skin_type == "Sensitive":
        morning = [
            "Fragrance-free gentle cleanser",
            "Soothing serum (panthenol/allantoin)",
            "Barrier moisturizer",
            "Mineral SPF 50 (if tolerated)",
        ]
        night = [
            "Gentle cleanse",
            "Barrier moisturizer",
            "Introduce actives slowly, patch test",
        ]
        return morning, night
    morning = ["Gentle cleanser", "Hydrating serum", "Moisturizer", "Broad spectrum SPF 50"]
    night = ["Gentle cleanse", "Targeted active as needed", "Moisturizer"]
    return morning, night


def generate_recommendation(
    skin_type: Optional[str] = None,
    disease: Optional[str] = None,
    concern: Optional[str] = None,
) -> Recommendation:
    skin_type = skin_type or "Unknown"
    disease = disease or "Unknown"
    concern = concern or "Unknown"

    key = _build_key(skin_type, disease, concern)
    entry: Optional[Dict[str, Any]] = _MAPPING.get(key)

    if entry is None:
        base_ingredients = _generic_ingredients_for_type(skin_type) if skin_type != "Unknown" else []
        disease_ingredients = _generic_for_disease(disease) if disease != "Unknown" else []
        concern_ingredients = _generic_for_concern(concern) if concern != "Unknown" else []

        ingredients = list(dict.fromkeys(base_ingredients + disease_ingredients + concern_ingredients))

        morning, night = _generic_routine_for_type(skin_type) if skin_type != "Unknown" else (
            ["Gentle cleanser", "Targeted serum (based on results)", "Broad spectrum SPF 50"],
            ["Gentle cleanse", "Targeted active (as tolerated)", "Moisturizer"],
        )

        products = [
            {"name": "Gentle Cleanser", "type": "cleanser", "url": "#"},
            {"name": "Broad Spectrum SPF 50", "type": "sunscreen", "url": "#"},
        ]
        tips = [
            "Introduce one new product at a time and patch-test.",
            "Daily SPF is recommended for all skin types.",
        ]
    else:
        ingredients = entry["active_ingredients"]
        morning = entry["morning_routine"]
        night = entry["night_routine"]
        products = entry["product_suggestions"]
        tips = entry.get("tips", [
            "These are general guidelines; adjust frequency based on your tolerance.",
            "Consult a dermatologist for a personalized plan.",
        ])

    return Recommendation(
        skin_type=skin_type,
        disease=disease,
        concern=concern,
        active_ingredients=ingredients,
        morning_routine=morning,
        night_routine=night,
        product_suggestions=products,
        tips=tips,
    )

