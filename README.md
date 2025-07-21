# File MarkItDown API 🔄

A high-performance FastAPI backend service that converts HTML content to multiple formats (Markdown, PDF, DOCX) using Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library. Optimized for cloud deployment on platforms like Render.

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

## ✨ Features

- **Multiple Input Methods**: File upload, JSON payload, or form data
- **Three Output Formats**: Markdown, PDF, DOCX
- **Cloud-Optimized**: Designed for reliable deployment on Render, Heroku, etc.
- **Smart Formatting**: Preserves HTML structure, headers, code blocks, and styling
- **Robust Error Handling**: Graceful fallbacks ensure service reliability
- **Fast & Lightweight**: Minimal dependencies for quick cold starts

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/patiencemanzen/file-markitdown.git
   cd file-markitdown
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - API: http://127.0.0.1:8000
   - Interactive docs: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## 📡 API Endpoints

### 1. File Upload (`/convert/`)
Convert HTML files to your desired format.

**Request:**
```bash
curl -X POST "http://localhost:8000/convert/" \
     -F "file=@conversation.html" \
     -F "output_format=pdf"
```

**Form Data:**
- `file`: HTML file to convert
- `output_format`: `markdown` | `pdf` | `docx`

---

### 2. JSON Payload (`/convert-json/`)
Send HTML content as JSON for conversion.

**Request:**
```bash
curl -X POST "http://localhost:8000/convert-json/" \
     -H "Content-Type: application/json" \
     -d '{
       "code": "<html><body><h1>Hello World</h1><p>This is HTML content</p></body></html>",
       "output_format": "markdown"
     }'
```

**JSON Body:**
```json
{
  "code": "HTML content as string",
  "output_format": "markdown|pdf|docx"
}
```

---

### 3. Form Data (`/convert-form/`)
Send HTML content via form fields.

**Request:**
```bash
curl -X POST "http://localhost:8000/convert-form/" \
     -F "code=<html><body><h1>Title</h1><p>Content</p></body></html>" \
     -F "output_format=docx"
```

**Form Data:**
- `code`: HTML content as string
- `output_format`: `markdown` | `pdf` | `docx`

## 🎯 Use Cases

### ChatGPT Conversation Export
Perfect for converting ChatGPT conversation exports to readable formats:

```javascript
// Frontend integration example
const convertChatGPT = async (htmlContent) => {
  const response = await fetch('/convert-json/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code: htmlContent,
      output_format: 'pdf'
    })
  });
  
  if (response.ok) {
    const blob = await response.blob();
    // Download the converted file
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'conversation.pdf';
    a.click();
  }
};
```

### Document Processing Pipeline
Integrate into document processing workflows:

```python
import requests

def convert_html_document(html_content, format_type):
    response = requests.post(
        'https://your-api.onrender.com/convert-json/',
        json={
            'code': html_content,
            'output_format': format_type
        }
    )
    
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Conversion failed: {response.status_code}")

# Usage
pdf_content = convert_html_document(html_string, 'pdf')
with open('output.pdf', 'wb') as f:
    f.write(pdf_content)
```

## 🏗️ Architecture

### Conversion Pipeline

```
HTML Input → Parser → Format Processor → Output
     ↓          ↓           ↓              ↓
File/JSON → BeautifulSoup → FPDF/Docx → Binary Response
```

### PDF Generation Strategy
1. **Enhanced FPDF + html2text** (Primary) - Cloud-optimized
2. **Basic FPDF + BeautifulSoup** (Fallback) - Always reliable
3. **Error PDF** (Last resort) - Prevents service crashes

### DOCX Generation Strategy
1. **python-docx + BeautifulSoup** (Primary) - Rich formatting
2. **MarkItDown + basic DOCX** (Fallback) - Simple conversion
3. **Error DOCX** (Last resort) - Service reliability

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Customize server settings
PORT=8000
HOST=0.0.0.0
WORKERS=1
```

### Production Deployment (Render)
```bash
# Build Command
pip install -r requirements.txt

# Start Command
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 📦 Dependencies

**Core:**
- `fastapi` - Modern web framework
- `uvicorn[standard]` - ASGI server
- `python-multipart` - File upload support

**Conversion:**
- `markitdown[all]` - Microsoft's HTML processor
- `python-docx` - DOCX generation
- `fpdf` - PDF creation
- `html2text` - HTML to Markdown
- `beautifulsoup4` - HTML parsing

## 🧪 Testing

### Manual Testing
Use the interactive API docs at `/docs` for testing:

1. Navigate to http://localhost:8000/docs
2. Expand any endpoint
3. Click "Try it out"
4. Upload file or paste HTML content
5. Execute and download result

### Sample HTML for Testing
```html
<!DOCTYPE html>
<html>
<head>
    <title>Test Document</title>
</head>
<body>
    <h1>Main Title</h1>
    <h2>Subtitle</h2>
    <p>This is a <strong>paragraph</strong> with <em>formatting</em>.</p>
    <blockquote>This is a quote</blockquote>
    <pre><code>console.log('This is code');</code></pre>
    <ul>
        <li>List item 1</li>
        <li>List item 2</li>
    </ul>
</body>
</html>
```

## 🚀 Deployment

### Deploy to Render
1. Fork this repository
2. Connect to Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Deploy!

### Deploy to Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
```

### Deploy with Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 Performance

- **Cold Start**: < 2 seconds
- **Conversion Time**: 
  - Markdown: ~100ms
  - PDF: ~500ms-1s
  - DOCX: ~300ms-800ms
- **Memory Usage**: ~50-100MB per conversion
- **Concurrent Requests**: Supports multiple simultaneous conversions

## 🛠️ Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) - Core conversion engine
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [FPDF](http://www.fpdf.org/) - PDF generation
- [python-docx](https://python-docx.readthedocs.io/) - DOCX creation

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/patiencemanzen/file-markitdown/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/patiencemanzen/file-markitdown/discussions)
- 📧 **Contact**: hseal419@gmail.com

---

<div align="center">
  <strong>Made with ❤️ by Manirabona for Document conversion</strong>
</div>
