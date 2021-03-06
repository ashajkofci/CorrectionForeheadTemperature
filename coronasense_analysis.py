# -*- coding: utf-8 -*-
"""coronasense_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SptFyUf_Y4y1APZxBY-ZteB3q3mcQkPE
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib import cm
from matplotlib.colors import Normalize 
from scipy.interpolate import interpn

df = pd.read_csv('data.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
df = df.set_index(pd.DatetimeIndex(df['timestamp']))
df = df[df['timestamp'] >= pd.Timestamp('2020/08/30')]
df = df[df['timestamp'] <= pd.Timestamp('2020/10/03')]
df = df[df['obj_score'] <= 39]
df = df[df['obj_score'] >= 33.5]
df['obj_score'] = df['obj_score'] + 0.1

print(df['timestamp'])
print(df.index)

def density_scatter( x , y, ax = None, sort = True, bins = 15, **kwargs )   :

    if ax is None :
        fig , ax = plt.subplots()
    data , x_e, y_e = np.histogram2d( x, y, bins = bins, density = True)
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False)

    z[np.where(np.isnan(z))] = 0.0

    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

    ax.scatter( x, y, c=z, s=2.5, **kwargs )

    norm = Normalize(vmin = np.min(z), vmax = np.max(z))
    #cbar = fig.colorbar(cm.ScalarMappable(norm = norm), ax=ax)
    #cbar.ax.set_ylabel('Density')

    return ax

fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
plt.plot(df['timestamp'], df['obj_score'],'.', alpha=0.1, label='Forehead temperature')
df_mean = df.resample('D').apply({'obj_score':'mean'})
df_std = df.resample('D').apply({'obj_score':'std'})

plt.plot(df_mean.index+pd.Timedelta('0.5 day'), df_mean['obj_score'], label='Average over 24h')

plt.fill_between(df_mean.index+pd.Timedelta('0.5 day'), df_mean['obj_score'] - df_std['obj_score']/2, df_mean['obj_score'] + df_std['obj_score']/2,
                 color='gray', alpha=1.0)

# Set title and labels for axes
ax.set(       ylabel="Forehead temp. (deg. C)", xlabel="Time (days)")

# Rotate tick marks on x-axis
#plt.setp(ax.get_xticklabels(), rotation=0)
frame1 = plt.gca()
#frame1.axes.xaxis.set_ticks([])
#ax.set_legend['Forehead temperature', 'Average over a day']
ax.legend()
print(len(df))
print("avg {} std {}".format(df['obj_score'].mean(), df['obj_score'].std()))
fig.subplots_adjust(bottom=0.2)
mean_raw = df['obj_score'].mean()
plt.tight_layout()
ax.set_ylim(33,39)

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()  # every month

years_fmt = mdates.DateFormatter('%Y')

ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(days)


# format the coords message box
#ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
#fig.autofmt_xdate()


plt.savefig('all_data.png')

groups = df.groupby(['rfid_uid']).std()['obj_score']
print('Personal mean {}, personal std {}'.format(groups.mean(), groups.std()))


print("Location A")
df_filtered = df[df['machine_id'].isin([4428])]
print("len {} avg {} std {}".format(len(df_filtered), df_filtered['obj_score'].mean(), df_filtered['obj_score'].std()))

groups = df_filtered.groupby(['rfid_uid']).std()['obj_score']
print('Personal mean {}, personal std {}'.format(groups.mean(), groups.std()))

print("Location B")
df_filtered = df[df['machine_id'].isin([2952,3075,3690,3813,3936,4059,4182,4305])]

groups = df_filtered.groupby(['rfid_uid']).std()['obj_score']
print('Personal mean {}, personal std {}'.format(groups.mean(), groups.std()))

print("len {} avg {} std {}".format(len(df_filtered), df_filtered['obj_score'].mean(), df_filtered['obj_score'].std()))
print("Location C")
df_filtered = df[df['machine_id'].isin([6396])]

groups = df_filtered.groupby(['rfid_uid']).std()['obj_score']
print('Personal mean {}, personal std {}'.format(groups.mean(), groups.std()))
print("len {} avg {} std {}".format(len(df_filtered), df_filtered['obj_score'].mean(), df_filtered['obj_score'].std()))


more_than_37 = df['obj_score']
print(len(more_than_37[more_than_37 > more_than_37.mean() + 3*more_than_37.std()]))

df_filtered_notouch = df[df['meteo_realtemp'] > 0]
df_filtered_notouch = df_filtered_notouch[df_filtered_notouch['machine_id'].isin([3075, 3936, 4059, 5781, 4428, 5535, 7134, 2706, 5904, 6396])]

plt.rcParams["figure.dpi"] = 180
fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
df.hist(column=['obj_score'], bins=20, figsize=(6, 3), ax = plt.gca())
ax.set(      ylabel="# Measurements", xlabel="Forehead temperature (degrees C)")
ax.set_title("")
ax.set_xlim(33,39)
# x coordinates for the lines
xcoords = [37.81]
# colors for the lines
colors = ['r']
for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='Fever threshold (μ+3σ = {})'.format(xc), c=c)
fig.subplots_adjust(bottom=0.2) 
plt.legend()
plt.tight_layout()

plt.savefig('hist_all.png')

fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
df_outside = df[df['meteo_realtemp'] > 0]
df_outside = df_outside[df_outside['machine_id'].isin([3075, 3936, 4059, 5781, 4428, 5535, 7134, 2706, 5904, 6396])] 

linear_regressor = LinearRegression()
linear_regressor.fit(df_outside['meteo_realtemp'].values.reshape(-1, 1), df_outside['obj_score'].values.reshape(-1, 1))
X = np.linspace(df_outside['meteo_realtemp'].min(), df_outside['meteo_realtemp'].max()).reshape(-1, 1)
Y_pred = linear_regressor.predict(X)
score_r2 = linear_regressor.score(df_outside['meteo_realtemp'].values.reshape(-1, 1), df_outside['obj_score'].values.reshape(-1, 1))
print('R2 = ',score_r2)


ax.set(xlabel="Outside temperature (deg. C)",
       ylabel="Forehead temp. (deg. C)")

density_scatter(df_outside['meteo_realtemp'], df_outside['obj_score'], ax=ax,label='Forehead temperature')
plt.plot(X, Y_pred, 'red', label=r'Linear fit $R^2={:.2f}$'.format(score_r2))

#df_ambient = df.resample('D').apply({'amb_temp':'mean'})
#plt.plot(df_mean.index, df_ambient['amb_temp'], label='Ambient temperature')

# Rotate tick marks on x-axis
plt.setp(ax.get_xticklabels(), rotation=45)
#ax.set_legend['Forehead temperature', 'Average over a day']
ax.legend()
print(len(df_outside))
#plt.title("Effect of outside temperature on forehead temperature")
more_than_37 = df_outside['obj_score']

print(len(more_than_37[more_than_37 > more_than_37.mean() + 3*more_than_37.std()]))
plt.tight_layout()

plt.savefig('outside_forehead.png')

fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
df_outside = df[df['meteo_realtemp'] > 0]
df_outside = df_outside[df_outside['machine_id'].isin([3075, 3936, 4059, 5781, 4428, 5535, 7134, 2706, 5904, 6396])]

linear_regressor = LinearRegression()
linear_regressor.fit(df_outside['meteo_realtemp'].values.reshape(-1, 1), df_outside['obj_score'].values.reshape(-1, 1))
X = np.linspace(df_outside['meteo_realtemp'].min(), df_outside['meteo_realtemp'].max()).reshape(-1, 1)
Y_pred = linear_regressor.predict(X)
score_r2 = linear_regressor.score(df_outside['meteo_realtemp'].values.reshape(-1, 1), df_outside['obj_score'].values.reshape(-1, 1))
print('R2 = ',score_r2)


ax.set(xlabel="Outside temperature (degrees C)",
       ylabel="Forehead temp. (deg. C)")
curve = linear_regressor.predict(df_outside['meteo_realtemp'].values.reshape(-1, 1))[:,0]
density_scatter(df_outside['meteo_realtemp'], df_outside['obj_score']-curve+mean_raw,ax = ax, label='Forehead temperature')
ax.set_ylim(33,39)

#df_ambient = df.resample('D').apply({'amb_temp':'mean'})
#plt.plot(df_mean.index, df_ambient['amb_temp'], label='Ambient temperature')

# Rotate tick marks on x-axis
plt.setp(ax.get_xticklabels(), rotation=45)
#ax.set_legend['Forehead temperature', 'Average over a day']
print(len(df_outside))
#plt.title("Measurements corrected from outside temperature model")
new_df = df_outside.copy()
new_df['obj_score'] = new_df['obj_score']-curve+mean_raw
more_than_37 = df_outside['obj_score']-curve+mean_raw
print(len(more_than_37[more_than_37 > more_than_37.mean() + 2*more_than_37.std()]))
plt.tight_layout()

plt.savefig('outside_forehead_corr.png')



fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
df_ambient = df[df['amb_temp'] > 0]

linear_regressor = LinearRegression()
linear_regressor.fit(df_ambient['amb_temp'].values.reshape(-1, 1), df_ambient['obj_score'].values.reshape(-1, 1))
X = np.linspace(df_ambient['amb_temp'].min(), df_ambient['amb_temp'].max()).reshape(-1, 1)
Y_pred = linear_regressor.predict(X)
score_r2 = linear_regressor.score(df_ambient['amb_temp'].values.reshape(-1, 1), df_ambient['obj_score'].values.reshape(-1, 1))
print('R2 = ',score_r2)

ax.set(xlabel="Ambient temperature (degrees C)",
       ylabel="Forehead temp. (deg. C)")
ax.set_ylim(33,39)

density_scatter(df_ambient['amb_temp'], df_ambient['obj_score'],ax = ax, label='Forehead temperature')
plt.plot(X, Y_pred, 'red', label=r'Linear fit $R^2={:.2f}$'.format(score_r2))


#df_ambient = df.resample('D').apply({'amb_temp':'mean'})
#plt.plot(df_mean.index, df_ambient['amb_temp'], label='Ambient temperature')

# Rotate tick marks on x-axis
plt.setp(ax.get_xticklabels(), rotation=45)
#ax.set_legend['Forehead temperature', 'Average over a day']
ax.legend()
#plt.title("Effect of ambient temperature on forehead temperature")
print(len(df_ambient))
plt.tight_layout()
plt.savefig('ambient_forehead.png')

fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
df_ambient = df[df['amb_temp'] > 0]

linear_regressor = LinearRegression()
linear_regressor.fit(df_ambient['amb_temp'].values.reshape(-1, 1), df_ambient['obj_score'].values.reshape(-1, 1))
X = np.linspace(df_ambient['amb_temp'].min(), df_ambient['amb_temp'].max()).reshape(-1, 1)
Y_pred = linear_regressor.predict(X)
score_r2 = linear_regressor.score(df_ambient['amb_temp'].values.reshape(-1, 1), df_ambient['obj_score'].values.reshape(-1, 1))
print('R2 = ',score_r2)

ax.set(xlabel="Ambient temperature (degrees C)",
       ylabel="Forehead temp. (deg. C)")
curve = linear_regressor.predict(df_ambient['amb_temp'].values.reshape(-1, 1))[:,0]
ax.set_ylim(33,39)

density_scatter(df_ambient['amb_temp'], df_ambient['obj_score']-curve+mean_raw,ax = ax, label='Forehead temperature')


#df_ambient = df.resample('D').apply({'amb_temp':'mean'})
#plt.plot(df_mean.index, df_ambient['amb_temp'], label='Ambient temperature')

# Rotate tick marks on x-axis
plt.setp(ax.get_xticklabels(), rotation=45)
#ax.set_legend['Forehead temperature', 'Average over a day']
#plt.title("Measurements corrected from ambient temperature model")
more_than_37 = df_ambient['obj_score']-curve+mean_raw
print(len(more_than_37[more_than_37 > more_than_37.mean() + 2*more_than_37.std()]))
plt.tight_layout()
plt.savefig('ambient_forehead_corr.png')



fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
df_ambient = new_df[new_df['amb_temp'] > 0]

linear_regressor = LinearRegression()
linear_regressor.fit(df_ambient['amb_temp'].values.reshape(-1, 1), df_ambient['obj_score'].values.reshape(-1, 1))
X = np.linspace(df_ambient['amb_temp'].min(), df_ambient['amb_temp'].max()).reshape(-1, 1)
Y_pred = linear_regressor.predict(X)
score_r2 = linear_regressor.score(df_ambient['amb_temp'].values.reshape(-1, 1), df_ambient['obj_score'].values.reshape(-1, 1))
print('R2 = ',score_r2)

ax.set(xlabel="Ambient temperature (degrees C)",
       ylabel="Forehead temp. (degrees C)")
curve = linear_regressor.predict(df_ambient['amb_temp'].values.reshape(-1, 1))[:,0]
ax.set_ylim(33,39)

density_scatter(df_ambient['amb_temp'], df_ambient['obj_score']-curve+mean_raw,ax=ax, label='Forehead temperature')

#plt.plot(df_ambient['amb_temp'], df_ambient['obj_score'],'.', alpha=0.1, label='Forehead temperature')
#plt.plot(X, Y_pred, 'red', label=r'Linear fit $R^2={:.2f}$'.format(score_r2))

#df_ambient = df.resample('D').apply({'amb_temp':'mean'})
#plt.plot(df_mean.index, df_ambient['amb_temp'], label='Ambient temperature')

# Rotate tick marks on x-axis
plt.setp(ax.get_xticklabels(), rotation=45)
#ax.set_legend['Forehead temperature', 'Average over a day']
ax.legend()
#plt.title("Measurements corrected from outside + ambient models")
more_than_37 = df_ambient['obj_score']-curve+mean_raw
new_df_all = df_ambient.copy()
new_df_all['obj_score'] = new_df_all['obj_score']-curve+mean_raw
print(len(df_ambient))
print(len(new_df_all))

print(len(more_than_37[more_than_37 > more_than_37.mean() + 2*more_than_37.std()]))
plt.tight_layout()

plt.savefig('foreheah_both_corr.png')

fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
df_hours = df
df_hours['hours'] = df_hours.index.hour


linear_regressor = make_pipeline(
        PolynomialFeatures(degree=2),
        LinearRegression()
        )
linear_regressor.fit(df_hours['hours'].values.reshape(-1, 1), df_hours['obj_score'].values.reshape(-1, 1))
X = np.linspace(df_hours['hours'].min(), df_hours['hours'].max()).reshape(-1, 1)

Y_pred = linear_regressor.predict(X)
score_r2 = linear_regressor.score(df_hours['hours'].values.reshape(-1, 1), df_hours['obj_score'].values.reshape(-1, 1))
print('R2 = ',score_r2)
ax.set_ylim(33,39)


ax.set(xlabel="Hours in the day (GMT)",
       ylabel="Forehead temp. (deg. C)")
by_hour = df_hours.groupby(df_hours.index.hour+2).mean()
by_hour_std = df_hours.groupby(df_hours.index.hour+2).std()


density_scatter(df_hours.index.hour, df_hours['obj_score'],ax=ax,label='Forehead temperature')
plt.plot(by_hour.index, by_hour['obj_score'],'-', alpha=1.0, label='Temperature average')
plt.fill_between(by_hour.index, by_hour['obj_score'] - by_hour_std['obj_score']/2, by_hour['obj_score'] + by_hour_std['obj_score']/2,
                 color='gray', alpha=0.3)
plt.xlim(4.1,21)
plt.plot(X, Y_pred, 'red', label=r'Polynomial fit $R^2={:.2f}$'.format(score_r2))

#df_ambient = df.resample('D').apply({'amb_temp':'mean'})
#plt.plot(df_mean.index, df_ambient['amb_temp'], label='Ambient temperature')

# Rotate tick marks on x-axis
plt.setp(ax.get_xticklabels(), rotation=45)
#ax.set_legend['Forehead temperature', 'Average over a day']
ax.legend()
print(len(df_hours))
#plt.title("Effect of time in the day on forehead temperature")
#more_than_37 = df_outside['obj_score']

#print(len(more_than_37[more_than_37 > more_than_37.mean() + 2*more_than_37.std()]))
plt.tight_layout()

plt.savefig('timeday.png')

fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
df_hours = new_df_all
df_hours['hours'] = df_hours.index.hour


linear_regressor = make_pipeline(
        PolynomialFeatures(degree=2),
        LinearRegression()
        )
linear_regressor.fit(df_hours['hours'].values.reshape(-1, 1), df_hours['obj_score'].values.reshape(-1, 1))
X = np.linspace(df_hours['hours'].min(), df_hours['hours'].max()).reshape(-1, 1)

Y_pred = linear_regressor.predict(X)
score_r2 = linear_regressor.score(df_hours['hours'].values.reshape(-1, 1), df_hours['obj_score'].values.reshape(-1, 1))
print('R2 = ',score_r2)
ax.set_ylim(33,39)

curve = linear_regressor.predict(df_hours['hours'].values.reshape(-1, 1))[:,0]

by_hour = df_hours.groupby(df_hours.index.hour+2).mean()
by_hour_std = df_hours.groupby(df_hours.index.hour+2).std()

df_hours['obj_score'] = df_hours['obj_score']-curve+df_hours['obj_score'].mean()

plt.plot(df_hours['timestamp'], df_hours['obj_score'],'.', alpha=0.1, label='Forehead temperature')
df_mean = df_hours.resample('D').apply({'obj_score':'mean'})
df_std = df_hours.resample('D').apply({'obj_score':'std'})

plt.plot(df_mean.index+pd.Timedelta('0.5 day'), df_mean['obj_score'], label='Average over 24h')

plt.fill_between(df_mean.index+pd.Timedelta('0.5 day'), df_mean['obj_score'] - df_std['obj_score']/2, df_mean['obj_score'] + df_std['obj_score']/2,
                 color='gray', alpha=1.0)

# Set title and labels for axes
ax.set(       ylabel="Forehead temp. (deg. C)", xlabel="Time (days)")
frame1 = plt.gca()
frame1.axes.xaxis.set_ticks([])
#plt.plot(df_hours['amb_temp'], df_hours['obj_score']-curve+df_hours['obj_score'].mean(),'.', alpha=0.1, label='Forehead temperature')

#plt.plot(df_hours.index.hour, df_hours['obj_score'],'.', alpha=0.1, label='Forehead temperature')
#plt.plot(by_hour.index, by_hour['obj_score'],'-', alpha=1.0, label='Temperature average')
#plt.fill_between(by_hour.index, by_hour['obj_score'] - by_hour_std['obj_score']/2, by_hour['obj_score'] + by_hour_std['obj_score']/2,
#                 color='gray', alpha=0.3)
#plt.xlim(4.1,21)
#plt.plot(X, Y_pred, 'red', label=r'Polynomial fit $R^2={:.2f}$'.format(score_r2))

#df_ambient = df.resample('D').apply({'amb_temp':'mean'})
#plt.plot(df_mean.index, df_ambient['amb_temp'], label='Ambient temperature')

# Rotate tick marks on x-axis
plt.setp(ax.get_xticklabels(), rotation=45)
#ax.set_legend['Forehead temperature', 'Average over a day']
ax.legend()
print(len(df_hours))
#plt.title("Correction from outside + ambient + seasonal models")
more_than_37 = df_hours['obj_score']
fig.subplots_adjust(bottom=0.2) 
ax.set_ylim(33,39)

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()  # every month

years_fmt = mdates.DateFormatter('%Y')

ax.xaxis.set_major_locator(months)
ax.xaxis.set_minor_locator(days)

plt.tight_layout()

print(len(more_than_37[more_than_37 > more_than_37.mean() + 2*more_than_37.std()]))
plt.savefig('corrected_outside_ambient_seasonal.png')



print("avg {} std {}".format(df_hours['obj_score'].mean(), df_hours['obj_score'].std()))

groups = df_hours.groupby(['rfid_uid']).std()['obj_score']
print('Personal mean {}, personal std {}'.format(groups.mean(), groups.std()))


print("Location A")
df_filtered = df_hours[df_hours['machine_id'].isin([4428])]
print("len {} avg {} std {}".format(len(df_filtered), df_filtered['obj_score'].mean(), df_filtered['obj_score'].std()))

groups = df_filtered.groupby(['rfid_uid']).std()['obj_score']
print('Personal mean {}, personal std {}'.format(groups.mean(), groups.std()))

print("Location B")
df_filtered = df_hours[df_hours['machine_id'].isin([2952, 3075, 3690, 3813, 3936, 4059, 4182, 4305])]

groups = df_filtered.groupby(['rfid_uid']).std()['obj_score']
print('Personal mean {}, personal std {}'.format(groups.mean(), groups.std()))

print("len {} avg {} std {}".format(len(df_filtered), df_filtered['obj_score'].mean(), df_filtered['obj_score'].std()))
print("Location C")
df_filtered = df_hours[df_hours['machine_id'].isin([5396])]

groups = df_filtered.groupby(['rfid_uid']).std()['obj_score']
print('Personal mean {}, personal std {}'.format(groups.mean(), groups.std()))
print("len {} avg {} std {}".format(len(df_filtered), df_filtered['obj_score'].mean(), df_filtered['obj_score'].std()))
more_than_37 = df_filtered ['obj_score']
print(len(more_than_37[more_than_37 > more_than_37.mean() + 3*more_than_37.std()]))

plt.rcParams["figure.dpi"] = 180
fig, ax = plt.subplots(figsize=(6, 2.5), dpi=180)
df_hours.hist(column=['obj_score'], bins=20, figsize=(6, 3), ax = plt.gca())
ax.set(      ylabel="# Measurements", xlabel="Forehead temperature (degrees C)")
ax.set_title("")
ax.set_xlim(33,39)
# x coordinates for the lines
xcoords = [37.38]
# colors for the lines
colors = ['r']
for xc,c in zip(xcoords,colors):
    plt.axvline(x=xc, label='Fever threshold (μ+3σ = {})'.format(xc), c=c)
fig.subplots_adjust(bottom=0.2) 
plt.legend()
plt.tight_layout()

plt.savefig('hist_corr.png')

print(len(df_filtered_notouch))
print(len(df_hours['obj_score']))




data1     = np.asarray(df_filtered_notouch['obj_score'])
data2     = np.asarray(df_hours['obj_score'])
mean      = np.mean([data1, data2], axis=0)
diff      = -data1 + data2                   # Difference between data1 and data2
md        = np.mean(diff)                   # Mean of the difference
sd        = np.std(diff, axis=0)            # Standard deviation of the difference

print("Mean:  {} SD: {}".format(md.mean(), sd.mean()))

fig, ax = plt.subplots(figsize=(6, 3), dpi=180)

density_scatter(df_hours['obj_score'], diff, ax = ax)
plt.axhline(md,           color='gray', linestyle='--')

ax.annotate('mean diff:\n{}'.format(np.round(md, 2)),
            xy=(0.99, 0.5),
            horizontalalignment='right',
            verticalalignment='center',
            fontsize=10,
            color='red',
            xycoords='axes fraction')
    
plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
plt.axhline(md - 1.96*sd, color='gray', linestyle='--')

ax.annotate('-{}SD: {}'.format(1.96, np.round(md - 1.96*sd, 2)),
            xy=(0.99, 0.08),
            horizontalalignment='right',
            verticalalignment='bottom',
            fontsize=10,
            color='red',
            xycoords='axes fraction')
ax.annotate('+{}SD: {}'.format(1.96, np.round(md + 1.96*sd, 2)),
            xy=(0.99, 0.86),
            horizontalalignment='right',
            fontsize=10,
            color='red',
            xycoords='axes fraction')
        

ax.set(xlabel="Temperature mean (deg. C)",
       ylabel="Correction (deg. C)")

plt.tight_layout()
plt.savefig('bland-altman.png')



fig, ax = plt.subplots(figsize=(6, 3), dpi=180)

density_scatter(df_hours['meteo_realtemp'], diff, ax = ax)
plt.axhline(md,           color='gray', linestyle='--')

ax.annotate('mean diff:\n{}'.format(np.round(md, 2)),
            xy=(0.99, 0.5),
            horizontalalignment='right',
            verticalalignment='center',
            fontsize=10,
            color='red',
            xycoords='axes fraction')
    
plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
plt.axhline(md - 1.96*sd, color='gray', linestyle='--')

ax.annotate('-{}SD: {}'.format(1.96, np.round(md - 1.96*sd, 2)),
            xy=(0.99, 0.08),
            horizontalalignment='right',
            verticalalignment='bottom',
            fontsize=10,
            color='red',
            xycoords='axes fraction')
ax.annotate('+{}SD: {}'.format(1.96, np.round(md + 1.96*sd, 2)),
            xy=(0.99, 0.86),
            horizontalalignment='right',
            fontsize=10,
            color='red',
            xycoords='axes fraction')
        

ax.set(xlabel="Outside temperature (deg. C)",
       ylabel="Correction (deg. C)")

plt.tight_layout()
plt.savefig('bland-altman-outside.png')