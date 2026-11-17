import type { Recommendation } from "@shared/schema";

const INGREDIENT_MAP: Record<string, string[]> = {
  "Oily+Acne": ["Salicylic Acid (2%)", "Niacinamide (10%)", "Benzoyl Peroxide (2.5%)", "Tea Tree Oil"],
  "Oily+Pores": ["Niacinamide (10%)", "Salicylic Acid (2%)", "Retinol (0.3%)", "AHA/BHA"],
  "Oily+Blackheads": ["Salicylic Acid (2%)", "Clay (Kaolin)", "Charcoal", "Glycolic Acid (7%)"],
  "Oily+Wrinkles": ["Retinol (0.5%)", "Niacinamide (5%)", "Peptides", "Hyaluronic Acid"],
  "Dry+Acne": ["Benzoyl Peroxide (2.5%)", "Niacinamide (5%)", "Ceramides", "Hyaluronic Acid"],
  "Dry+Pores": ["Hyaluronic Acid", "Niacinamide (5%)", "Squalane", "Retinol (0.25%)"],
  "Dry+Wrinkles": ["Retinol (0.5%)", "Peptides", "Ceramides", "Hyaluronic Acid"],
  "Dry+Blackheads": ["Lactic Acid (5%)", "Hyaluronic Acid", "Squalane", "Niacinamide"],
  "Normal+Acne": ["Salicylic Acid (0.5%)", "Niacinamide (5%)", "Zinc", "Green Tea Extract"],
  "Normal+Pores": ["Niacinamide (10%)", "Retinol (0.3%)", "AHA/BHA", "Hyaluronic Acid"],
  "Normal+Wrinkles": ["Retinol (0.5%)", "Vitamin C (15%)", "Peptides", "Hyaluronic Acid"],
  "Normal+Blackheads": ["Salicylic Acid (2%)", "Niacinamide", "Clay Mask", "AHA"],
  "Sensitive+Acne": ["Azelaic Acid (10%)", "Centella Asiatica", "Niacinamide (5%)", "Green Tea"],
  "Sensitive+Pores": ["Niacinamide (5%)", "Centella Asiatica", "Hyaluronic Acid", "Aloe Vera"],
  "Sensitive+Wrinkles": ["Bakuchiol", "Peptides", "Ceramides", "Hyaluronic Acid"],
  "Sensitive+Blackheads": ["Mandelic Acid (5%)", "Niacinamide", "Centella Asiatica", "Green Tea"],
  "Oily+Atopic Dermatitis": ["Ceramides", "Niacinamide (5%)", "Colloidal Oatmeal", "Lightweight Hyaluronic Acid"],
  "Dry+Atopic Dermatitis": ["Ceramides", "Colloidal Oatmeal", "Shea Butter", "Hyaluronic Acid"],
  "Normal+Atopic Dermatitis": ["Ceramides", "Niacinamide (5%)", "Panthenol", "Aloe Vera"],
  "Sensitive+Atopic Dermatitis": ["Ceramides", "Colloidal Oatmeal", "Aloe Vera", "Panthenol"],
  "Oily+Benign Lesion": ["Niacinamide (10%)", "Vitamin C (15%)", "SPF 50+", "Retinol (0.3%)"],
  "Dry+Benign Lesion": ["Vitamin C (10%)", "Ceramides", "SPF 50+", "Hyaluronic Acid"],
  "Normal+Benign Lesion": ["Vitamin C (15%)", "Niacinamide (5%)", "SPF 50+", "Antioxidant Serum"],
  "Sensitive+Benign Lesion": ["Azelaic Acid (10%)", "Centella Asiatica", "SPF 50+", "Ceramides"],
  "Oily+Melanoma": ["SPF 50+ Broad Spectrum", "Vitamin C (15%)", "Niacinamide (10%)", "Antioxidant Complex"],
  "Dry+Melanoma": ["SPF 50+ Broad Spectrum", "Vitamin C (10%)", "Ceramides", "Hyaluronic Acid"],
  "Normal+Melanoma": ["SPF 50+ Broad Spectrum", "Vitamin C (15%)", "Niacinamide", "Antioxidant Complex"],
  "Sensitive+Melanoma": ["SPF 50+ Mineral Sunscreen", "Centella Asiatica", "Ceramides", "Azelaic Acid (10%)"],
  "Oily+Tinea Ringworm Candidiasis": ["Antifungal (Ketoconazole)", "Tea Tree Oil", "Zinc Pyrithione", "Niacinamide (5%)"],
  "Dry+Tinea Ringworm Candidiasis": ["Antifungal (Ketoconazole)", "Ceramides", "Panthenol", "Colloidal Oatmeal"],
  "Normal+Tinea Ringworm Candidiasis": ["Antifungal (Ketoconazole)", "Tea Tree Oil", "Niacinamide", "Zinc"],
  "Sensitive+Tinea Ringworm Candidiasis": ["Antifungal (Miconazole)", "Centella Asiatica", "Aloe Vera", "Ceramides"],
};

