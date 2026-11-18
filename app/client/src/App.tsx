import { Switch, Route, Router as WouterRouter } from "wouter";
import { IS_DEMO, BASE } from "@/lib/demo";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/not-found";
import LandingPage from "@/pages/landing";
import AnalyzePage from "@/pages/analyze";
import AboutPage from "@/pages/about";

function Router() {
  return (
    <Switch>
      <Route path="/" component={LandingPage} />
      <Route path="/analyze" component={AnalyzePage} />
      <Route path="/about" component={AboutPage} />
      <Route component={NotFound} />
    </Switch>
  );
}

function DemoBanner() {
  return (
    <div
      className="fixed bottom-4 left-1/2 -translate-x-1/2 z-[100] max-w-[92vw] rounded-full bg-slate-900/90 text-white text-xs sm:text-sm px-4 py-2 shadow-lg backdrop-blur"
      data-testid="demo-banner"
    >
      Demo mode: results are pre-computed with the real models for a sample image.{" "}
      <a
        className="underline font-medium"
        href="https://github.com/zehraeraslan/SkinLens"
        target="_blank"
        rel="noreferrer"
      >
        Run it locally for live analysis
      </a>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <WouterRouter base={BASE.replace(/\/$/, "")}>
          <Router />
        </WouterRouter>
        {IS_DEMO && <DemoBanner />}
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
