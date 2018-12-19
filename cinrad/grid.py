# -*- coding: utf-8 -*-
# Author: Puyuan Du

import numpy as np
from scipy.interpolate import griddata
from pyresample.geometry import GridDefinition
from pyresample.kd_tree import resample_nearest

from .constants import deg2rad

def resample(data, distance, azimuth, d_reso, a_reso):
    r'''
    Resample radar radial data which have different number of radials
    in one scan into that of 360 radials

    Parameters
    ----------
    data: numpy.ndarray
        radar radial data
    distance: numpy.ndarray
        original distance
    azimuth: numpy.ndarray
        original azimuth

    Returns
    -------
    r: numpy.ndarray
        resampled radial data
    dist: numpy.ndarray
        resampled distance
    theta: numpy.ndarray
        resampled azimuth
    '''
    #Target grid
    Rrange = np.arange(d_reso, distance.max() + d_reso, d_reso)
    Trange = np.linspace(0, 360, a_reso + 1) * deg2rad
    dist, theta = np.meshgrid(Rrange, Trange)
    #Original grid
    d, t = np.meshgrid(distance, azimuth)
    r = griddata((d.flatten(), t.flatten()), data.flatten(), (dist, theta), method='nearest')
    return r, dist, theta

def grid_2d(data, x, y, resolution=(1000, 1000)):
    r'''
    Interpolate data in polar coordinates into geographic coordinates

    Parameters
    ----------
    data: numpy.ndarray
        original radial data
    x: numpy.ndarray
        original longitude data arranged in radials
    y: numpy.ndarray
        original latitude data arranged in radials
    resolution: tuple
        the size of output

    Returns:
    r: numpy.ndarray
        interpolated data in grid
    x_cor: numpy.ndarray
        interpolated longitude in grid
    y_cor: numpy.ndarray
        interpolated latitude in grid
    '''
    odf = GridDefinition(x, y)
    r_x, r_y = resolution
    x_cor = np.linspace(x.min(), x.max(), r_x)
    y_cor = np.linspace(y.min(), y.max(), r_y)
    t_x, t_y = np.meshgrid(x_cor, y_cor)
    tdf = GridDefinition(t_x, t_y)
    result = resample_nearest(odf, data, tdf, 2000)
    return result, x_cor, y_cor
