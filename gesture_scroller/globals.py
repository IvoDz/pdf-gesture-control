import queue
import threading

gesture_queue = queue.Queue()

terminate = threading.Event()