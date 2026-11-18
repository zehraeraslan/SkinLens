// Static "demo mode" (GitHub Pages): no server, results are pre-computed with the real models
// for one sample image. Enabled at build time with VITE_DEMO=true.
export const IS_DEMO = import.meta.env.VITE_DEMO === "true";
export const BASE: string = import.meta.env.BASE_URL;
