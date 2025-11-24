import cv2  # type: ignore
import numpy as np  # type: ignore
import time
import sys
import os

VIDEO_PATH = "videos/video.mp4"

ASCII_CHARS = np.array(list(" .:-=+*#%@"))

def get_terminal_size():
    size = os.get_terminal_size()
    return size.columns, size.lines - 2  # ajusta altura para caber

def frame_to_ascii(frame, width, height, color=True):
    frame = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    norm = gray / 255.0
    idx = (norm * (len(ASCII_CHARS) - 1)).astype(np.int32)

    ascii_lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            char = ASCII_CHARS[idx[y, x]]
            if color:
                b, g, r = frame[y, x]
                line += f"\x1b[38;2;{r};{g};{b}m{char}"
            else:
                line += char
        ascii_lines.append(line + ("\x1b[0m" if color else ""))
    return "\n".join(ascii_lines)

def clear_terminal():
    print("\033[H", end="")  # move o cursor para o topo

def main():
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"Erro ao abrir vídeo: {VIDEO_PATH}")
        return

    FPS = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = 1.0 / FPS

    term_width, term_height = get_terminal_size()

    while True:
        t0 = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        ascii_art = frame_to_ascii(frame, term_width, term_height, color=True)
        clear_terminal()
        print(ascii_art)
        sys.stdout.flush()

        dt = time.time() - t0
        if dt < frame_delay:
            time.sleep(frame_delay - dt)

    cap.release()

if __name__ == "__main__":
    main()
