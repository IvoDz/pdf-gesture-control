import mediapipe as mp
import time
import cv2
from pdf_viewer import PDFViewer
from global_gesture import gesture_queue

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

video = cv2.VideoCapture(0)
terminate_capture = False

def process_gesture(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global terminate_capture, current_gesture
    scrollable_gestures = ("Closed_Fist", "Open_Palm")
    termination_gestures = ("ILoveYou", "Victory") 
    
    try:
        gesture = result.gestures[0][0].category_name
        print(f"Detected gesture: {gesture}")
        if gesture in scrollable_gestures:
            gesture_queue.put(gesture)
        if gesture in termination_gestures:
            print("Exiting...")
            terminate_capture = True
        else:
            return None
    except IndexError:
        return None

def capture():
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=process_gesture)

    timestamp = 0
    last_check_time = time.time() 
    with GestureRecognizer.create_from_options(options) as recognizer:
        while video.isOpened(): 
            if terminate_capture: break
            
            ret, frame = video.read()

            if not ret:
                print("Ignoring empty frame")
                break

            current_time = time.time()
            if current_time - last_check_time >= 2:  
                timestamp += 1
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                recognizer.recognize_async(mp_image, timestamp)
                last_check_time = current_time 
                
            if cv2.waitKey(5) & 0xFF == 27:
                break

    video.release()
    cv2.destroyAllWindows()
