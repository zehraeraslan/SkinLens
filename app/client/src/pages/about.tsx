import { Link } from "wouter";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Brain,
  Database,
  Layers,
  Microscope,
  Shield,
  Cpu,
  BarChart3,
  Eye,
  Sparkles,
  GraduationCap,
  User,
  AlertTriangle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { SkinLensLogo } from "@/components/skinlens-logo";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.5 },
  }),
};

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-background" data-testid="about-page">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <SkinLensLogo size={32} />
            <span className="font-semibold text-lg tracking-tight">SkinLens</span>
          </Link>
          <div className="hidden md:flex items-center gap-8">
            <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Home</Link>
            <Link href="/analyze" className="text-sm text-muted-foreground hover:text-foreground transition-colors">Analyze</Link>
            <Link href="/about" className="text-sm text-foreground font-medium transition-colors">About</Link>
          </div>
          <Link href="/analyze">
            <Button size="sm" data-testid="nav-start-btn">
              Start Analysis
              <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </Link>
        </div>
      </nav>

      <section className="pt-32 pb-16 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div initial="hidden" animate="visible" variants={{ visible: { transition: { staggerChildren: 0.1 } } }}>
            <motion.span variants={fadeUp} custom={0} className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-violet-50 text-violet-600 border border-violet-100 mb-6">
              <Microscope className="w-3.5 h-3.5" />
              About SkinLens
            </motion.span>
            <motion.h1 variants={fadeUp} custom={1} className="text-4xl sm:text-5xl font-bold tracking-tight mb-6">
              About the{" "}
              <span className="bg-gradient-to-r from-violet-600 to-blue-500 bg-clip-text text-transparent">Project</span>
            </motion.h1>
            <motion.p variants={fadeUp} custom={2} className="text-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              SkinLens is an AI-powered dermatological analysis platform developed as a graduation project,
              combining deep learning with clinical dermatology for accessible skin health assessment.
            </motion.p>
          </motion.div>
        </div>
      </section>

      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
            <Card className="p-8 border-border/50" data-testid="card-developer">
              <div className="flex items-start gap-5">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center flex-shrink-0">
                  <User className="w-7 h-7 text-white" />
                </div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-xl font-semibold">Zehra Eraslan</h3>
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-600 border border-blue-100">
                      <GraduationCap className="w-3 h-3" />
                      Developer
                    </span>
                  </div>
                  <p className="text-muted-foreground leading-relaxed mt-3">
                    Hello, my name is Zehra Eraslan. I am a senior Computer Engineering student at Uskudar University
                    and currently pursuing a double major in Software Engineering. This website was developed as part
                    of my Software Engineering graduation project. The goal of this project is to apply my academic
                    knowledge in software development and artificial intelligence to create a practical and
                    user-friendly system.
                  </p>
                </div>
              </div>
            </Card>
          </motion.div>
        </div>
      </section>

      <section className="py-16 px-6 bg-card/30">
        <div className="max-w-5xl mx-auto">
          <div className="grid md:grid-cols-2 gap-8">
            <motion.div initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}>
              <Card className="p-8 h-full border-border/50">
                <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-5">
                  <Brain className="w-6 h-6 text-blue-500" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Model Architecture</h3>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  The system uses three specialized models: a hybrid DenseNet121 + LBP skin type classifier, a DenseNet121 disease classifier and an EfficientNetB0 skin concern classifier, each fine-tuned for a specific dermatological task.
                  DenseNet121 and EfficientNetB0 are pretrained on ImageNet and offer a good balance of accuracy and computational efficiency. The disease model was trained on dermoscopic and clinical images of various body sites, not on facial photographs.
                </p>
                <div className="space-y-3">
                  {[
                    { label: "Skin Type Model", file: "best_hybrid_model.h5", classes: "4 classes" },
                    { label: "Disease Model", file: "focal_finetuned_skin_model.keras", classes: "5 classes" },
                    { label: "Concern Model", file: "skin_concern_final_model.keras", classes: "4 classes" },
                  ].map((model) => (
                    <div key={model.label} className="flex items-center justify-between py-2 px-3 rounded-lg bg-muted/50">
                      <span className="text-sm font-medium">{model.label}</span>
                      <span className="text-xs text-muted-foreground">{model.classes}</span>
                    </div>
                  ))}
                </div>
              </Card>
            </motion.div>

            <motion.div initial={{ opacity: 0, x: 20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }}>
              <Card className="p-8 h-full border-border/50">
                <div className="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center mb-5">
                  <Layers className="w-6 h-6 text-emerald-500" />
                </div>
                <h3 className="text-xl font-semibold mb-3">Classification Targets</h3>
                <div className="space-y-5">
                  <div>
                    <h4 className="text-sm font-medium mb-2 text-blue-600">Skin Types</h4>
                    <div className="flex flex-wrap gap-1.5">
                      {["Dry", "Normal", "Oily", "Sensitive"].map((t) => (
                        <span key={t} className="px-2.5 py-1 text-xs rounded-full bg-blue-50 text-blue-700 border border-blue-100">{t}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium mb-2 text-orange-600">Skin Diseases</h4>
                    <div className="flex flex-wrap gap-1.5">
                      {["Acne", "Atopic Dermatitis", "Benign Lesion", "Melanoma", "Tinea Ringworm Candidiasis"].map((t) => (
                        <span key={t} className="px-2.5 py-1 text-xs rounded-full bg-orange-50 text-orange-700 border border-orange-100">{t}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="text-sm font-medium mb-2 text-violet-600">Skin Concerns</h4>
                    <div className="flex flex-wrap gap-1.5">
                      {["Acne", "Blackheads", "Pores", "Wrinkles"].map((t) => (
                        <span key={t} className="px-2.5 py-1 text-xs rounded-full bg-violet-50 text-violet-700 border border-violet-100">{t}</span>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>
            </motion.div>
          </div>
        </div>
      </section>

      <section className="py-16 px-6">
        <div className="max-w-5xl mx-auto">
          <motion.h2 initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} className="text-2xl font-bold tracking-tight mb-10 text-center">
            System Pipeline
          </motion.h2>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {[
              { icon: Database, title: "Image Upload", description: "Validated file upload with format and size checks", color: "text-blue-500", bg: "bg-blue-50" },
              { icon: Cpu, title: "Preprocessing", description: "Resize to 224x224, normalize pixels, convert to tensor", color: "text-emerald-500", bg: "bg-emerald-50" },
              { icon: BarChart3, title: "Inference", description: "Parallel model execution with confidence thresholds", color: "text-orange-500", bg: "bg-orange-50" },
              { icon: Eye, title: "Explainability", description: "Grad-CAM heatmap generation for model interpretability", color: "text-violet-500", bg: "bg-violet-50" },
            ].map((item, i) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <Card className="p-5 h-full border-border/50 text-center">
                  <div className={`w-10 h-10 rounded-lg ${item.bg} flex items-center justify-center mx-auto mb-3`}>
                    <item.icon className={`w-5 h-5 ${item.color}`} />
                  </div>
                  <h3 className="font-semibold mb-1.5">{item.title}</h3>
                  <p className="text-xs text-muted-foreground leading-relaxed">{item.description}</p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 px-6 bg-card/30">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
            <Card className="p-8 border-border/50">
              <div className="flex items-start gap-4 mb-6">
                <div className="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center flex-shrink-0">
                  <Shield className="w-6 h-6 text-amber-500" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">Confidence & Reliability</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    The platform implements a strict confidence threshold system. If the maximum confidence score
                    from the disease or concern model falls below <strong>70%</strong>, the system flags the result
                    as low-confidence and prompts the user to upload a clearer image. This ensures clinical-grade
                    reliability in predictions.
                  </p>
                </div>
              </div>
              <div className="grid sm:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl bg-green-50 border border-green-100 text-center">
                  <div className="text-2xl font-bold text-green-600 mb-1">{"\u2265"} 70%</div>
                  <div className="text-xs text-green-700">Confident Result</div>
                </div>
                <div className="p-4 rounded-xl bg-amber-50 border border-amber-100 text-center">
                  <div className="text-2xl font-bold text-amber-600 mb-1">&lt; 70%</div>
                  <div className="text-xs text-amber-700">Retry Requested</div>
                </div>
                <div className="p-4 rounded-xl bg-blue-50 border border-blue-100 text-center">
                  <div className="text-2xl font-bold text-blue-600 mb-1">13 Classes</div>
                  <div className="text-xs text-blue-700">Across 3 Models</div>
                </div>
              </div>
            </Card>
          </motion.div>
        </div>
      </section>

      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
            <Card className="p-8 border-border/50">
              <div className="flex items-start gap-4 mb-6">
                <div className="w-12 h-12 rounded-xl bg-violet-50 flex items-center justify-center flex-shrink-0">
                  <Sparkles className="w-6 h-6 text-violet-500" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2">Recommendation Engine</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    The platform features a logic-based recommendation engine that combines skin type, disease, and concern
                    predictions to generate personalized skincare advice. The engine produces targeted active ingredients,
                    morning and evening routines, product suggestions, and lifestyle tips.
                  </p>
                </div>
              </div>
              <div className="grid sm:grid-cols-2 gap-4">
                {[
                  { title: "Active Ingredients", desc: "Targeted actives based on your skin profile" },
                  { title: "Morning Routine", desc: "Step-by-step AM skincare protocol" },
                  { title: "Night Routine", desc: "Step-by-step PM treatment protocol" },
                  { title: "Lifestyle Tips", desc: "Holistic habits for skin health" },
                ].map((item) => (
                  <div key={item.title} className="p-3 rounded-lg bg-muted/50">
                    <div className="text-sm font-medium mb-0.5">{item.title}</div>
                    <div className="text-xs text-muted-foreground">{item.desc}</div>
                  </div>
                ))}
              </div>
            </Card>
          </motion.div>
        </div>
      </section>

      <section className="py-16 px-6 bg-card/30">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
            <Card className="p-8 border-amber-200 bg-amber-50/30" data-testid="card-disclaimer">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
                  <AlertTriangle className="w-6 h-6 text-amber-600" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2 text-amber-800">Important Disclaimer</h3>
                  <p className="text-amber-700 leading-relaxed mb-3">
                    This platform is designed for educational and research purposes as a graduation project.
                    The analysis results provided by SkinLens are <strong>advisory and preliminary only</strong>.
                  </p>
                  <p className="text-amber-700 leading-relaxed">
                    SkinLens is <strong>not intended to replace professional medical advice, diagnosis, or treatment</strong>.
                    The results should not be used as the sole basis for any medical decisions. Always consult a
                    qualified dermatologist or healthcare professional for accurate diagnosis and treatment recommendations.
                  </p>
                </div>
              </div>
            </Card>
          </motion.div>
        </div>
      </section>

      <footer className="border-t border-border/50 py-10 px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <SkinLensLogo size={24} />
            <span className="text-sm font-medium">SkinLens</span>
          </div>
          <p className="text-xs text-muted-foreground">
            Graduation Project · For educational and research purposes only · Not a substitute for professional medical advice
          </p>
        </div>
      </footer>
    </div>
  );
}
