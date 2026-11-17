from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.api.routes import router as api_router
from app.config import get_settings
from app.core.model_loader import get_model_registry
from app.services.report_service import build_pdf_report


settings = get_settings()

app = FastAPI(title=settings.project_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def preload_models() -> None:
    import threading
    def _load():
        try:
            get_model_registry().load_models()
            print("All models loaded successfully.")
        except Exception as e:
            print(f"Model loading error (will retry on first request): {e}")
    threading.Thread(target=_load, daemon=True).start()


app.include_router(api_router, prefix=settings.api_prefix)


@app.post(f"{settings.api_prefix}/report")
async def generate_report(payload: dict) -> StreamingResponse:
    """
    Generate a PDF report from a previously obtained analysis payload.
    Frontend sends the full /analyze JSON payload and optional original image (base64).
    """
    uploaded_image_b64 = payload.get("uploaded_image_base64")
    pdf_bytes = build_pdf_report(uploaded_image_b64, payload)
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="SkinLens_Report.pdf"'},
    )


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

