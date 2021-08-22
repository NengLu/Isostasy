#!/usr/bin/env python
# coding: utf-8
#
# Neng Lu
# nengl@student.unimelb.edu.au
# ANU & Unimelb
# Canberra, Australia

import numpy as np
import math
import stripy
from osgeo import gdal
from osgeo import osr

def testimport():
    print("It works!")

#-----------------------------------------------------------#
# data=(ny,nx) version
def array2geotiff_yx(fname, data, latRange, lonRange, dtype):   
    """
    save GeoTiff file from the array of dem data
    input:
    fname: save file name
    data: elevation data, an array in size of (n_lat,n_lon) 
    latRange: range of latitude, an array as [minlat,maxlat]
    lonRange: range of longitude, an array as [minlon,maxlon]
    dtype: dtype in gdal, as gdal.GDT_Byte or gdal.GDT_Float32
    """   
    nx = data.shape[1]
    ny = data.shape[0]
    xmin,xmax,ymin,ymax = [lonRange[0],lonRange[1],latRange[0],latRange[1]]
    dx = (xmax - xmin) / float(nx)
    dy = (ymax - ymin) / float(ny)
    geotransform = (xmin, dx, 0, ymax, 0, -dy)
    dst = gdal.GetDriverByName('GTiff').Create(fname, nx, ny, 1, dtype)
    dst.SetGeoTransform(geotransform) 
    dst.GetRasterBand(1).WriteArray(data)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    dst.SetProjection(srs.ExportToWkt())  
    dst.FlushCache() 
    
def loadxyz2grd(fname,order,dlon,dlat):
    """
    load .xyz file to grid
    input:
    fname: load file name
    order: the squence of lons and lats saving in .xyz 
    dlon:
    dlat: 
    
    data: elevation data, an array in size of (n_lat,n_lon) 
    latRange: range of latitude, an array as [minlat,maxlat]
    lonRange: range of longitude, an array as [minlon,maxlon]
    dtype: dtype in gdal, as gdal.GDT_Byte or gdal.GDT_Float32
    """ 
    data = np.loadtxt(fname)
    if order == "lonlat":
        lons,lats,z = data[:,0],data[:,1],data[:,2]
    if order == "latlon":
        lats,lons,z = data[:,0],data[:,1],data[:,2]
    minlon,maxlon,minlat,maxlat = lons.min(),lons.max(),lats.min(),lats.max()
    extent = (minlon,maxlon,minlat,maxlat)
    nlon = int((maxlon-minlon)/dlon+1)
    nlat = int((maxlat-minlat)/dlat+1)
    size = nlon*nlat
    data = np.zeros((nlat,nlon))
    for i in range(size):
        lon_idx = np.around((lons[i]-minlon)/dlon).astype("int")
        lat_idx = np.around((lats[i]-maxlat)/dlat).astype("int")
        data[lat_idx,lon_idx]=z[i]
    return data,extent

def xyz2grd(lons,lats,dlon,dlat,data_xyz):
    minlon,maxlon,minlat,maxlat = lons.min(),lons.max(),lats.min(),lats.max()
    nlon = int((maxlon-minlon)/dlon+1)
    nlat = int((maxlat-minlat)/dlat+1)
    size = nlon*nlat
    data_grd = np.zeros((nlat,nlon))
    for i in range(size):
        lon_idx = np.around((lons[i]-minlon)/dlon).astype("int")
        lat_idx = np.around((lats[i]-maxlat)/dlat).astype("int")
        data_grd[lat_idx,lon_idx]=data_xyz[i]
    return data_grd    
    
