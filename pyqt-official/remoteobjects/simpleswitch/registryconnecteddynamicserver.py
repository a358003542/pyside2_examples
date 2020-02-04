#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2018 Riverbank Computing Limited
## Copyright (C) 2017 Ford Motor Company
##
## This file is part of the PyQt examples.
##
## $QT_BEGIN_LICENSE:BSD$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## BSD License Usage
## Alternatively, you may use this file under the terms of the BSD license
## as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import sys

from PySide2.QtCore import (Property, Signal, Slot, QCoreApplication,
        QObject, QTimer, QUrl)
from PySide2.QtRemoteObjects import QRemoteObjectHost, QRemoteObjectRegistryHost


class SimpleSwitch(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._currState = False

        self._stateChangeTimer = QTimer(self)
        self._stateChangeTimer.timeout.connect(self._timeout)
        self._stateChangeTimer.start(2000)

        print("Source node started")

    # PyQt does not support the use of static source types defined in .rep
    # files.  However we can manually specify a dynamic type that matches a
    # .rep defined type by defining properties, signals and slots in the same
    # order.  We also have to account for any internals also generated by the
    # .rep generator.  At the moment this only includes an extra 'push' slot
    # for each property (that never seems to get called).  This allows this
    # example to act as a server for Qt's C++ 'directconnectclient' example.
    # It is not necessary when using with clients that use dynamic source types
    # (written using either C++ or Python).
    @Slot()
    def pushCurrState(self, currState):
        pass

    def _get_currState(self):
        return self._currState

    def _set_currState(self, value):
        # If the value has changed then update it and emit the notify signal.
        if self._currState != value:
            self._currState = value
            self.currStateChanged.emit(value)

    # The property's notify signal.
    currStateChanged = Signal(bool)

    # The property exposed to a remote client.
    currState = Property(bool, fget=_get_currState, fset=_set_currState,
            notify=currStateChanged)

    # The slot exposed to a remote client.
    @Slot(bool)
    def server_slot(self, clientState):
        # The switch state echoed back by the client.
        print("Replica state is", clientState)

    def _timeout(self):
        # Note that we don't decorate this callable so that it doesn't get
        # exposed in a replica.
        self.currState = not self.currState

        print("Source state is", self.currState)


if __name__ == '__main__':

    app = QCoreApplication(sys.argv)

    # Create the simple switch.
    srcSwitch = SimpleSwitch()

    # Create the node that hosts the registry.  This could be in a separate
    # process.
    regNode = QRemoteObjectRegistryHost(QUrl('local:registry'))

    # Create the host object node.  This will connect to the registry node
    # rather than to a client.
    srcNode = QRemoteObjectHost(QUrl('local:replica'), QUrl('local:registry'))

    # Enable remoting.
    srcNode.enableRemoting(srcSwitch, 'SimpleSwitch')

    sys.exit(app.exec_())
