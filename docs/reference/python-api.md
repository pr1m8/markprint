# Python API

```python
from markprint import RenderOptions, render_pdf, render_html, render_pdf_bytes

render_pdf(markdown="# Hello", output="hello.pdf")
document = render_html(markdown="# Hello")
pdf_bytes = render_pdf_bytes(markdown="# Hello")
```
