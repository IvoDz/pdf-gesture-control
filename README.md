# Gesture-Enabled PDF Reader

Simple gesture-controlled PDF reader, that allows to navigate through PDFs using hand gestures. 

### Prerequisites

Before you begin, ensure you have:
- Python 3.11
- Poetry
- Webcam

### Installation

1. **Clone the repository:**
  
  ```bash
  git clone https://github.com/IvoDz/pdf-gesture-control.git
  cd pdf-gesture-control
  ```

2. **Install dependencies:**

  ```bash
  poetry install
  ```

### Running the Application

To run the application, execute:
    
  ```bash
  python main.py
  ```

## Usage

After PDF is opened, make sure you are sitting in front of the webcam. Now use gestures:
- Opened fist (✋), to go to the **next** page 
- Closed fist (✊), to go to the **previous** page

To exit, use 🤘 or ✌️, or simply close the reader.

## Built With
- [OpenCV](https://opencv.org/) 
- [MediaPipe](https://mediapipe.dev/) 
- [PyMuPDF](https://pymupdf.readthedocs.io/) 

