import random
import sys
import time
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

pallete_name = "husl"
colors = sns.color_palette(pallete_name, 8)
colors.reverse()
cmap = mpl.colors.LinearSegmentedColormap.from_list(pallete_name, colors)

# def press_callback(event):
#     event.canvas.figure.text(event.xdata, event.ydata, '<- clicked here')
#     print('you pressed', event.button, event.xdata, event.ydata)
    
# def release_callback(event):
#     event.canvas.draw()
    
# (figure, axes) = plt.subplots()
# press_conn_id = figure.canvas.mpl_connect('button_press_event', press_callback)
# release_conn_id = figure.canvas.mpl_connect('button_release_event', release_callback)
# plt.show()

##################################################################


##########################################################
# class LineBuilder:
#     def __init__(self, line):
#         self.line = line
#         self.xs = list(line.get_xdata())
#         self.ys = list(line.get_ydata())
#         self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

#     def __call__(self, event):
#         print('click', event)
#         if event.inaxes!=self.line.axes: return
#         self.xs.append(event.xdata)
#         self.ys.append(event.ydata)
#         self.line.set_data(self.xs, self.ys)
#         self.line.figure.canvas.draw()

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_title('click to build line segments')
# line, = ax.plot([0], [0])  # empty line
# linebuilder = LineBuilder(line)

# plt.show()

##################################################################
# from matplotlib import widgets
# from matplotlib.backend_bases import MouseEvent

# def get_sine_data(amplitude=5, frequency=3, time=None):
#     return amplitude * np.sin(2 * np.pi * frequency * time)

# class SineSliders:
#     def __init__(self, amplitude=5, frequency=3):
#         (self.figure, _) = plt.subplots()
#         self.configure()
#         self.a0 = amplitude
#         self.f0 = frequency
#         self.time = np.arange(0.0, 1.0, 0.001)
#         self.data = get_sine_data(
#             amplitude=self.a0, frequency=self.f0, time=self.time)
#         (self.line,) = plt.plot(self.time, self.data, lw=2, color='red')
#         self.axes_amp  = plt.axes([0.25, 0.15, 0.65, 0.03])
#         self.axes_freq = plt.axes([0.25, 0.1, 0.65, 0.03])
#         self.setup_sliders()
#         self.setup_reset_button()
#         self.setup_color_selector()

#     def start(self):
#         plt.show()

#     def configure(self):
#         plt.subplots_adjust(left=0.25, bottom=0.25)
#         plt.axis([0, 1, -10, 10])

#     def setup_sliders(self):
#         self.slider_amp = widgets.Slider(
#             self.axes_amp, 'Amp', 0.1, 10.0, valinit=self.a0)
#         self.slider_freq = widgets.Slider(
#             self.axes_freq, 'Freq', 0.1, 30.0, valinit=self.f0)
#         self.slider_freq.on_changed(self.update)
#         self.slider_amp.on_changed(self.update)
        
#     def setup_reset_button(self):
#         reset_axes = plt.axes([0.8, 0.025, 0.1, 0.04])
#         reset_button = widgets.Button(reset_axes, 'Reset', hovercolor='0.975')
#         reset_button.on_clicked(self.reset)
        
#     def setup_color_selector(self):
#         radio_axes = plt.axes([0.025, 0.5, 0.15, 0.15], aspect=1)
#         radio_select = widgets.RadioButtons(
#             radio_axes, ('red', 'blue', 'green',), active=0)
#         radio_select.on_clicked(self.switchcolor)
        
#     def update(self, val):
#         self.data = get_sine_data(self.slider_amp.val,
#                                   self.slider_freq.val,
#                                   self.time)
#         self.line.set_ydata(self.data)
#         self.figure.canvas.draw()

#     def reset(self, event):
#         self.slider_freq.reset()
#         self.slider_amp.reset()

#     def switchcolor(self, label):
#         self.line.set_color(label)
#         self.figure.canvas.draw()

# sldrs = SineSliders(amplitude=0.5, frequency=20)
# sldrs.start()

####################################################
# import numpy as np
# import matplotlib.pyplot as plt

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_title('click on points')

# line, = ax.plot(np.random.rand(100), 'o', picker=5)  # 5 points tolerance

# def onpick(event):
#     thisline = event.artist
#     xdata = thisline.get_xdata()
#     ydata = thisline.get_ydata()
#     ind = event.ind
#     points = tuple(zip(xdata[ind], ydata[ind]))
#     print('onpick points:', points)

# fig.canvas.mpl_connect('pick_event', onpick)

# plt.show()

##################################################
import numpy as np
import matplotlib.pyplot as plt

X = np.random.rand(100, 1000)
xs = np.mean(X, axis=1)
ys = np.std(X, axis=1)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click on point to plot time series')
line, = ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance


def onpick(event):

    if event.artist!=line: return True
    print(event.artist)

    N = len(event.ind)
    if not N: return True


    figi = plt.figure()
    for subplotnum, dataind in enumerate(event.ind):
        ax = figi.add_subplot(N,1,subplotnum+1)
        ax.plot(X[dataind])
        ax.text(0.05, 0.9, 'mu={:.3f}\nsigma={:.3f}'.format(xs[dataind], ys[dataind]),
                transform=ax.transAxes, va='top')
        ax.set_ylim(-0.5, 1.5)
    figi.show()
    return True

fig.canvas.mpl_connect('pick_event', onpick)

plt.show()