import time
from threading import Thread, Lock
import sys

lock = Lock()

COLOR_MAP = {
    '🙋': (255, 105, 180),
    '🤷': (46, 207, 240),
    '❓': (218, 145, 255, 0.35),
    '🙅': (125, 251, 237, 0.349),
    '😁': (201, 30, 30),
    '🤔': (177, 158, 189, 0.71),
    '🙅': (221, 125, 5),
    '😴': (167, 0, 230),
    '😋': (0, 212, 147, 0.89),
    '🤭': (255, 177, 61),
    '👫': (114, 153, 255),
    '🌅': (0, 116, 149),
    '👩‍❤️‍👨': (0, 255, 149),
    '🔇': (255, 255, 255),
}

def get_target_color(text):
    for c in reversed(text):
        if c in COLOR_MAP:
            return COLOR_MAP[c]
    return (255, 255, 255)

def animate_text(text, delay=0.2):
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
        ("\nBertanya 🙋", 0.15),
        ("Mengapa kita 🤷", 5.0),
        ("Masih disini❓", 10.0),
        ("Tersenyum 😁\n ", 15.7),
        ("\nAlasan masih bersama 🤔", 22.5),
        ("Bukan 🙅", 22.6),
        ("Karena terlanjur lama 😴", 22.61),
        ("Tapi rasanya 😋", 22.8),
        ("Yang masih sama 🤭\n ", 37.8),
        ("\nSeperti sejak pertama jumpa 👫", 45.0),
        ("Dirimu dikala senja 🌅", 46.8),
        ("Duduk berdua 👩‍❤️‍👨", 48.0),
        ("Tanpa suara 🔇\n", 61.2),
    ]
    print(" = Monolog - Pamungkus = \n ")

    threads = []
    for lyric_text, lyric_delay in lyrics:
        t = Thread(target=sing_lyric, args=(lyric_text, lyric_delay))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sing_song()
