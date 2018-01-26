import numpy as np
from sklearn.metrics import roc_curve

import warnings # current version of seaborn generates a bunch of warnings that we'll ignore
warnings.filterwarnings("ignore")
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.style
import matplotlib as mpl


def extract_final_losses(history):
	train_loss = history.history['loss']
	val_loss = history.history['val_loss']
	idx_min_val_loss = np.argmin(val_loss)
	return {'train_loss': train_loss[idx_min_val_loss], 'val_loss': val_loss[idx_min_val_loss]}

def plot_training_error_curves(history, arch_idx = None):
	print("Ploting training error curves...")

	train_loss = history.history['loss']
	val_loss = history.history['val_loss']

	mpl.style.use('default')
	fig, ax = plt.subplots()
	ax.grid(False)
	ax.plot(train_loss, label = 'Train')
	ax.plot(val_loss, label = 'Validation')
	ax.set(title = 'Training and Validation Error Curves', xlabel = 'Epochs', ylabel = 'Loss (MSE)')
	ax.legend()

	#plt.show()
	file = "plot.png"
	if arch_idx:
		file = "arch_" + str(arch_idx) + "_" + file

	file = "results/" + file

	fig.savefig(file)

def plot_roc_curve(y_test, y_pred, arch_idx = None):
	print("Ploting ROC curve...")
	fpr_net, tpr_net, _ = roc_curve(y_test, y_pred)

	mpl.style.use('default')
	fig, ax = plt.subplots()
	ax.grid(False)
	ax.plot([0, 1], [0, 1], 'k--')
	ax.plot(fpr_net, tpr_net, label='net1')
	ax.set(title = 'ROC Curve', xlabel = 'False positive rate', ylabel = 'True positive rate')

	#plt.show()
	file = "roc.png"
	if arch_idx:
		file = "arch_" + str(arch_idx) + "_" + file

	file = "results/" + file

	fig.savefig(file)

def plot_scatter_matrix(dset, hue):
	sns.set(color_codes=True)
	g = sns.pairplot(dset, hue=hue, vars=["f1", "f2", "f3", "f4", "f5", "f6"], markers=["o", "x"])
	g.fig.get_children()[-1].set_bbox_to_anchor((1.1, 0.5, 0, 0))
	g.savefig("./results/dset_scat_matrix.png")

def plot_boxPlot(dset):
	sns.set(color_codes=True)
	plt.figure()
	axes = dset.boxplot(by='target', figsize=(12, 6), return_type='axes')
	for ax in axes:
		ax.set_ylim(-1.4, 10)
	
	plt.savefig("./results/dset_boxplot.png")

def plot_series(dset_full, train_predict, val_predict, test_predict, look_back, scaler, dimension='x'):
	print("Plotting serie curve...")

	mpl.style.use('default')
	fig, ax = plt.subplots()
	ax.grid(False)

	# shift train predictions for plotting
	train_predict_plot = np.empty_like(dset_full)
	train_predict_plot[:, :] = np.nan
	train_predict_plot[look_back:len(train_predict)+look_back, :] = train_predict
	# shift validation predictions for plotting
	val_predict_plot = np.empty_like(dset_full)
	val_predict_plot[:, :] = np.nan
	val_predict_plot[len(train_predict)+(look_back):len(val_predict)+len(train_predict)+(look_back), :] = val_predict
	# shift test predictions for plotting
	test_predict_plot = np.empty_like(dset_full)
	test_predict_plot[:, :] = np.nan
	test_predict_plot[len(dset_full)-len(test_predict):len(dset_full), :] = test_predict
	# plot baseline and predictions
	plt.plot(scaler.inverse_transform(dset_full))
	plt.plot(train_predict_plot)
	plt.plot(val_predict_plot)
	plt.plot(test_predict_plot)

	#plt.show()
	file = dimension + "_serie.png"
	if arch_idx:
		file = "arch_" + str(arch_idx) + "_" + file

	file = "results/" + file

	fig.savefig(file)

def plot_2d_series(dset_full, train_predict, val_predict, test_predict, look_back, scaler):
	print("Plotting 2D serie curve...")
	mpl.style.use('default')
	#TODO
