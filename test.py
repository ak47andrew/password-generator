import time
from console_progressbar import ProgressBar

pb = ProgressBar(total=100,prefix='Converting video', decimals=2, length=70, fill='█', zfill='_')
pb.print_progress_bar(2)
time.sleep(5)
pb.print_progress_bar(25)
time.sleep(5)
pb.print_progress_bar(50)
time.sleep(5)
pb.print_progress_bar(95)
time.sleep(5)
pb.print_progress_bar(100)
