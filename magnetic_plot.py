import numpy as np
import seaborn as sns
from matplotlib.backends import backend_agg
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt

def get_grid_values(xrange: tuple, yrange:tuple) -> tuple:
    return np.meshgrid(np.linspace(*xrange),
                        np.linspace(*yrange))

def get_field_components(distance: float, currents: tuple,
                        magconst: float, xrange: tuple,
                        yrange:tuple) -> tuple:
    (x, y) = get_grid_values(xrange, yrange)
    x1 = x - distance
    x2 = x + distance
    s12 = x1 ** 2 + y ** 2
    s22 = x2 ** 2 + y ** 2
    (I1, I2) = currents
    const = magconst / (s12 * s22)
    Bx = const * -y * ((I1 * s22) + (I2 * s12))
    By = const * ((I1 * s22 * x1) + (I2 * s12 * x2))
    return (Bx, By)

class Experiment:
    def __init__(self, d: float, Is: tuple,
                xrange, yrange, m: float=2.0e-7):
        self.distance = d
        self.magconst = m
        (self.current1, self.current2) = Is
        self.xrange = xrange
        (self.xmin, self.xmax, _) = xrange
        self.yrange = yrange
        (self.ymin, self.ymax, _) = yrange
        (self.x, self.y) = get_grid_values(xrange, yrange)
        self.ranges = [self.xmin, self.xmax,
                        self.ymin, self.ymax]
        (self.Bx, self.By) = get_field_components(
            self.distance, Is, self.magconst,
            self.xrange, self.yrange)
        self.B = self.Bx + self.By

from matplotlib.colors import LinearSegmentedColormap
class ExperimentPlotConfig:
    def __init__(self, size: tuple, title_size: int=14,
                label_size: int=10,
                bgcolor: str="#aaaaaa", num_colors: int=8,
                colorbar_adjust: float=1.0,
                aspect_ratio=1.0):
        self.size = size
        self.title_size = title_size
        self.label_size = label_size
        self.bgcolor = bgcolor
        self.num_colors = num_colors
        self.colorbar_adjust = colorbar_adjust
        self.aspect_ratio = aspect_ratio
    
    def fg_cmap(self, palette_name="husl"):
        colors = sns.color_palette(palette_name, self.num_colors)
        colors.reverse()
        return LinearSegmentedColormap.from_list(palette_name, colors)
        
    def bg_cmap(self):
        return sns.dark_palette(self.bgcolor, as_cmap=True)

class Plotter:
    def __init__(self, index, plot_config, experiment):
        self.cfg = plot_config
        self.data = experiment
        # self.figure_manager = backend_agg.new_figure_manager(
            # index, figsize=self.cfg.size)
        # self.figure = self.figure_manager.canvas.figure
        self.figure = plt.figure(index, figsize=self.cfg.size)
    
    def get_axes(self):
        gs = GridSpec(1, 1)
        return self.figure.add_subplot(gs[0, 0])

    def update_axes(self, axes):
        tmpl = ('Magnetic Field for Two Wires\n'
                '$I_1$={} A, $I_2$={} A, at d={} m')
        title = tmpl.format(self.data.current1,
                            self.data.current2,
                            self.data.distance)
        axes.set_title(
            title, fontsize=self.cfg.title_size)
        axes.set_xlabel(
            '$x$ m', fontsize=self.cfg.label_size)
        axes.set_ylabel(
            '$y$ m', fontsize=self.cfg.label_size)
        axes.axis(
            self.data.ranges,
            aspect=self.cfg.aspect_ratio)
        return axes
    
    def make_background(self, axes):
        return axes.imshow(
                self.data.B, extent=self.data.ranges,
                cmap=self.cfg.bg_cmap())

    def make_quiver(self, axes):
        return axes.quiver(
            self.data.x, self.data.y,
            self.data.Bx, self.data.By,
            self.data.B, cmap=self.cfg.fg_cmap())

    def make_colorbar(self, figure, quiver):
        return self.figure.colorbar(
            quiver, shrink=self.cfg.colorbar_adjust)

    def save(self, filename, **kwargs):
        axes = self.update_axes(self.get_axes())
        back = self.make_background(axes)
        quiver = self.make_quiver(axes)
        colorbar = self.make_colorbar(self.figure, quiver)
        self.figure.savefig(filename, **kwargs)
        print("Saved {}.".format(filename))

if __name__=='__main__':
    plot_config = ExperimentPlotConfig(
        size=(12,10),
        title_size=20,
        label_size=16,
        bgcolor="#666666",
        colorbar_adjust=0.96)
    
    experiments = [
        Experiment(d=0.04, Is=(1,1),
                xrange=(-0.1, 0.1, 20),
                yrange=(-0.1, 0.1, 20)),
        Experiment(d=2.0, Is=(10,20),
                xrange=(-1.2, 1.2, 70),
                yrange=(-1.2, 1.2, 70)),
        Experiment(d=4.0, Is=(45,15),
                xrange=(-5.3, 5.3, 60),
                yrange=(-5.3, 5.3, 60)),
        Experiment(d=2.0, Is=(1,2),
                xrange=(-8.0, 8.0, 50),
                yrange=(-8.0, 8.0, 50))]
    
    for (index, experiment) in enumerate(experiments):
        filename = "expmt_{}.png".format(index)
        Plotter(index,
                plot_config,
                experiment).save(filename)