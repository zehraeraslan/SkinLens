import { Link } from "wouter";
import { motion } from "framer-motion";
import {
  Sparkles,
  Shield,
  Microscope,
  Brain,
  ArrowRight,
  Eye,
  Layers,
  ChevronRight,
  Stethoscope,
  FlaskConical,
  FileText,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { SkinLensLogo } from "@/components/skinlens-logo";

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.6, ease: [0.22, 1, 0.36, 1] },
  }),
};

const features = [
  {
    icon: Brain,
    title: "Deep Learning Models",
    description: "Three specialized deep learning models (DenseNet121 and EfficientNetB0) trained on dermatological datasets for skin type, disease, and concern detection.",
    color: "text-blue-500",
    bg: "bg-blue-50",
  },
  {
    icon: Eye,
    title: "Explainable AI",
    description: "Grad-CAM heatmap visualizations show exactly which regions of your skin the AI focuses on for its predictions.",
    color: "text-emerald-500",
    bg: "bg-emerald-50",
  },
  {
    icon: Shield,
    title: "Confidence Threshold",
    description: "Built-in reliability checks ensure predictions meet a 70% confidence threshold before delivering results.",
    color: "text-amber-500",
    bg: "bg-amber-50",
  },
  {
    icon: FlaskConical,
    title: "Smart Recommendations",
    description: "Personalized skincare routines and ingredient suggestions based on your unique skin profile combination.",
    color: "text-violet-500",
    bg: "bg-violet-50",
  },
];

const analysisCards = [
  {
    icon: Layers,
    title: "Full Skin Analysis",
    description: "Complete analysis covering skin type, diseases, and concerns in one scan.",
    mode: "full",
    gradient: "from-blue-500 to-cyan-400",
  },
  {
    icon: Sparkles,
    title: "Skin Type Analysis",
    description: "Determine if your skin is dry, normal, oily, or sensitive.",
    mode: "skin_type",
    gradient: "from-emerald-500 to-teal-400",
  },
  {
    icon: Stethoscope,
    title: "Disease Detection",
    description: "Screen for conditions including acne, atopic dermatitis, benign lesions, melanoma, and fungal infections.",
    mode: "disease",
    gradient: "from-orange-500 to-amber-400",
  },
  {
    icon: Microscope,
    title: "Concern Detection",
    description: "Identify skin concerns such as acne, blackheads, enlarged pores, and wrinkles.",
    mode: "concern",
    gradient: "from-violet-500 to-purple-400",
  },
];

