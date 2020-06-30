PATH = './trained_models/from_pdf/'

from flair.visual.training_curves import Plotter
plotter = Plotter()
plotter.plot_training_curves(PATH + 'loss.tsv')
plotter.plot_weights(PATH + 'weights.txt')