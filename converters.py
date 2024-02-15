from PIL import Image
from moviepy.editor import VideoFileClip
from console_progressbar import ProgressBar


def image(path: str):
    img = Image.open(path)
    pixels = img.load()

    def get_value(x: int, y: int):
        pixel = pixels[x,y]
        match sum(pixel) % 7:
            case 0:
                return 0
            case 1:
                return 1
            case 2:
                return pixel[2] // 2
            case 3:
                return sum(pixel) // 3
            case 4:
                return pixel[0] + pixel[2]
            case 5:
                return pixel[0] % (x if x != 0 else 1) + pixel[1] % (y if y != 0 else 1)
            case 6:
                return pixel[0] % 2 + pixel[1] % 3 + pixel[2] % 6

    o = list()
    pb = ProgressBar(total=img.size[0] * img.size[1],prefix='Converting image', 
                     decimals=2, length=150, fill='█', zfill='_')
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            pb.print_progress_bar(x * img.size[0] + y + 1)
            o.append(get_value(x, y))
    return o


def video(path: str):
    o = []
    frames = list(VideoFileClip(path).iter_frames())
    pb = ProgressBar(total=len(frames),prefix='Converting video', 
                     decimals=2, length=150, fill='█', zfill='_')
    print(len(frames))
    for ind, frame in enumerate(frames):
        flatten = frame.ravel().tolist()
        o.append(sum(flatten) // len(flatten) + ind)
        pb.print_progress_bar(ind + 1)
    print("Done!")
    return o
