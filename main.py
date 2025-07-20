from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse
from app.converters import convert_html_to_format
import io

app = FastAPI()

@app.post("/convert/")
async def convert_file(
    file: UploadFile,
    output_format: str = Form(...)
):
    if output_format not in ["markdown", "pdf", "docx"]:
        return {"error": "Unsupported format."}

    html_bytes = await file.read()
    result = convert_html_to_format(html_bytes, output_format)

    return StreamingResponse(
        io.BytesIO(result["content"]),
        media_type=result["media_type"],
        headers={"Content-Disposition": f"attachment; filename={result['filename']}"}
    )
