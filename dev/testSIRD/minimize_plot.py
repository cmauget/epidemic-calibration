import matplotlib.pyplot as plt, numpy as np, pandas as pd

def final_plot(df, basename, methods):
	fig, ax = plt.subplots(figsize=(8.26,8.26))
	ax.set_title(f'Comparison of methods (SIRD model, {basename})', fontsize=20)
	for i, method in enumerate(df.Methods.unique()):
		_df = df[ df.Methods == method]
		if method in methods:
			LS = ['-.', '-', '--']
			ls = LS[ i%len(LS) ]
			ax.plot(_df.Starting_Days.apply(lambda v: str(v)), _df.Mae, ls=ls, lw=3.75, label=method)			
		else:
			LS = ['-.', ':', '-', '--']
			ls = LS[ i%len(LS) ]
			#~ ls = np.random.choice([':', '-', '-.'])
			ax.plot(_df.Starting_Days.apply(lambda v: str(v)), _df.Mae, ls=ls, lw=1, label=method)
	ax.set_xlabel('Starting day', fontsize=16)
	ax.set_ylabel('MAE', fontsize=16)
	ax.set_yscale('log')
	#~ ax.set_ylim([0.99 * _df.Mae.min(), 1.1 * _df.Mae.max()])
	ax.legend(ncol=3, loc='upper center', fontsize=12)
	#~ plt.grid()
	plt.savefig(f'fig/fig_SIRD_{basename}.pdf')
	plt.show()
	plt.close(fig)

DUOS = [
	['n5', ['bfgs', 'powell']],
	['n10', ['bfgs']],
	['ny', ['cg', 'bfgs','slsqp', 'shgo', 'nelder']],
	]

for basename, methods in DUOS:
	df = pd.read_csv(f'data/sird_{basename}.csv', sep = ',')
	final_plot(df, basename, methods)
