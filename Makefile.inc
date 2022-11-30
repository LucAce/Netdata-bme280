# SPDX-License-Identifier: GPL-3.0-or-later

# install these files
dist_python_DATA       += bme280/bme280.chart.py
dist_pythonconfig_DATA += bme280/bme280.conf

# do not install these files, but include them in the distribution
dist_noinst_DATA       += bme280/README.md bme280/Makefile.inc
