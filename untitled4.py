from skimage import io
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pandas as pd

# %matplotlib
# matplotlib.use("Qt5Agg")
from gaze_tracking import GazeTracking

vol = io.imread("img.tif")
vol.shape
volume = np.swapaxes(vol, 0, 1)
gaze = GazeTracking()
webCam = cv2.VideoCapture(0)


class IndexTracker:
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title("use scroller")
        self.X = X
        _, _, self.SliceCount = X.shape
        self.currSliceIndex = self.SliceCount // 2
        self.im = ax.imshow(self.X[:, :, self.currSliceIndex])
        self.update()

    def onScroll(self, event):
        if event.button == "up":
            self.currSliceIndex = (self.currSliceIndex + 1) % self.SliceCount
            self.update()
        else:
            self.currSliceIndex = (self.currSliceIndex - 1) % self.SliceCount
            self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.currSliceIndex])
        self.ax.set_ylabel("slice %s" % self.currSliceIndex)
        self.im.axes.figure.canvas.draw()


# Create a plot
fig, ax = plt.subplots(1, 1)
X = vol
tracker = IndexTracker(ax, X)
fig.canvas.mpl_connect("scroll_event", tracker.onScroll)
tracker_history = []

while True:
    plt.pause(0.001)
    _, frame = webCam.read()
    gaze.refresh(frame)
    slc = {"slice": tracker.currSliceIndex}
    slc["leye"] = gaze.pupil_left_coords()
    slc["reye"] = gaze.pupil_right_coords()
    tracker_history.append(slc)
    cv2.imshow("Demo", frame)
    if cv2.waitKey(1) == 27:
        break
    print(slc)

plt.close(fig)
df = pd.DataFrame.from_dict(tracker_history)
df.to_csv("out.csv")
webCam.release()
cv2.destroyAllWindows()
