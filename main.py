import converters
import time

start = time.time()
converters.image("1.webp")
converters.video("Dunes.mov")
print(time.time() - start)
