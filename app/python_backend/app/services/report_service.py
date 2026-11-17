from __future__ import annotations

import base64
import io
from typing import Dict, Optional

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


def _draw_multiline(c: canvas.Canvas, text: str, x: float, y: float, max_width: float) -> float:
    for line in text.split("\n"):
        c.drawString(x, y, line)
        y -= 5 * mm
    return y


def build_pdf_report(
    uploaded_image_b64: Optional[str],
    analysis_payload: Dict,
) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 20 * mm
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, y, "SkinLens Skin Analysis Report")
    y -= 15 * mm

    c.setFont("Helvetica", 11)
    status = analysis_payload.get("global_status")
    mode = analysis_payload.get("mode")
    c.drawString(20 * mm, y, f"Mode: {mode}   Status: {status}")
    y -= 10 * mm

    # Uploaded image (if provided)
    if uploaded_image_b64 and uploaded_image_b64.startswith("data:image"):
        try:
            header, b64 = uploaded_image_b64.split(",", 1)
            img_data = base64.b64decode(b64)
            img_reader = ImageReader(io.BytesIO(img_data))
            c.drawImage(
                img_reader,
                20 * mm,
                y - 60 * mm,
                width=50 * mm,
                preserveAspectRatio=True,
                mask="auto",
            )
        except Exception:
            pass

    y -= 70 * mm

    def block(title: str, node: Optional[Dict]) -> float:
        nonlocal y
        if node is None:
            return y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20 * mm, y, title)
        y -= 7 * mm
        c.setFont("Helvetica", 11)
        line = f"Prediction: {node.get('label')} (confidence {node.get('confidence'):.2f})"
        y = _draw_multiline(c, line, 22 * mm, y, width - 40 * mm)
        return y - 5 * mm

    y = block("Skin Type", analysis_payload.get("skin_type"))
    y = block("Skin Disease", analysis_payload.get("skin_disease"))
    y = block("Skin Concern", analysis_payload.get("skin_concern"))

    rec = analysis_payload.get("recommendation")
    if rec is not None:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20 * mm, y, "Recommendations")
        y -= 7 * mm
        c.setFont("Helvetica", 11)
        lines = []
        if rec.get("active_ingredients"):
            lines.append("Active Ingredients: " + ", ".join(rec["active_ingredients"]))
        if rec.get("morning_routine"):
            lines.append("Morning routine:")
            lines += [f" - {s}" for s in rec["morning_routine"]]
        if rec.get("night_routine"):
            lines.append("Night routine:")
            lines += [f" - {s}" for s in rec["night_routine"]]
        if rec.get("tips"):
            lines.append("Tips:")
            lines += [f" - {s}" for s in rec["tips"]]
        y = _draw_multiline(c, "\n".join(lines), 22 * mm, y, width - 40 * mm)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

