# -*- coding: utf-8 -*-

# Resource object code
#
# Created: Wed May 15 17:17:52 2013
#      by: The Resource Compiler for PyQt (Qt v5.0.2)
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore

qt_resource_data = b"\
\x00\x00\x00\xae\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x10\x00\x00\x00\x10\x04\x03\x00\x00\x00\xed\xdd\xe2\x52\
\x00\x00\x00\x0f\x50\x4c\x54\x45\xc0\xc0\xc0\xc0\xc0\xc0\xc0\xc0\
\xc0\xff\xff\xff\x00\x00\x00\x63\x34\x8b\x60\x00\x00\x00\x03\x74\
\x52\x4e\x53\x00\x01\x02\x0d\x63\x94\xb3\x00\x00\x00\x4b\x49\x44\
\x41\x54\x78\x5e\x3d\x8a\xc1\x0d\xc0\x30\x0c\x02\x1d\x89\x01\xba\
\x8b\x3d\x40\x54\xb3\xff\x4c\x05\xa7\x0a\x0f\x74\xe6\x1c\x41\xf2\
\x89\x58\x81\xcc\x7c\x0d\x2d\xa8\x50\x06\x96\xc0\x6a\x63\x9f\xa9\
\xda\x12\xec\xd2\xa8\xa5\x40\x03\x5c\x56\x06\xfc\x6a\xfe\x47\x0d\
\xb8\x2e\x50\x39\xde\xf1\x65\xf8\x00\x49\xd8\x14\x02\x64\xfa\x65\
\x99\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x06\
\x07\x03\x7d\xc3\
\x00\x69\
\x00\x6d\x00\x61\x00\x67\x00\x65\x00\x73\
\x00\x0d\
\x0f\x7f\xc5\x07\
\x00\x69\
\x00\x6e\x00\x74\x00\x65\x00\x72\x00\x76\x00\x69\x00\x65\x00\x77\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x12\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