const stats = [
  { value: "3", label: "AI Models" },
  { value: "13", label: "Skin Classes" },
  { value: "70%", label: "Confidence Threshold" },
  { value: "224x224", label: "Image Resolution" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background" data-testid="landing-page">
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border/50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2.5">
            <SkinLensLogo size={32} />
            <span className="font-semibold text-lg tracking-tight">SkinLens</span>
          </Link>
          <div className="hidden md:flex items-center gap-8">
            <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors" data-testid="nav-home">Home</Link>
            <Link href="/analyze" className="text-sm text-muted-foreground hover:text-foreground transition-colors" data-testid="nav-analyze">Analyze</Link>
            <Link href="/about" className="text-sm text-muted-foreground hover:text-foreground transition-colors" data-testid="nav-about">About</Link>
          </div>
          <Link href="/analyze">
            <Button size="sm" data-testid="nav-start-btn">
              Start Analysis
              <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </Link>
        </div>
      </nav>

      <section className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            className="max-w-3xl mx-auto text-center"
            initial="hidden"
            animate="visible"
            variants={{
              visible: { transition: { staggerChildren: 0.1 } },
            }}
          >
            <motion.div variants={fadeUp} custom={0}>
              <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-600 border border-blue-100 mb-6">
                <Sparkles className="w-3.5 h-3.5" />
                Graduation Project
              </span>
            </motion.div>

            <motion.h1
              variants={fadeUp}
              custom={1}
              className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight leading-[1.1] mb-6"
            >
              AI-Powered{" "}
              <span className="bg-gradient-to-r from-blue-600 via-cyan-500 to-teal-400 bg-clip-text text-transparent">
                Dermatological
              </span>
              <br />
              Skin Analysis
            </motion.h1>

            <motion.p
              variants={fadeUp}
              custom={2}
              className="text-lg text-muted-foreground max-w-2xl mx-auto mb-10 leading-relaxed"
            >
              Upload a facial skin image and receive instant analysis powered by
              three specialized deep learning models. Get personalized skincare
              recommendations backed by AI explainability.
            </motion.p>

            <motion.div variants={fadeUp} custom={3} className="flex items-center justify-center gap-4">
              <Link href="/analyze">
                <Button size="lg" className="h-12 px-8 text-base" data-testid="hero-start-btn">
                  Start Free Analysis
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </Link>
              <Link href="/about">
                <Button variant="outline" size="lg" className="h-12 px-8 text-base" data-testid="hero-learn-btn">
                  Learn More
                </Button>
              </Link>
            </motion.div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
            className="mt-20 max-w-4xl mx-auto"
          >
            <div className="relative rounded-2xl overflow-hidden bg-gradient-to-br from-blue-500/5 via-cyan-500/5 to-teal-500/5 border border-border/50 p-8 sm:p-12">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(59,130,246,0.08),transparent_50%)]" />
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(20,184,166,0.06),transparent_50%)]" />
              <div className="relative grid grid-cols-2 sm:grid-cols-4 gap-6">
                {stats.map((stat, i) => (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.7 + i * 0.1 }}
                    className="text-center"
                  >
                    <div className="text-3xl sm:text-4xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent">
                      {stat.value}
                    </div>
                    <div className="text-sm text-muted-foreground mt-1">{stat.label}</div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      <section className="py-20 px-6 bg-card/30">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl font-bold tracking-tight mb-4">Platform Features</h2>
            <p className="text-muted-foreground max-w-lg mx-auto">
              Built on cutting-edge deep learning technology for accurate and explainable skin analysis.
            </p>
          </motion.div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <Card className="p-6 h-full border-border/50 hover:border-border transition-colors" data-testid={`feature-card-${i}`}>
                  <div className={`w-10 h-10 rounded-lg ${feature.bg} flex items-center justify-center mb-4`}>
                    <feature.icon className={`w-5 h-5 ${feature.color}`} />
                  </div>
                  <h3 className="font-semibold mb-2">{feature.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {feature.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl font-bold tracking-tight mb-4">Analysis Modes</h2>
            <p className="text-muted-foreground max-w-lg mx-auto">
              Choose the analysis type that best fits your needs, from comprehensive to targeted screening.
            </p>
          </motion.div>

          <div className="grid sm:grid-cols-2 gap-5 max-w-4xl mx-auto">
            {analysisCards.map((card, i) => (
              <motion.div
                key={card.mode}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
              >
                <Link href={`/analyze?mode=${card.mode}`}>
                  <Card
                    className="p-6 cursor-pointer group border-border/50 hover:border-border hover:shadow-md transition-all"
                    data-testid={`mode-card-${card.mode}`}
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className={`w-11 h-11 rounded-xl bg-gradient-to-br ${card.gradient} flex items-center justify-center shadow-sm`}>
                        <card.icon className="w-5.5 h-5.5 text-white" />
                      </div>
                      <ChevronRight className="w-5 h-5 text-muted-foreground/50 group-hover:text-foreground group-hover:translate-x-0.5 transition-all" />
                    </div>
                    <h3 className="font-semibold text-lg mb-1.5">{card.title}</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {card.description}
                    </p>
                  </Card>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-6 bg-card/30">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl font-bold tracking-tight mb-4">How It Works</h2>
            <p className="text-muted-foreground max-w-lg mx-auto">
              Three simple steps to get your comprehensive skin analysis report.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {[
              {
                step: "01",
                title: "Upload Image",
                description: "Take or upload a clear facial skin photo in JPEG or PNG format.",
                icon: FileText,
              },
              {
                step: "02",
                title: "AI Analysis",
                description: "Our deep learning models analyze your image across multiple dimensions simultaneously.",
                icon: Brain,
              },
              {
                step: "03",
                title: "Get Results",
                description: "Receive detailed predictions, confidence scores, heatmaps, and personalized recommendations.",
                icon: Eye,
              },
            ].map((item, i) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="text-center"
              >
                <div className="relative inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/10 to-cyan-500/10 mb-5">
                  <item.icon className="w-7 h-7 text-blue-500" />
                  <span className="absolute -top-2 -right-2 w-7 h-7 rounded-full bg-blue-500 text-white text-xs font-bold flex items-center justify-center">
                    {item.step}
                  </span>
                </div>
                <h3 className="font-semibold text-lg mb-2">{item.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl font-bold tracking-tight mb-4">
              Ready to Analyze Your Skin?
            </h2>
            <p className="text-muted-foreground mb-8 max-w-lg mx-auto">
              Get started with a free analysis today. Upload your photo and let our AI provide personalized insights.
            </p>
            <Link href="/analyze">
              <Button size="lg" className="h-12 px-10 text-base" data-testid="cta-start-btn">
                Start Analysis Now
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </Link>
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