const MORNING_ROUTINES: Record<string, string[]> = {
  Oily: [
    "Gentle foaming cleanser",
    "Alcohol-free toner with BHA",
    "Lightweight serum (Niacinamide or Vitamin C)",
    "Oil-free moisturizer with SPF 30+",
  ],
  Dry: [
    "Cream-based gentle cleanser",
    "Hydrating toner with Hyaluronic Acid",
    "Hydrating serum (Hyaluronic Acid)",
    "Rich moisturizer with ceramides",
    "Mineral sunscreen SPF 50",
  ],
  Normal: [
    "Gentle gel cleanser",
    "Balancing toner",
    "Antioxidant serum (Vitamin C)",
    "Lightweight moisturizer with SPF 30+",
  ],
  Sensitive: [
    "Micellar water or ultra-gentle cleanser",
    "Calming toner (Centella Asiatica)",
    "Soothing serum (Centella or Aloe)",
    "Fragrance-free moisturizer with SPF 50",
  ],
};

const NIGHT_ROUTINES: Record<string, string[]> = {
  Oily: [
    "Oil-based cleanser (double cleanse)",
    "Gentle foaming cleanser",
    "Exfoliating toner (2-3x/week)",
    "Treatment serum (Retinol or BHA)",
    "Oil-free night moisturizer",
  ],
  Dry: [
    "Oil-based cleanser",
    "Cream cleanser",
    "Hydrating essence",
    "Night serum (Retinol 1-2x/week)",
    "Rich night cream or sleeping mask",
  ],
  Normal: [
    "Gentle cleanser",
    "Toner",
    "Treatment serum (Retinol 2-3x/week)",
    "Night moisturizer",
  ],
  Sensitive: [
    "Micellar water",
    "Ultra-gentle cream cleanser",
    "Calming serum (Bakuchiol instead of Retinol)",
    "Barrier-repair night cream",
  ],
};

export function generateRecommendation(
  skinType: string,
  disease: string,
  concern: string
): Recommendation {
  const key1 = `${skinType}+${concern}`;
  const key2 = `${skinType}+${disease}`;

  let ingredients = INGREDIENT_MAP[key1] || INGREDIENT_MAP[key2] || [
    "Hyaluronic Acid",
    "Niacinamide (5%)",
    "Ceramides",
    "Vitamin C (10%)",
  ];

  const extraIngredients = INGREDIENT_MAP[key2];
  if (extraIngredients && key1 !== key2) {
    const uniqueSet = new Set([...ingredients, ...extraIngredients]);
    const combined = Array.from(uniqueSet);
    ingredients = combined.slice(0, 6);
  }

  const morning = MORNING_ROUTINES[skinType] || MORNING_ROUTINES["Normal"];
  const night = NIGHT_ROUTINES[skinType] || NIGHT_ROUTINES["Normal"];

  const products = generateProductSuggestions(skinType, disease, concern);
  const tips = generateLifestyleTips(skinType, disease, concern);

  return {
    active_ingredients: ingredients,
    morning_routine: morning,
    night_routine: night,
    product_suggestions: products,
    lifestyle_tips: tips,
  };
}

