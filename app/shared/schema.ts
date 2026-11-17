import { z } from "zod";

export const SKIN_TYPE_CLASSES = ["Dry", "Normal", "Oily", "Sensitive"] as const;
export const SKIN_DISEASE_CLASSES = ["Acne", "Atopic Dermatitis", "Benign Lesion", "Melanoma", "Tinea Ringworm Candidiasis"] as const;
export const SKIN_CONCERN_CLASSES = ["Acne", "Blackheads", "Pores", "Wrinkles"] as const;

export const ANALYSIS_MODES = ["full", "skin_type", "disease", "concern"] as const;

export type AnalysisMode = typeof ANALYSIS_MODES[number];
export type SkinTypeClass = typeof SKIN_TYPE_CLASSES[number];
export type SkinDiseaseClass = typeof SKIN_DISEASE_CLASSES[number];
export type SkinConcernClass = typeof SKIN_CONCERN_CLASSES[number];

export interface PredictionResult {
  label: string;
  confidence: number;
}

export interface ModelPrediction {
  predicted_class: string;
  confidence: number;
  all_predictions: PredictionResult[];
  status: "SUCCESS" | "LOW_CONFIDENCE_RETRY";
}

export interface GradCAMResult {
  heatmap_base64: string;
  overlay_base64: string;
}

export interface Recommendation {
  active_ingredients: string[];
  morning_routine: string[];
  night_routine: string[];
  product_suggestions: { name: string; type: string; description: string }[];
  lifestyle_tips: string[];
}

export interface AnalysisResult {
  id: string;
  mode: AnalysisMode;
  timestamp: string;
  original_image_base64: string;
  skin_type?: ModelPrediction;
  skin_disease?: ModelPrediction;
  skin_concern?: ModelPrediction;
  gradcam_disease?: GradCAMResult;
  gradcam_concern?: GradCAMResult;
  recommendation?: Recommendation;
  overall_status: "SUCCESS" | "LOW_CONFIDENCE_RETRY";
  low_confidence_message?: string;
}

export const analysisRequestSchema = z.object({
  mode: z.enum(ANALYSIS_MODES),
});

export type AnalysisRequest = z.infer<typeof analysisRequestSchema>;

