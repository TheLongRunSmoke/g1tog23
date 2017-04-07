#!/usr/bin/python

#    Copyright 2013 Frank Tkalcevic (frank@franksworkshop.com.au)
#    Copyright 2016 Alexey Hohlov (root@amper.me)
#    Copyright 2017 thelongrunsmoke (thelongrunsmoke@gmail.com)
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# Version 1.1
# 	- Fix problem not picking up F word
# Version 1.2
# 	- Adding E argument and calculation for E, ignoring not changed positions
# Version 1.3
# 	- Migerate to py3.x

import os
import re
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar

from author import douglas

plane = 17
point_tolerance = 0.05
length_tolerance = 0.005

output_file = ""


def output_line(s):
    if output_file == "":
        print(s)
    else:
        with open(output_file, "a") as myfile:
            myfile.write(s + "\n")


class Gcode(object):
    prevx = 0
    prevy = 0
    prevz = 0
    preva = 0
    prevf = 0
    preve = 0

    def __init__(self):
        self.regMatch = {}
        self.line_count = 0
        self.output_line_count = 0
        self.input_line_count = 0
        self._fileSize = None

    def load(self, filename):
        if os.path.isfile(filename):
            self._fileSize = os.stat(filename).st_size
            with open(filename, 'r') as file:
                self.input_line_count = sum(1 for line in file)
            gcodeFile = open(filename, 'r')
            self._load(gcodeFile)
            gcodeFile.close()

    def load_list(self, l):
        self._load(l)

    def _load(self, gcode_file):

        st = []
        lastx = 0
        lasty = 0
        lastz = 0
        lasta = 0
        lastf = 0
        laste = 0
        self.line_count = 0
        self.output_line_count = 0

        for line in gcode_file:
            self.line_count = self.line_count + 1
            ui.set_progress(int(self.line_count/self.input_line_count*100))
            line = line.rstrip()
            original_line = line
            if type(line) is tuple:
                line = line[0]

            if ';' in line or '(' in line:
                sem_pos = line.find(';')
                par_pos = line.find('(')
                pos = sem_pos
                if pos is None:
                    pos = par_pos
                elif par_pos is not None:
                    if par_pos > sem_pos:
                        pos = par_pos
                line = line[0:pos]

            # we only try to simplify G1 coordinated moves
            G = self.get_code_int(line, 'G')
            if G == 1:  # Move
                x = self.get_code_float(line, 'X')
                y = self.get_code_float(line, 'Y')
                z = self.get_code_float(line, 'Z')
                a = self.get_code_float(line, 'A')
                f = self.get_code_float(line, 'F')
                e = self.get_code_float(line, 'E')

                if x is None and y is None and e is not None or f is not None:
                    if len(line) > 0 and len(st) > 0:
                        self.simplify_path(st)
                        st = []

                if x is None:
                    x = lastx
                if y is None:
                    y = lasty
                if z is None:
                    z = lastz
                if a is None:
                    a = lasta
                if f is None:
                    f = lastf
                if e is None:
                    e = laste

                st.append([x, y, z, a, f, e])

                lastx = x
                lasty = y
                lastz = z
                lasta = a
                lastf = f
                laste = e
            else:
                # any other move signifies the end of a list of line segments,
                # so we simplify them.

                if G == 92:
                    laste = self.get_code_float(line, 'E')
                    self.preve = laste

                if G == 0:  # Rapid - remember position
                    x = self.get_code_float(line, 'X')
                    y = self.get_code_float(line, 'Y')
                    z = self.get_code_float(line, 'Z')
                    a = self.get_code_float(line, 'A')
                    f = self.get_code_float(line, 'F')

                    if x is not None:
                        lastx = x
                    if y is not None:
                        lasty = y
                    if z is not None:
                        lastz = z
                    if a is not None:
                        lasta = a
                    if f is not None:
                        lastf = f

                if len(line) > 0 and len(st) > 0:
                    self.simplify_path(st)
                    st = []
                output_line(original_line)
                self.output_line_count = self.output_line_count + 1

        if len(st) != 0:
            self.simplify_path(st)

        output_line("; GCode file processed by " + sys.argv[0])
        output_line("; Input Line Count = " + str(self.line_count))
        output_line("; Output Line Count = " + str(self.output_line_count))
        if self.output_line_count < self.line_count:
            output_line(
                "; Line reduction = " + str(100 * (self.line_count - self.output_line_count) / self.line_count) + "%")

    def get_code_int(self, line, code):
        if code not in self.regMatch:
            self.regMatch[code] = re.compile(code + '([^\s]+)', flags=re.IGNORECASE)
        m = self.regMatch[code].search(line)
        if m is None:
            return None
        try:
            return int(m.group(1))
        except (IndexError, ValueError):
            return None

    def get_code_float(self, line, code):
        if code not in self.regMatch:
            self.regMatch[code] = re.compile(code + '([^\s]+)', flags=re.IGNORECASE)
        m = self.regMatch[code].search(line)
        if m is None:
            return None
        try:
            return float(m.group(1))
        except (IndexError, ValueError):
            return None

    def simplify_path(self, st):
        # print("st= %i" % len(st))
        l = douglas(st, plane=plane, tolerance=point_tolerance, length_tolerance=length_tolerance)
        for i, (g, p, c) in enumerate(l):
            self.output_line_count = self.output_line_count + 1
            s = g + " "
            if p[0] is not None:
                if p[0] is not self.prevx:
                    s = s + "X{0:.3f}".format(p[0]) + " "
                    self.prevx = p[0]
            if p[1] is not None:
                if p[1] is not self.prevy:
                    s = s + "Y{0:.3f}".format(p[1]) + " "
                    self.prevy = p[1]
            if p[2] is not None:
                if p[2] != self.prevz:
                    s = s + "Z{0:.3f}".format(p[2]) + " "
                    self.prevz = p[2]
            if p[3] is not None:
                if p[3] is not self.preva:
                    s = s + "A{0:.3f}".format(p[3]) + " "
                    self.preva = p[3]
            if p[5] is not None:
                if p[5] is not self.preve:
                    s = s + "E{0:.5f}".format(p[5]) + " "
                    self.preve = p[5]
            if p[4] is not None:
                if p[4] is not self.prevf:
                    s = s + "F{0:.3f}".format(p[4]) + " "
                    self.prevf = p[4]
            if c is not None:
                s = s + c
            s = s.rstrip()
            output_line(s)


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pbar = QProgressBar(self)
        self.set_closable()
        self.setWindowTitle('G1toG23')
        self.show()

    def set_unclosable(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowSystemMenuHint)

    def set_closable(self):
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowCloseButtonHint)

    def set_progress(self, progress):
        if 0 <= progress <= 100:
            self.pbar.setValue(progress)


def process(output):
    """
    Process input file if specifed.
    """
    input_file = output + ".bak"
    if os.path.isfile(input_file):
        os.remove(input_file)
    os.rename(output, input_file)
    Gcode().load(input_file)
    # ui.close()
    # else:
    # ui.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = GUI()
    if len(sys.argv) > 1:
        # ui.set_unclosable()
        output_file = sys.argv[1]
        process(output_file)  # Not best practice, will refactor later.
    sys.exit(app.exec_())
