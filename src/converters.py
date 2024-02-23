import os

from console_progressbar import ProgressBar
from moviepy.editor import VideoFileClip
from PIL import Image


# ! DON'T REMOVE OR RENAME METHODS "default" AND "folder"!
# NOTE You, however, can change their behaver as soon as they return list of integers
def default(path: str, silent: bool):
    if not silent:
        print(f"No function found for the extension {path}. Using default method")
    with open(path, "rb") as f:
        data = f.read()
    return [i for i in data]


def folder(path: str, silent: bool):
    o = []

    for file in os.listdir(path):
        np = os.path.join(path, file)
        if not silent:
            print(f"Processing {np}")

        if os.path.isdir(np):
            o.extend(folder(np, silent))
        else:
            ext = np.split(".")[-1].lower()
            command = config.get(ext, default)
            o.extend(command(np, silent))

    return o


# NOTE If you rename this methods, remove them or add new - don't forget to change them in the "config" variable
def image(path: str, silent: bool):
    img = Image.open(path)
    pixels = img.load()

    def get_value(x: int, y: int):
        pixel = pixels[x,y]
        if isinstance(pixel, int):
            pixel = (pixel, pixel, pixel)
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
                return pixel[0] % max(1, x) + pixel[1] % max(1, y)
            case 6:
                return pixel[0] % 2 + pixel[1] % 3 + pixel[2] % 6

    o = list()
    pb = ProgressBar(total=(img.size[0] - 1) * img.size[0] + (img.size[1] - 1) + 1,prefix='Converting image')
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            o.append(get_value(x, y))
        if not silent:
            pb.print_progress_bar(x * img.size[0] + y + 1)
    return o


def video(path: str, silent: bool):
    def split_vid(clip: VideoFileClip, start: int, end: int) -> tuple[VideoFileClip, bool]:
        if end > clip.duration:
            end = clip.duration
            output = True
        else:
            output = False
        
        subclip = clip.subclip(start, end)

        return subclip, output

    o = []
    clip = VideoFileClip(path)
    pb = ProgressBar(total=int(clip.fps * clip.duration) + 1,prefix='Converting video')
    if not silent:
        pb.print_progress_bar(0)
    start = 0
    end = 1
    
    while True:
        subclip, finish = split_vid(clip, start, end)
        
        start += 1
        end += 1

        for ind, frame in enumerate(subclip.iter_frames()):
            flatten = frame.ravel().tolist()
            o.append(sum(flatten) // len(flatten) + ind)
            if not silent:
                pb.next()
        if finish:
            break
    
    return o


config = {
    # Images
    "png": image,
    "jpg": image,
    "jpeg": image,
    "bmp": image,
    "webp": image,

    # Videos
    "mov": video,
    "mp4": video,
}
