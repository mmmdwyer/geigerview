#!/bin/bash
rrdtool graph radsday.png --start -86400\
            DEF:cpm=rads.rrd:cpm:MAX \
            LINE1:cpm#FF00FF:"Clicks/Min"

rrdtool graph radsweek.png --start -604800\
            DEF:cpm=rads.rrd:cpm:MAX \
            LINE1:cpm#FF00FF:"Clicks/Min"

rrdtool graph radsmonth.png --start -2678400\
            DEF:cpm=rads.rrd:cpm:MAX \
            LINE1:cpm#FF00FF:"Clicks/Min"