def interp2grid(extent0,dx0,dy0,data0,extent1,dx1,dy1,order): 
    """
    extent0,dx0,dy0,data0: source data
    extent1,dx1,dy1: target data
    """
    square0  = stripy.cartesian_meshes.square_mesh(extent0, dx0, dy0,refinement_levels=0)
    xmin0, xmax0, ymin0, ymax0 = extent0    
    data = np.zeros(square0.npoints)
    for i in range(square0.npoints):
        x = square0.x[i]
        y = square0.y[i]
        idx = np.around((x-xmin0)/dx0).astype(int)
        idy = np.around((y-ymin0)/dy0).astype(int)
        data[i] = data0[idy,idx]
    
    xmin1, xmax1, ymin1, ymax1 = extent1
    grid_x = np.arange(xmin1, xmax1+dx1/2, dx1)
    grid_y = np.arange(ymin1, ymax1+dy1/2, dy1)
    grid_xcoords, grid_ycoords = np.meshgrid(grid_x, grid_y)
    data1, ierr = square0.interpolate(grid_xcoords.ravel(), grid_ycoords.ravel(), data, order=order)
    nx = grid_x.shape[0]
    ny = grid_y.shape[0]
    data1 = data1.reshape(ny,nx)
    return data1
    
def get_closest_grid(extent0,dx0,dy0,data0,extent1,dx1,dy1):
    """
    extent0,dx0,dy0,data0: source data
    extent1,dx1,dy1: target data
    """

    xmin0, xmax0, ymin0, ymax0 = extent0 
    x1 = np.arange(extent1[0],extent1[1]+dx1/4,dx1)
    y1 = np.arange(extent1[2],extent1[3]+dy1/4,dy1) 
    
    x0 = np.arange(extent0[0],extent0[1]+dx0/4,dx0)
    y0 = np.arange(extent0[2],extent0[3]+dy0/4,dy0) 
    
    nx1 = len(x1)
    ny1 = len(y1)

    data1 = np.zeros((ny1,nx1))
    xid = np.zeros(nx1)
    yid = np.zeros(ny1)
    
    for i in range(nx1):
        xid[i] = (np.abs(x0 - x1[i])).argmin()
    for j in range(ny1):
        yid[j] = (np.abs(y0 - y1[j])).argmin()
            
    for i in range(nx1):
        for j in range(ny1):
            data1[j,i] = data0[yid[j].astype(int),xid[i].astype(int)]
           
    return data1
    
def lonlat_2_rowcol(lon,lat,extent,cellsize):
    minlon = extent[0]
    col = np.around((lon-minlon)/cellsize).astype(int)
    #minlat = extent[2]
    #row = np.around((lat-minlat)/cellsize).astype(int)
    maxlat = extent[3]
    row = np.around((maxlat-lat)/cellsize).astype(int)
    return row, col

def lonlat_2_ind(lon,lat,extent,cellsize,dims):
    row,col = lonlat_2_rowcol(lon,lat,extent,cellsize)
    ind = np.ravel_multi_index((row, col), dims) 
    return ind

def rowcol_2lonlat(row,col,extent,cellsize):
    lons = np.arange(extent[0],extent[1]+cellsize/4,cellsize)
    lats = np.arange(extent[2],extent[3]+cellsize/4,cellsize)
    _lats = lats[::-1]
    lon = lons[col]
    lat = _lats[row]
    return lon,lat

def ind_2_lonlat(ind,extent,cellsize,dims):
    row,col = np.unravel_index(ind, dims)
    lon,lat = rowcol_2lonlat(row,col,extent,cellsize)
    return lon,lat
      
def cal_azi(x1,y1,x2,y2):
    y = y2-y1
    x = x2-x1
    azi = math.atan2(y, x) * 180 / math.pi
    azi = float((-azi + 90.0) % 360.0)
    return azi
    
def cal_dis_LngLat(lon1,lat1,lon2,lat2):
    if lon1 == lon2 and lat1 == lat2:
    	d=0
    else:	
    	latitude1 = (math.pi/180)*lat1
    	latitude2 = (math.pi/180)*lat2
    	longitude1 = (math.pi/180)*lon1
    	longitude2= (math.pi/180)*lon2
   	 #{arccos[sinb*siny+cosb*cosy*cos(a-x)]}*R
    	R = 6378.137
    	d = math.acos(math.sin(latitude1)*math.sin(latitude2)+ math.cos(latitude1)*math.cos(latitude2)*math.cos(longitude2-longitude1))*R
    return d
