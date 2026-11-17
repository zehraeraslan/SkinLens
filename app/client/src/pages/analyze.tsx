import { useState, useCallback, useRef } from "react";
import { Link, useSearch } from "wouter";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowRight,
  ArrowLeft,
  Upload,
  Image as ImageIcon,
  Layers,
  Sparkles,
  Stethoscope,
  Microscope,
  X,
  AlertTriangle,
  CheckCircle2,
  Loader2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import type { AnalysisMode, AnalysisResult } from "@shared/schema";
import ResultsDashboard from "@/components/results-dashboard";
import { SkinLensLogo, SkinLensIcon } from "@/components/skinlens-logo";

const analysisOptions = [
  {
    mode: "full" as AnalysisMode,
    icon: Layers,
    title: "Full Skin Analysis",
    description: "Run all three models for a comprehensive report.",
    gradient: "from-blue-500 to-cyan-400",
    detail: "Skin Type + Disease + Concern Detection",
  },
  {
    mode: "skin_type" as AnalysisMode,
    icon: Sparkles,
    title: "Skin Type Analysis",
    description: "Classify your skin type accurately.",
    gradient: "from-emerald-500 to-teal-400",
    detail: "Dry · Normal · Oily · Sensitive",
  },
  {
    mode: "disease" as AnalysisMode,
    icon: Stethoscope,
    title: "Disease Detection",
    description: "Screen for common dermatological conditions.",
    gradient: "from-orange-500 to-amber-400",
    detail: "Acne · Atopic Dermatitis · Benign Lesion · Melanoma · Tinea",
  },
  {
    mode: "concern" as AnalysisMode,
    icon: Microscope,
    title: "Concern Detection",
    description: "Identify visible skin concerns.",
    gradient: "from-violet-500 to-purple-400",
    detail: "Acne · Blackheads · Pores · Wrinkles",
  },
];

const processingSteps = [
  { label: "Preprocessing Image", duration: 1200 },
  { label: "Analyzing Skin Type", duration: 1500 },
  { label: "Detecting Skin Diseases", duration: 2000 },
  { label: "Identifying Skin Concerns", duration: 1800 },
  { label: "Generating Recommendations", duration: 1000 },
];

type Step = "mode" | "upload" | "processing" | "results";

