import type { Express } from "express";
import { createServer, type Server } from "http";
import multer from "multer";
import { randomUUID } from "crypto";
import { analysisRequestSchema, type AnalysisResult, type AnalysisMode } from "@shared/schema";

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 8 * 1024 * 1024 },
  fileFilter: (_req, file, cb) => {
    const allowed = ["image/jpeg", "image/png", "image/jpg"];
    if (allowed.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error("Only JPEG and PNG images are allowed"));
    }
  },
});

const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || "http://127.0.0.1:8000";

function mapModeToPython(mode: AnalysisMode): string {
  switch (mode) {
    case "disease": return "skin_disease";
    case "concern": return "skin_concern";
    default: return mode;
  }
}

const LABEL_NORMALIZE: Record<string, string> = {
  "benign_lesion": "Benign Lesion",
  "acne": "Acne",
  "pores": "Pores",
  "wrinkles": "Wrinkles",
};

function normalizeLabel(label: string): string {
  return LABEL_NORMALIZE[label] || label;
}

function transformPythonResponse(
  pyData: any,
  mode: AnalysisMode,
  imageBase64: string
): AnalysisResult {
  const transformPrediction = (pred: any) => {
    if (!pred) return undefined;
    const allPredictions = Object.entries(pred.probabilities || {}).map(
      ([label, confidence]) => ({
        label: normalizeLabel(label),
        confidence: confidence as number,
      })
    );
    allPredictions.sort((a, b) => b.confidence - a.confidence);
    return {
      predicted_class: normalizeLabel(pred.label),
      confidence: pred.confidence,
      all_predictions: allPredictions,
      status: (pred.status === "OK" ? "SUCCESS" : "LOW_CONFIDENCE_RETRY") as "SUCCESS" | "LOW_CONFIDENCE_RETRY",
    };
  };

  const transformGradcam = (base64Str: string | null | undefined) => {
    if (!base64Str) return undefined;
    return {
      heatmap_base64: base64Str,
      overlay_base64: base64Str,
    };
  };

  const transformRecommendation = (rec: any) => {
    if (!rec) return undefined;
    return {
      active_ingredients: rec.active_ingredients || [],
      morning_routine: rec.morning_routine || [],
      night_routine: rec.night_routine || [],
      product_suggestions: (rec.product_suggestions || []).map((p: any) => ({
        name: p.name,
        type: p.type,
        description: p.description || `Recommended ${p.type} for your skin profile`,
      })),
      lifestyle_tips: rec.tips || [],
    };
  };

  const overallStatus = pyData.global_status === "OK" ? "SUCCESS" : "LOW_CONFIDENCE_RETRY";

  return {
    id: randomUUID(),
    mode,
    timestamp: new Date().toISOString(),
    original_image_base64: imageBase64,
    skin_type: transformPrediction(pyData.skin_type),
    skin_disease: transformPrediction(pyData.skin_disease),
    skin_concern: transformPrediction(pyData.skin_concern),
    gradcam_disease: transformGradcam(pyData.gradcam?.disease),
    gradcam_concern: transformGradcam(pyData.gradcam?.concern),
    recommendation: transformRecommendation(pyData.recommendation),
    overall_status: overallStatus as "SUCCESS" | "LOW_CONFIDENCE_RETRY",
    low_confidence_message: pyData.message || undefined,
  };
}

export async function registerRoutes(
  httpServer: Server,
  app: Express
): Promise<Server> {

  app.post("/api/analyze", (req, res, next) => {
    upload.single("image")(req, res, (err: any) => {
      if (err) {
        if (err instanceof multer.MulterError) {
          return res.status(400).json({ message: err.message });
        }
        return res.status(400).json({ message: err.message || "File upload error" });
      }
      next();
    });
  }, async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({ message: "No image file provided" });
      }

      const modeParam = req.body.mode || "full";
      const parseResult = analysisRequestSchema.safeParse({ mode: modeParam });
      if (!parseResult.success) {
        return res.status(400).json({ message: "Invalid analysis mode" });
      }

      const mode: AnalysisMode = parseResult.data.mode;
      const imageBase64 = `data:${req.file.mimetype};base64,${req.file.buffer.toString("base64")}`;
      const pythonMode = mapModeToPython(mode);

      const blob = new Blob([req.file.buffer], { type: req.file.mimetype });
      const formData = new globalThis.FormData();
      formData.append("file", blob, req.file.originalname || "image.jpg");

      const pyUrl = `${PYTHON_BACKEND_URL}/api/analyze?mode=${pythonMode}`;

      const pyRes = await fetch(pyUrl, {
        method: "POST",
        body: formData,
      });

      if (!pyRes.ok) {
        const errorText = await pyRes.text();
        console.error("Python backend error:", pyRes.status, errorText);
        return res.status(pyRes.status).json({ 
          message: `Analysis failed: ${errorText}` 
        });
      }

      const pyData = await pyRes.json();
      const result = transformPythonResponse(pyData, mode, imageBase64);

      res.json(result);
    } catch (error: any) {
      console.error("Analysis error:", error);
      if (error.cause?.code === "ECONNREFUSED") {
        return res.status(503).json({ 
          message: "AI analysis service is starting up. Please try again in a moment." 
        });
      }
      res.status(500).json({ message: error.message || "Analysis failed" });
    }
  });

  app.get("/api/health", async (_req, res) => {
    try {
      const pyRes = await fetch(`${PYTHON_BACKEND_URL}/health`);
      const pyHealth = await pyRes.json();
      res.json({ status: "ok", python_backend: pyHealth.status });
    } catch {
      res.json({ status: "ok", python_backend: "unavailable" });
    }
  });

  return httpServer;
}
