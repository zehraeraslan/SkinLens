import { useState } from "react";
import { motion } from "framer-motion";
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  Download,
  Droplets,
  Eye,
  FlaskConical,
  Moon,
  Sun,
  ShoppingBag,
  Heart,
  BarChart3,
  RefreshCw,
  Shield,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Cell,
} from "recharts";
import type { AnalysisResult, ModelPrediction } from "@shared/schema";

interface Props {
  result: AnalysisResult;
  onReset: () => void;
}

const CHART_COLORS = ["#3b82f6", "#06b6d4", "#10b981", "#f59e0b", "#8b5cf6"];

function ConfidenceBadge({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color = pct >= 90 ? "text-green-600 bg-green-50 border-green-100" : pct >= 70 ? "text-blue-600 bg-blue-50 border-blue-100" : "text-amber-600 bg-amber-50 border-amber-100";
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 text-xs font-semibold rounded-full border ${color}`} data-testid="badge-confidence">
      {pct}%
    </span>
  );
}

function PredictionCard({
  title,
  icon: Icon,
  prediction,
  color,
  gradient,
}: {
  title: string;
  icon: any;
  prediction: ModelPrediction;
  color: string;
  gradient: string;
}) {
  return (
    <Card className="p-5 border-border/50" data-testid={`card-${title.toLowerCase().replace(/\s/g, "-")}`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center`}>
            <Icon className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-sm">{title}</h3>
            <p className="text-xs text-muted-foreground">
              {prediction.status === "SUCCESS" ? "Analysis Complete" : "Low Confidence"}
            </p>
          </div>
        </div>
        <ConfidenceBadge value={prediction.confidence} />
      </div>
      <div className="flex items-center gap-3 p-3 rounded-xl bg-muted/50 mb-3">
        <div className={`w-2 h-8 rounded-full bg-gradient-to-b ${gradient}`} />
        <div>
          <span className="text-xs text-muted-foreground">Predicted</span>
          <p className="font-semibold text-lg leading-tight" data-testid={`text-prediction-${title.toLowerCase().replace(/\s/g, "-")}`}>
            {prediction.predicted_class}
          </p>
        </div>
      </div>
      <div className="space-y-2">
        {prediction.all_predictions.map((p, i) => (
          <div key={p.label} className="flex items-center gap-2">
            <span className="text-xs text-muted-foreground w-20 truncate">{p.label}</span>
            <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${p.confidence * 100}%` }}
                transition={{ delay: i * 0.1, duration: 0.6 }}
                className="h-full rounded-full"
                style={{ backgroundColor: CHART_COLORS[i % CHART_COLORS.length] }}
              />
            </div>
            <span className="text-xs font-medium w-10 text-right">{Math.round(p.confidence * 100)}%</span>
          </div>
        ))}
      </div>
    </Card>
  );
}

export default function ResultsDashboard({ result, onReset }: Props) {
  const [activeTab, setActiveTab] = useState("overview");

  if (result.overall_status === "LOW_CONFIDENCE_RETRY") {
    return (
      <div className="max-w-2xl mx-auto pt-8">
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}>
          <Card className="p-8 border-amber-200 bg-amber-50/30 text-center" data-testid="card-low-confidence">
            <div className="w-16 h-16 rounded-2xl bg-amber-100 flex items-center justify-center mx-auto mb-5">
              <AlertTriangle className="w-8 h-8 text-amber-600" />
            </div>
            <h2 className="text-xl font-bold mb-3 text-amber-800">Low Confidence Result</h2>
            <p className="text-amber-700 mb-6 max-w-md mx-auto leading-relaxed">
              {result.low_confidence_message ||
                "The lighting or focus of the image is insufficient. Please upload a clearer photo for an accurate dermatological assessment."}
            </p>
            <Button onClick={onReset} className="h-11" data-testid="btn-retry">
              <RefreshCw className="w-4 h-4 mr-2" />
              Try Again with a Better Photo
            </Button>
          </Card>
          <Card className="p-5 border-amber-200 bg-amber-50/30 mt-6 text-left" data-testid="card-medical-disclaimer-low">
            <div className="flex items-start gap-3">
              <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
                <Shield className="w-5 h-5 text-amber-600" />
              </div>
              <div>
                <h4 className="font-semibold text-sm text-amber-800 mb-1">Important Medical Disclaimer</h4>
                <p className="text-xs text-amber-700 leading-relaxed">
                  SkinLens results are <strong>advisory and preliminary only</strong> and are <strong>not a substitute for
                  professional medical advice, diagnosis, or treatment</strong>. Please consult a qualified dermatologist
                  for accurate diagnosis.
                </p>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    );
  }

  const diseaseChartData = result.skin_disease?.all_predictions.map((p) => ({
    name: p.label,
    value: Math.round(p.confidence * 100),
  }));

  const concernChartData = result.skin_concern?.all_predictions.map((p) => ({
    subject: p.label,
    value: Math.round(p.confidence * 100),
    fullMark: 100,
  }));

  return (
    <div className="max-w-6xl mx-auto" data-testid="results-dashboard">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold tracking-tight mb-1" data-testid="text-results-title">Analysis Results</h1>
          <p className="text-sm text-muted-foreground">
            {new Date(result.timestamp).toLocaleString()} · {result.mode === "full" ? "Full Analysis" : result.mode === "skin_type" ? "Skin Type" : result.mode === "disease" ? "Disease Detection" : "Concern Detection"}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={onReset} data-testid="btn-new-analysis-results">
            <RefreshCw className="w-4 h-4 mr-2" />
            New Analysis
          </Button>
          <Button variant="outline" onClick={() => handleExportReport(result)} data-testid="btn-export">
            <Download className="w-4 h-4 mr-2" />
            Export Report
          </Button>
        </div>
      </div>

      <div className="flex items-center gap-2 mb-6">
        <CheckCircle2 className="w-5 h-5 text-green-500" />
        <span className="text-sm font-medium text-green-700">All models returned confident results</span>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="bg-muted/50" data-testid="tabs-results">
          <TabsTrigger value="overview" data-testid="tab-overview">Overview</TabsTrigger>
          {(result.skin_disease || result.skin_concern) && (
            <TabsTrigger value="charts" data-testid="tab-charts">Charts</TabsTrigger>
          )}
          {(result.gradcam_disease || result.gradcam_concern) && (
            <TabsTrigger value="heatmaps" data-testid="tab-heatmaps">Grad-CAM</TabsTrigger>
          )}
          {result.recommendation && (
            <TabsTrigger value="recommendations" data-testid="tab-recommendations">Recommendations</TabsTrigger>
          )}
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid md:grid-cols-3 gap-5">
            <Card className="p-4 border-border/50 md:row-span-2">
              <p className="text-xs font-medium text-muted-foreground mb-3">Uploaded Image</p>
              <img
                src={result.original_image_base64}
                alt="Uploaded skin"
                className="w-full rounded-xl object-cover aspect-square"
                data-testid="img-uploaded"
              />
            </Card>

            <div className="md:col-span-2 grid sm:grid-cols-2 gap-5">
              {result.skin_type && (
                <PredictionCard
                  title="Skin Type"
                  icon={Droplets}
                  prediction={result.skin_type}
                  color="text-emerald-500"
                  gradient="from-emerald-500 to-teal-400"
                />
              )}
              {result.skin_disease && (
                <PredictionCard
                  title="Skin Disease"
                  icon={Eye}
                  prediction={result.skin_disease}
                  color="text-orange-500"
                  gradient="from-orange-500 to-amber-400"
                />
              )}
              {result.skin_concern && (
                <PredictionCard
                  title="Skin Concern"
                  icon={FlaskConical}
                  prediction={result.skin_concern}
                  color="text-violet-500"
                  gradient="from-violet-500 to-purple-400"
                />
              )}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="charts" className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            {diseaseChartData && (
              <Card className="p-5 border-border/50" data-testid="chart-disease">
                <h3 className="font-semibold mb-1">Disease Prediction Distribution</h3>
                <p className="text-xs text-muted-foreground mb-4">Confidence scores across all disease classes</p>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={diseaseChartData} layout="vertical" margin={{ left: 10, right: 20 }}>
                      <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="hsl(var(--border))" />
                      <XAxis type="number" domain={[0, 100]} tickFormatter={(v) => `${v}%`} fontSize={11} />
                      <YAxis type="category" dataKey="name" width={80} fontSize={11} />
                      <Tooltip
                        formatter={(value: number) => [`${value}%`, "Confidence"]}
                        contentStyle={{
                          backgroundColor: "hsl(var(--card))",
                          border: "1px solid hsl(var(--border))",
                          borderRadius: "8px",
                          fontSize: "12px",
                        }}
                      />
                      <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={24}>
                        {diseaseChartData.map((_: any, i: number) => (
                          <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </Card>
            )}

            {concernChartData && (
              <Card className="p-5 border-border/50" data-testid="chart-concern">
                <h3 className="font-semibold mb-1">Concern Prediction Radar</h3>
                <p className="text-xs text-muted-foreground mb-4">Multi-dimensional concern analysis visualization</p>
                <div className="h-72">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={concernChartData} cx="50%" cy="50%" outerRadius="70%">
                      <PolarGrid stroke="hsl(var(--border))" />
                      <PolarAngleAxis dataKey="subject" fontSize={11} />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} fontSize={10} />
                      <Radar
                        name="Confidence"
                        dataKey="value"
                        stroke="#8b5cf6"
                        fill="#8b5cf6"
                        fillOpacity={0.2}
                        strokeWidth={2}
                      />
                      <Tooltip
                        formatter={(value: number) => [`${value}%`, "Confidence"]}
                        contentStyle={{
                          backgroundColor: "hsl(var(--card))",
                          border: "1px solid hsl(var(--border))",
                          borderRadius: "8px",
                          fontSize: "12px",
                        }}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </Card>
            )}
          </div>
        </TabsContent>

        <TabsContent value="heatmaps" className="space-y-6">
          <Card className="p-6 border-border/50" data-testid="card-gradcam">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-red-50 flex items-center justify-center">
                <Eye className="w-5 h-5 text-red-500" />
              </div>
              <div>
                <h3 className="font-semibold">Grad-CAM Heatmaps</h3>
                <p className="text-xs text-muted-foreground">
                  Visualization of regions the model focused on for predictions
                </p>
              </div>
            </div>

            <div className="grid sm:grid-cols-2 gap-6">
              {result.gradcam_disease && (
                <div>
                  <p className="text-sm font-medium mb-3">Disease Detection Focus</p>
                  <div className="relative rounded-xl overflow-hidden bg-muted/30 aspect-square">
                    <img
                      src={result.original_image_base64}
                      alt="Original"
                      className="absolute inset-0 w-full h-full object-cover"
                    />
                    <img
                      src={result.gradcam_disease.overlay_base64}
                      alt="Disease GradCAM"
                      className="absolute inset-0 w-full h-full object-cover mix-blend-multiply opacity-60"
                      data-testid="img-gradcam-disease"
                    />
                  </div>
                  <p className="text-xs text-muted-foreground mt-2 text-center">
                    Red regions indicate areas the model used to classify: <strong>{result.skin_disease?.predicted_class}</strong>
                  </p>
                </div>
              )}

              {result.gradcam_concern && (
                <div>
                  <p className="text-sm font-medium mb-3">Concern Detection Focus</p>
                  <div className="relative rounded-xl overflow-hidden bg-muted/30 aspect-square">
                    <img
                      src={result.original_image_base64}
                      alt="Original"
                      className="absolute inset-0 w-full h-full object-cover"
                    />
                    <img
                      src={result.gradcam_concern.overlay_base64}
                      alt="Concern GradCAM"
                      className="absolute inset-0 w-full h-full object-cover mix-blend-multiply opacity-60"
                      data-testid="img-gradcam-concern"
                    />
                  </div>
                  <p className="text-xs text-muted-foreground mt-2 text-center">
                    Red regions indicate areas the model used to classify: <strong>{result.skin_concern?.predicted_class}</strong>
                  </p>
                </div>
              )}
            </div>
          </Card>
        </TabsContent>

        <TabsContent value="recommendations" className="space-y-6">
          {result.recommendation && (
            <>
              <Card className="p-6 border-border/50" data-testid="card-ingredients">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center">
                    <FlaskConical className="w-5 h-5 text-blue-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Recommended Active Ingredients</h3>
                    <p className="text-xs text-muted-foreground">Based on your skin type, condition, and concerns</p>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  {result.recommendation.active_ingredients.map((ing) => (
                    <Badge key={ing} variant="secondary" className="px-3 py-1.5 text-sm" data-testid={`badge-ingredient-${ing}`}>
                      {ing}
                    </Badge>
                  ))}
                </div>
              </Card>

              <div className="grid md:grid-cols-2 gap-5">
                <Card className="p-6 border-border/50" data-testid="card-morning-routine">
                  <div className="flex items-center gap-3 mb-5">
                    <div className="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center">
                      <Sun className="w-5 h-5 text-amber-500" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Morning Routine</h3>
                      <p className="text-xs text-muted-foreground">Your AM skincare protocol</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    {result.recommendation.morning_routine.map((step, i) => (
                      <div key={i} className="flex items-start gap-3">
                        <span className="w-6 h-6 rounded-full bg-amber-100 text-amber-700 text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                          {i + 1}
                        </span>
                        <span className="text-sm leading-relaxed">{step}</span>
                      </div>
                    ))}
                  </div>
                </Card>

                <Card className="p-6 border-border/50" data-testid="card-night-routine">
                  <div className="flex items-center gap-3 mb-5">
                    <div className="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center">
                      <Moon className="w-5 h-5 text-indigo-500" />
                    </div>
                    <div>
                      <h3 className="font-semibold">Night Routine</h3>
                      <p className="text-xs text-muted-foreground">Your PM treatment protocol</p>
                    </div>
                  </div>
                  <div className="space-y-3">
                    {result.recommendation.night_routine.map((step, i) => (
                      <div key={i} className="flex items-start gap-3">
                        <span className="w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                          {i + 1}
                        </span>
                        <span className="text-sm leading-relaxed">{step}</span>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>

              <Card className="p-6 border-border/50" data-testid="card-products">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center">
                    <ShoppingBag className="w-5 h-5 text-emerald-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Product Suggestions</h3>
                    <p className="text-xs text-muted-foreground">Recommended product types for your skin profile</p>
                  </div>
                </div>
                <div className="grid sm:grid-cols-2 gap-4">
                  {result.recommendation.product_suggestions.map((product, i) => (
                    <div key={i} className="p-4 rounded-xl bg-muted/30 border border-border/30">
                      <div className="flex items-center gap-2 mb-1.5">
                        <Badge variant="outline" className="text-xs">{product.type}</Badge>
                      </div>
                      <h4 className="font-medium text-sm mb-1">{product.name}</h4>
                      <p className="text-xs text-muted-foreground leading-relaxed">{product.description}</p>
                    </div>
                  ))}
                </div>
              </Card>

              <Card className="p-6 border-border/50" data-testid="card-lifestyle">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 rounded-xl bg-rose-50 flex items-center justify-center">
                    <Heart className="w-5 h-5 text-rose-500" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Lifestyle Tips</h3>
                    <p className="text-xs text-muted-foreground">Habits for healthier skin</p>
                  </div>
                </div>
                <div className="grid sm:grid-cols-2 gap-3">
                  {result.recommendation.lifestyle_tips.map((tip, i) => (
                    <div key={i} className="flex items-start gap-2 p-3 rounded-lg bg-muted/30">
                      <CheckCircle2 className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
                      <span className="text-sm leading-relaxed">{tip}</span>
                    </div>
                  ))}
                </div>
              </Card>
            </>
          )}
        </TabsContent>
      </Tabs>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mt-8"
      >
        <Card className="p-5 border-amber-200 bg-amber-50/30" data-testid="card-medical-disclaimer">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
              <Shield className="w-5 h-5 text-amber-600" />
            </div>
            <div>
              <h4 className="font-semibold text-sm text-amber-800 mb-1">Important Medical Disclaimer</h4>
              <p className="text-xs text-amber-700 leading-relaxed">
                These results are <strong>advisory and preliminary only</strong>. SkinLens is an AI-based tool developed for
                educational purposes and is <strong>not a substitute for professional medical advice, diagnosis, or treatment</strong>.
                Please consult a qualified dermatologist or healthcare professional before making any medical decisions
                based on these results.
              </p>
            </div>
          </div>
        </Card>
      </motion.div>
    </div>
  );
}

function handleExportReport(result: AnalysisResult) {
  const reportContent = generateTextReport(result);
  const blob = new Blob([reportContent], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `SkinLens_Report_${new Date().toISOString().slice(0, 10)}.txt`;
  a.click();
  URL.revokeObjectURL(url);
}

function generateTextReport(result: AnalysisResult): string {
  const lines: string[] = [];
  lines.push("=".repeat(60));
  lines.push("SkinLens - Skin Analysis Report");
  lines.push("=".repeat(60));
  lines.push(`Date: ${new Date(result.timestamp).toLocaleString()}`);
  lines.push(`Analysis Mode: ${result.mode}`);
  lines.push(`Status: ${result.overall_status}`);
  lines.push("");

  if (result.skin_type) {
    lines.push("-".repeat(40));
    lines.push("SKIN TYPE ANALYSIS");
    lines.push(`Predicted: ${result.skin_type.predicted_class}`);
    lines.push(`Confidence: ${Math.round(result.skin_type.confidence * 100)}%`);
    lines.push("All Predictions:");
    result.skin_type.all_predictions.forEach((p) => {
      lines.push(`  ${p.label}: ${Math.round(p.confidence * 100)}%`);
    });
    lines.push("");
  }

  if (result.skin_disease) {
    lines.push("-".repeat(40));
    lines.push("SKIN DISEASE DETECTION");
    lines.push(`Predicted: ${result.skin_disease.predicted_class}`);
    lines.push(`Confidence: ${Math.round(result.skin_disease.confidence * 100)}%`);
    lines.push("All Predictions:");
    result.skin_disease.all_predictions.forEach((p) => {
      lines.push(`  ${p.label}: ${Math.round(p.confidence * 100)}%`);
    });
    lines.push("");
  }

  if (result.skin_concern) {
    lines.push("-".repeat(40));
    lines.push("SKIN CONCERN DETECTION");
    lines.push(`Predicted: ${result.skin_concern.predicted_class}`);
    lines.push(`Confidence: ${Math.round(result.skin_concern.confidence * 100)}%`);
    lines.push("All Predictions:");
    result.skin_concern.all_predictions.forEach((p) => {
      lines.push(`  ${p.label}: ${Math.round(p.confidence * 100)}%`);
    });
    lines.push("");
  }

  if (result.recommendation) {
    lines.push("-".repeat(40));
    lines.push("RECOMMENDATIONS");
    lines.push("");
    lines.push("Active Ingredients:");
    result.recommendation.active_ingredients.forEach((ing) => {
      lines.push(`  - ${ing}`);
    });
    lines.push("");
    lines.push("Morning Routine:");
    result.recommendation.morning_routine.forEach((step, i) => {
      lines.push(`  ${i + 1}. ${step}`);
    });
    lines.push("");
    lines.push("Night Routine:");
    result.recommendation.night_routine.forEach((step, i) => {
      lines.push(`  ${i + 1}. ${step}`);
    });
    lines.push("");
    lines.push("Lifestyle Tips:");
    result.recommendation.lifestyle_tips.forEach((tip) => {
      lines.push(`  - ${tip}`);
    });
  }

  lines.push("");
  lines.push("=".repeat(60));
  lines.push("DISCLAIMER: This report is generated by SkinLens, an AI-based");
  lines.push("tool developed for educational purposes. Results are advisory");
  lines.push("and preliminary only. It is not a substitute for professional");
  lines.push("medical advice, diagnosis, or treatment. Please consult a");
  lines.push("qualified dermatologist for accurate diagnosis.");
  lines.push("=".repeat(60));

  return lines.join("\n");
}
