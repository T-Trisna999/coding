import time
from threading import Thread, Lock
import sys

lock = Lock()

COLOR_MAP = {
    '💘': (255, 0, 0),
    '🍂': (84, 44, 44),
    '💫': (255, 255, 5),
    '🙍': (255, 127, 5),
    '💞': (255, 65, 210),
    '😍': (255, 65, 210),
    '💖': (221, 125, 5),
    '🌍': (0, 253, 255),
    '🕺': (0, 253, 1),
    '😆': (255, 65, 210),
}

def get_target_color(text):
    for c in reversed(text):
        if c in COLOR_MAP:
            return COLOR_MAP[c]
    return (255, 255, 255)

def animate_text(text, delay=0.1):
    with lock:
        text = text.strip('\n')
        target_color = get_target_color(text)
        total_chars = len(text)
        start_time = time.time()

        # Simpan posisi kursor
        sys.stdout.write("\0337")
        sys.stdout.flush()

        while True:
            elapsed = time.time() - start_time
            current_char = int(elapsed // delay)

            if current_char >= total_chars:
                break

            line = []
            for i in range(current_char + 1):
                time_since = max(elapsed - i*delay, 0)
                ratio = time_since / (total_chars*delay - i*delay)
                ratio = max(0, min(ratio, 1))

                r = int(255 - (255 - target_color[0]) * ratio)
                g = int(255 - (255 - target_color[1]) * ratio)
                b = int(255 - (255 - target_color[2]) * ratio)

                line.append(f"\033[38;2;{r};{g};{b}m{text[i]}\033[0m")

            # Hapus baris lalu gambar ulang
            sys.stdout.write("\0338\033[2K")
            sys.stdout.write("".join(line))
            sys.stdout.flush()
            time.sleep(delay/10)

        # Tampilkan hasil akhir dengan jarak
        sys.stdout.write("\0338\033[2K")
        sys.stdout.write("".join([
            f"\033[38;2;{target_color[0]};{target_color[1]};{target_color[2]}m{c}\033[0m"
            for c in text
        ]) + "\n")
        sys.stdout.flush()

def sing_lyric(lyric, delay):
    time.sleep(delay)
    animate_text(lyric)

def sing_song():
    lyrics = [
        ("\nWe fell in love in October 💘", 1.3),
        ("That's why, I love fall 🍂", 6.8),
        ("Looking at the stars 💫", 11.1),
        ("Admiring from afar 🙍 ", 14.5),
        ("My gril, my gril, my gril 💞", 18.5),
        ("You will be my gril 😍", 23.8),
        ("My gril, my gril, my gril 💖", 26.9),
        ("You will be my world 🌍", 32.5),
        ("My world, my world, my world 🕺", 33.7),
        ("You will be my gril 😆", 41.0),
        ("🎧🎶", 41.9),
    ]
    print(" = We fell in love in october = \n ")

    threads = []
    for lyric_text, lyric_delay in lyrics:
        t = Thread(target=sing_lyric, args=(lyric_text, lyric_delay))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sing_song()