function generateProductSuggestions(
  skinType: string,
  disease: string,
  concern: string
): { name: string; type: string; description: string }[] {
  const suggestions: { name: string; type: string; description: string }[] = [];

  if (skinType === "Oily") {
    suggestions.push({
      name: "Gel-based Cleanser with Salicylic Acid",
      type: "Cleanser",
      description: "A lightweight, non-stripping cleanser that controls excess oil and unclogs pores.",
    });
  } else if (skinType === "Dry") {
    suggestions.push({
      name: "Cream Cleanser with Ceramides",
      type: "Cleanser",
      description: "A hydrating cleanser that cleanses without disrupting the skin barrier.",
    });
  } else if (skinType === "Sensitive") {
    suggestions.push({
      name: "Fragrance-Free Micellar Cleanser",
      type: "Cleanser",
      description: "An ultra-gentle cleanser that removes impurities without irritation.",
    });
  } else {
    suggestions.push({
      name: "Balanced Gel Cleanser",
      type: "Cleanser",
      description: "A gentle daily cleanser suitable for normal skin to maintain balance.",
    });
  }

  if (concern === "Wrinkles") {
    suggestions.push({
      name: "Retinol 0.5% Night Treatment",
      type: "Treatment",
      description: "Stimulates cell turnover, reduces fine lines, and improves skin texture overnight.",
    });
  }

  if (concern === "Acne" || concern === "Blackheads" || concern === "Pores") {
    suggestions.push({
      name: "Niacinamide 10% + Zinc 1% Serum",
      type: "Serum",
      description: "Reduces sebum production, minimizes pore appearance, and calms blemishes.",
    });
  }

  if (disease === "Acne") {
    suggestions.push({
      name: "Benzoyl Peroxide 2.5% Spot Treatment",
      type: "Treatment",
      description: "Targets active acne breakouts by killing bacteria and reducing inflammation.",
    });
  }

  if (disease === "Atopic Dermatitis") {
    suggestions.push({
      name: "Colloidal Oatmeal Barrier Cream",
      type: "Moisturizer",
      description: "Soothes eczema-prone skin, reduces itching, and restores the moisture barrier.",
    });
  }

  if (disease === "Melanoma" || disease === "Benign Lesion") {
    suggestions.push({
      name: "Broad Spectrum SPF 50+ PA++++ Sunscreen",
      type: "Sunscreen",
      description: "Maximum UV protection essential for skin with lesions or melanoma risk factors.",
    });
    suggestions.push({
      name: "Vitamin C + E + Ferulic Acid Serum",
      type: "Serum",
      description: "Powerful antioxidant protection to prevent further UV-induced skin damage.",
    });
  }

  if (disease === "Tinea Ringworm Candidiasis") {
    suggestions.push({
      name: "Antifungal Cream (Ketoconazole 2%)",
      type: "Treatment",
      description: "Topical antifungal treatment for ringworm, tinea, and candidiasis infections.",
    });
  }

  suggestions.push({
    name: "Broad Spectrum SPF 50+ Sunscreen",
    type: "Sunscreen",
    description: "Essential daily UV protection to prevent photoaging and hyperpigmentation.",
  });

  return suggestions;
}

function generateLifestyleTips(
  skinType: string,
  disease: string,
  concern: string
): string[] {
  const tips: string[] = [
    "Apply SPF 30+ sunscreen daily, even on cloudy days",
    "Drink at least 8 glasses of water daily for optimal hydration",
    "Change pillowcases at least twice a week",
  ];

  if (skinType === "Oily" || concern === "Acne") {
    tips.push("Avoid touching your face throughout the day");
    tips.push("Use oil-free, non-comedogenic makeup products");
  }

  if (skinType === "Dry" || disease === "Atopic Dermatitis") {
    tips.push("Use a humidifier in dry environments");
    tips.push("Avoid hot showers — use lukewarm water instead");
  }

  if (skinType === "Sensitive") {
    tips.push("Patch test all new products before full application");
    tips.push("Avoid fragranced skincare and household products");
  }

  if (concern === "Wrinkles") {
    tips.push("Sleep on your back to minimize sleep wrinkles");
    tips.push("Include antioxidant-rich foods in your diet");
  }

  if (concern === "Blackheads" || concern === "Pores") {
    tips.push("Remove makeup thoroughly before bed every night");
    tips.push("Avoid pore-clogging comedogenic products");
  }

  if (disease === "Melanoma" || disease === "Benign Lesion") {
    tips.push("Consult a dermatologist immediately for professional evaluation");
    tips.push("Monitor any skin lesions for changes in size, shape, or color (ABCDE rule)");
    tips.push("Wear protective clothing and avoid peak sun hours (10am-4pm)");
  }

  if (disease === "Tinea Ringworm Candidiasis") {
    tips.push("Keep affected areas clean and dry");
    tips.push("Avoid sharing towels, clothing, or personal items");
    tips.push("Complete the full course of antifungal treatment");
  }

  if (disease === "Acne") {
    tips.push("Avoid picking or squeezing acne lesions");
    tips.push("Wash face no more than twice daily to avoid over-stripping");
  }

  return tips.slice(0, 6);
}