export default function AnalyzePage() {
  const searchString = useSearch();
  const params = new URLSearchParams(searchString);
  const initialMode = (params.get("mode") as AnalysisMode) || null;

  const [step, setStep] = useState<Step>(initialMode ? "upload" : "mode");
  const [selectedMode, setSelectedMode] = useState<AnalysisMode | null>(initialMode);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [processingStep, setProcessingStep] = useState(0);
  const [progressValue, setProgressValue] = useState(0);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleModeSelect = (mode: AnalysisMode) => {
    setSelectedMode(mode);
    setStep("upload");
  };

  const handleFileSelect = useCallback((file: File) => {
    if (!file.type.match(/^image\/(jpeg|png|jpg)$/)) {
      setError("Please upload a JPEG or PNG image.");
      return;
    }
    if (file.size > 8 * 1024 * 1024) {
      setError("File size must be less than 8MB.");
      return;
    }
    setError(null);
    setSelectedFile(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFileSelect(file);
    },
    [handleFileSelect]
  );

  const handleAnalyze = async () => {
    if (!selectedFile || !selectedMode) return;

    setStep("processing");
    setProcessingStep(0);
    setProgressValue(0);

    const formData = new FormData();
    formData.append("image", selectedFile);
    formData.append("mode", selectedMode);

    const stepsForMode =
      selectedMode === "full"
        ? processingSteps
        : selectedMode === "skin_type"
        ? processingSteps.slice(0, 2)
        : selectedMode === "disease"
        ? [processingSteps[0], processingSteps[2]]
        : [processingSteps[0], processingSteps[3]];

    const totalDuration = stepsForMode.reduce((a, b) => a + b.duration, 0);
    let elapsed = 0;

    for (let i = 0; i < stepsForMode.length; i++) {
      setProcessingStep(i);
      const stepDuration = stepsForMode[i].duration;
      const startProgress = (elapsed / totalDuration) * 100;
      const endProgress = ((elapsed + stepDuration) / totalDuration) * 100;

      const frames = 20;
      for (let f = 0; f < frames; f++) {
        await new Promise((r) => setTimeout(r, stepDuration / frames));
        setProgressValue(startProgress + ((endProgress - startProgress) * f) / frames);
      }
      elapsed += stepDuration;
    }

    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.message || "Analysis failed");
      }

      const data: AnalysisResult = await res.json();
      setProgressValue(100);
      await new Promise((r) => setTimeout(r, 500));
      setResult(data);
      setStep("results");
    } catch (err: any) {
      setError(err.message || "Something went wrong. Please try again.");
      setStep("upload");
    }
  };

  const handleReset = () => {
    setStep("mode");
    setSelectedMode(null);
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    setProcessingStep(0);
    setProgressValue(0);
  };

  return (
    <div className="min-h-screen bg-background" data-testid="analyze-page">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <SkinLensLogo size={32} />
            <span className="font-semibold text-lg tracking-tight">SkinLens</span>
          </Link>
          <div className="hidden md:flex items-center gap-8">
            <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Home</Link>
            <Link href="/analyze" className="text-sm text-foreground font-medium transition-colors">Analyze</Link>
            <Link href="/about" className="text-sm text-muted-foreground hover:text-foreground transition-colors">About</Link>
          </div>
          {step !== "mode" && step !== "processing" && (
            <Button variant="outline" size="sm" onClick={handleReset} data-testid="btn-new-analysis">
              New Analysis
            </Button>
          )}
        </div>
      </nav>

      <div className="pt-24 pb-16 px-6">
        <AnimatePresence mode="wait">
          {step === "mode" && (
            <motion.div
              key="mode"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-4xl mx-auto"
            >
              <div className="text-center mb-12">
                <h1 className="text-3xl font-bold tracking-tight mb-3" data-testid="text-mode-title">Select Analysis Mode</h1>
                <p className="text-muted-foreground max-w-lg mx-auto">
                  Choose the type of analysis you'd like to perform on your skin image.
                </p>
              </div>

              <div className="grid sm:grid-cols-2 gap-5">
                {analysisOptions.map((opt, i) => (
                  <motion.div
                    key={opt.mode}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.08 }}
                  >
                    <Card
                      className="p-6 cursor-pointer group border-border/50 hover:border-border hover:shadow-md transition-all"
                      onClick={() => handleModeSelect(opt.mode)}
                      data-testid={`btn-mode-${opt.mode}`}
                    >
                      <div className="flex items-start justify-between mb-4">
                        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${opt.gradient} flex items-center justify-center shadow-sm`}>
                          <opt.icon className="w-6 h-6 text-white" />
                        </div>
                        <ArrowRight className="w-5 h-5 text-muted-foreground/40 group-hover:text-foreground group-hover:translate-x-0.5 transition-all" />
                      </div>
                      <h3 className="font-semibold text-lg mb-1">{opt.title}</h3>
                      <p className="text-sm text-muted-foreground mb-3">{opt.description}</p>
                      <span className="text-xs text-muted-foreground/70">{opt.detail}</span>
                    </Card>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}

          {step === "upload" && (
            <motion.div
              key="upload"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-2xl mx-auto"
            >
              <button
                onClick={() => { setStep("mode"); setSelectedMode(null); }}
                className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground mb-8 transition-colors"
                data-testid="btn-back-mode"
              >
                <ArrowLeft className="w-4 h-4" />
                Back to mode selection
              </button>

              <div className="text-center mb-8">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-600 border border-blue-100 mb-4">
                  {analysisOptions.find((o) => o.mode === selectedMode)?.title}
                </div>
                <h1 className="text-3xl font-bold tracking-tight mb-3" data-testid="text-upload-title">Upload Your Image</h1>
                <p className="text-muted-foreground">
                  Upload a clear, well-lit facial skin photo for the best results.
                </p>
              </div>

              {error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="mb-6 p-4 rounded-xl bg-red-50 border border-red-100 flex items-start gap-3"
                  data-testid="error-message"
                >
                  <AlertTriangle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-red-800">Error</p>
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                  <button onClick={() => setError(null)} className="ml-auto">
                    <X className="w-4 h-4 text-red-400" />
                  </button>
                </motion.div>
              )}

              <Card className="border-border/50 overflow-hidden">
                <div
                  className={`relative p-8 ${
                    isDragging
                      ? "bg-blue-50/80 border-2 border-dashed border-blue-300"
                      : previewUrl
                      ? "bg-muted/20"
                      : "bg-muted/10"
                  } transition-colors`}
                  onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                  onDragLeave={() => setIsDragging(false)}
                  onDrop={handleDrop}
                  data-testid="dropzone"
                >
                  {previewUrl ? (
                    <div className="flex flex-col items-center">
                      <div className="relative w-full max-w-sm mx-auto mb-6">
                        <img
                          src={previewUrl}
                          alt="Preview"
                          className="w-full h-auto rounded-xl shadow-lg object-cover max-h-80"
                          data-testid="img-preview"
                        />
                        <button
                          onClick={() => {
                            setSelectedFile(null);
                            setPreviewUrl(null);
                          }}
                          className="absolute top-2 right-2 w-8 h-8 rounded-full bg-black/50 text-white flex items-center justify-center hover:bg-black/70 transition-colors"
                          data-testid="btn-remove-image"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                      <div className="flex items-center gap-2 text-sm text-muted-foreground mb-1">
                        <CheckCircle2 className="w-4 h-4 text-green-500" />
                        <span>{selectedFile?.name}</span>
                      </div>
                      <span className="text-xs text-muted-foreground">
                        {selectedFile && (selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      </span>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center py-8">
                      <div className="w-16 h-16 rounded-2xl bg-blue-50 flex items-center justify-center mb-5">
                        <Upload className="w-7 h-7 text-blue-500" />
                      </div>
                      <p className="font-medium mb-1">
                        {isDragging ? "Drop your image here" : "Drag & drop your image here"}
                      </p>
                      <p className="text-sm text-muted-foreground mb-5">or click to browse files</p>
                      <Button
                        variant="outline"
                        onClick={() => fileInputRef.current?.click()}
                        data-testid="btn-browse"
                      >
                        <ImageIcon className="w-4 h-4 mr-2" />
                        Choose File
                      </Button>
                      <p className="text-xs text-muted-foreground/60 mt-4">
                        Supports JPEG, PNG · Max 8MB
                      </p>
                    </div>
                  )}
                  {!previewUrl && (
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/jpeg,image/png"
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) handleFileSelect(file);
                      }}
                      data-testid="input-file"
                    />
                  )}
                  {previewUrl && (
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/jpeg,image/png"
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) handleFileSelect(file);
                      }}
                    />
                  )}
                </div>

                {previewUrl && (
                  <div className="p-5 border-t border-border/50">
                    <Button
                      className="w-full h-12"
                      onClick={handleAnalyze}
                      data-testid="btn-analyze"
                    >
                      Start Analysis
                      <ArrowRight className="w-5 h-5 ml-2" />
                    </Button>
                  </div>
                )}
              </Card>
            </motion.div>
          )}

          {step === "processing" && (
            <motion.div
              key="processing"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="max-w-lg mx-auto pt-12"
            >
              <div className="text-center mb-12">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  className="inline-flex w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-400 items-center justify-center mb-6 shadow-lg"
                >
                  <SkinLensIcon size={32} className="text-white" />
                </motion.div>
                <h2 className="text-2xl font-bold tracking-tight mb-2" data-testid="text-processing">Analyzing Your Image</h2>
                <p className="text-muted-foreground">Please wait while our AI models process your skin image...</p>
              </div>

              <Card className="p-6 border-border/50 mb-8">
                <Progress value={progressValue} className="h-2 mb-6" data-testid="progress-bar" />
                <div className="space-y-3">
                  {(selectedMode === "full"
                    ? processingSteps
                    : selectedMode === "skin_type"
                    ? processingSteps.slice(0, 2)
                    : selectedMode === "disease"
                    ? [processingSteps[0], processingSteps[2]]
                    : [processingSteps[0], processingSteps[3]]
                  ).map((s, i) => (
                    <div
                      key={s.label}
                      className={`flex items-center gap-3 py-2 px-3 rounded-lg transition-all ${
                        i === processingStep
                          ? "bg-blue-50 text-blue-700"
                          : i < processingStep
                          ? "text-green-600"
                          : "text-muted-foreground/50"
                      }`}
                    >
                      {i < processingStep ? (
                        <CheckCircle2 className="w-[18px] h-[18px] text-green-500 flex-shrink-0" />
                      ) : i === processingStep ? (
                        <Loader2 className="w-[18px] h-[18px] animate-spin flex-shrink-0" />
                      ) : (
                        <div className="w-[18px] h-[18px] rounded-full border-2 border-current flex-shrink-0" />
                      )}
                      <span className="text-sm font-medium">{s.label}</span>
                    </div>
                  ))}
                </div>
              </Card>

              <p className="text-center text-xs text-muted-foreground/60">
                This typically takes 5-10 seconds depending on the analysis mode.
              </p>
            </motion.div>
          )}

          {step === "results" && result && (
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <ResultsDashboard result={result} onReset={handleReset} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
