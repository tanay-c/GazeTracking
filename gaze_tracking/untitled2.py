from skimage import io
import numpy as np
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
%matplotlib 
matplotlib.use('Qt5Agg')

vol = io.imread("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/attention-mri.tif")

vol.shape
volume=np.swapaxes(vol,0,1)



def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)
                



class IndexTracker:
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title("use buttons j and k to navigate images")

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.X[:, :, self.ind])
        self.update()

    def on_scroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        self.ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()
        
    def process_key(self, event):
        if event.key == 'j':
            self.previous_slice(ax)
        elif event.key == 'k':
            self.next_slice(ax)
        self.update()

    def previous_slice(self, ax):
        self.ind = (self.ind - 1) % self.slices

    def next_slice(self, ax):
        self.ind = (self.ind + 1) % self.slices

# fig, ax = plt.subplots(1, 1)

# X = vol_a

# tracker = IndexTracker(ax, X)


# fig.canvas.mpl_connect('scroll_event', tracker.on_scroll)
# plt.show()

              
def ShowSlice():
    fig, ax = plt.subplots(1, 1)
    X = vol
    tracker = IndexTracker(ax, X)
    fig.canvas.mpl_connect('scroll_event', tracker.on_scroll)
    plt.show()
    return tracker  

tr=ShowSlice()