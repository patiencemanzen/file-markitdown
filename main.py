from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse
from app.converters import convert_html_to_format
from pydantic import BaseModel
import io

app = FastAPI()

class ConvertRequest(BaseModel):
    code: str  # HTML content as string
    output_format: str

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

@app.post("/convert-json/")
async def convert_from_json(request: ConvertRequest):
    if request.output_format not in ["markdown", "pdf", "docx"]:
        return {"error": "Unsupported format."}

    html_bytes = request.code.encode('utf-8')
    result = convert_html_to_format(html_bytes, request.output_format)

    return StreamingResponse(
        io.BytesIO(result["content"]),
        media_type=result["media_type"],
        headers={"Content-Disposition": f"attachment; filename={result['filename']}"}
    )
