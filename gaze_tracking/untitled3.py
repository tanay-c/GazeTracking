from skimage import io
import numpy as np
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# %matplotlib
matplotlib.use('Qt5Agg')

vol = io.imread(
    "https://s3.amazonaws.com/assets.datacamp.com/blog_assets/attention-mri.tif")
vol.shape
volume = np.swapaxes(vol, 0, 1)
gaze = GazeTracking()


#SliceCount = 60
# _, _, SliceCount = volume.shape
# SliceCount = SliceCount // 2

#slices = [{"leye": None, "reye": None} for _ in range(SliceCount)]


class IndexTracker:
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title("use bscroller")
        self.X = X
        _, _, self.SliceCount = X.shape
        self.currSliceIndex = self.SliceCount // 2
        self.im = ax.imshow(self.X[:, :, self.currSliceIndex])
        self.update()

    # currSliceIndex = 0
    # image = ax.imshow(volume[:, :, currSliceIndex])

    def onScroll(self, event):
        if event.button == 'up':
            self.currSliceIndex = (self.currSliceIndex + 1) % self.SliceCount
        else:
            self.currSliceIndex = (self.currSliceIndex - 1) % self.SliceCount
        # image.set_data(volume[:, :, currSliceIndex])

    def update(self):
        self.im.set_data(self.X[:, :, self.currSliceIndex])
        self.ax.set_ylabel('slice %s' % self.currSliceIndex)
        self.im.axes.figure.canvas.draw()


def create_slices(n):
    return([{"leye": None, "reye": None} for _ in range(n)])


webCam = cv2.VideoCapture(0)

while True:
    _, frame = webCam.read()
    gaze.refresh(frame)

    slices[currSliceIndex]["leye"] = gaze.pupil_left_coords()
    slices[currSliceIndex]["reye"] = gaze.pupil_left_coords()

    image.axes.figure.canvas.draw()
    if cv2.waitKey(1) == 27:
        break


def ShowSlice():
    fig, ax = plt.subplots(1, 1)
    X = vol
    tracker = IndexTracker(ax, X)
    fig.canvas.mpl_connect('scroll_event', tonScroll)
    plt.show()
    return tracker


tr = ShowSlice()
df = pd.DataFrame.from_dict(slices)
webcam.release()
cv2.destroyAllWindows()

df.to_csv('out.csv')
