from gesture_capturer import capture
from pdf_viewer import PDFViewer
import threading
import sys
from fitz import FileNotFoundError

if __name__ == "__main__":
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else "sample.pdf"
    try:
        viewer = PDFViewer(pdf_path)
    except FileNotFoundError:
        print("PDF file not found!")
        sys.exit(1)

    capturer_thread = threading.Thread(target=capture)
    capturer_thread.start()

    viewer.run()

    capturer_thread.join()
