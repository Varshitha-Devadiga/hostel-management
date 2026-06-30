from app import create_app
from app.auth.routes import verify_document_ocr
import os

app = create_app()

with app.app_context():
    # The file from the URL: http://127.0.0.1:5000/static/uploads/Screenshot_2025-06-03_095649.png
    file_path = os.path.join(app.root_path, '..', 'static', 'uploads', 'Screenshot_2025-06-03_095649.png')
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        class DummyFile:
            def __init__(self, path):
                self.path = path
                self.filename = os.path.basename(path)
                self.f = open(path, 'rb')
            def seek(self, pos):
                self.f.seek(pos)
            def read(self, *args):
                return self.f.read(*args)
            def __getattr__(self, name):
                return getattr(self.f, name)
                
        df = DummyFile(file_path)
        # Expected number from the screenshot: 935242975860
        result, msg = verify_document_ocr(df, "Aadhaar Card", "935242975860")
        print(f"Result: {result}")
        print(f"Message: {msg}")
        df.f.close()
