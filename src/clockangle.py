import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def parse_data(listfile):

	data = np.genfromtxt(listfile)
	by = data[:,4]
	bz = data[:,5]
	alfven = data[:,6]
	by[by == 9999.99] = np.nan
	bz[bz == 9999.99] = np.nan
	alfven[alfven == 999.9] = np.nan

	clockangle = np.arctan2(by,bz)

	date = []
	datea = []
	dateb = []

	for i, item in enumerate(data):
		year = int(data[:,0][i])
		doy = int(data[:,1][i])
		hour = int(data[:,2][i])
		minute = int(data[:,3][i])
		date.append(datetime(year, 1, 1) + timedelta(days = doy - 1, hours = hour, minutes = minute))

	diff = []
	i = 0
	'''
	while i < len(clockangle)-2:
		diff.append(clockangle[i+1]-clockangle[i])
		i += 1

	while i < len(clockangle)-2:
		if (-clockangle[i+2] + 8*clockangle[i+1] - 8*clockangle[i-1] + clockangle[i-2])/12 > 180:
			diff.append(360-((-clockangle[i+2] + 8*clockangle[i+1] - 8*clockangle[i-1] + clockangle[i-2])/12))
		elif (-clockangle[i+2] + 8*clockangle[i+1] - 8*clockangle[i-1] + clockangle[i-2])/12 < -180:
			diff.append(((-clockangle[i+2] + 8*clockangle[i+1] - 8*clockangle[i-1] + clockangle[i-2])/12)+360)
		else:
			diff.append((-clockangle[i+2] + 8*clockangle[i+1] - 8*clockangle[i-1] + clockangle[i-2])/12)
		i += 1

	
	while i < len(clockangle)-1:
		if (clockangle[i+1] - clockangle[i-1])/2 > 180:
			diff.append(360-(clockangle[i+1] - clockangle[i-1])/2)
		elif (clockangle[i+1] - clockangle[i-1])/2 < -180:
			diff.append((clockangle[i+1] - clockangle[i-1])/2+360)
		else:
			diff.append((clockangle[i+1] - clockangle[i-1])/2)
		i += 1
	'''

	while i < len(clockangle) - 2:
		diff.append((-by[i+2] + 8*by[i+1] - 8*by[i-1] + by[i-2])/12)
		i+=1

	diff.append(np.nan)
	diff.append(np.nan)
	
	i=0
	'''
	while i < len(diff):
		if diff[i] > np.pi:
			diff[i] = 2*np.pi - diff[i]
		if diff[i] < -np.pi:
			diff[i] = 2*np.pi + diff[i]
		i+=1
	'''
	indices = [i for i, x in enumerate(alfven) if x < 1.3]
	
	for item in indices:
		datea.append(date[item])
	
	magnitude = [abs(value) for value in diff]

	for num, item in enumerate(magnitude):
		if item > 10:
			dateb.append(date[num])
	
	for date in datea:
		if date in dateb:
			print(date)
		
	print(set(datea).intersection(dateb))

parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1981a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1982a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1983a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1984a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1985a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1986a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1987a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1988a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1989a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1990a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1991a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1992a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1993a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1994a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1995a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1996a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1997a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1998a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_1999a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2000a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2001a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2002a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2003a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2004a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2005a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2006a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2007a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2008a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2009a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2010a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2011a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2012a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2013a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2014a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2015a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2016a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2017a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2018a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2019a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2020a.lst')
parse_data('//wsl$/Ubuntu/home/rdl6937/precursorDB/data/omni/omni_2021a.lst')
