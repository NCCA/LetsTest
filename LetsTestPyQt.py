#!/usr/bin/env python

from __future__ import print_function
import os,sys

from PyQt5.QtWidgets import (QLabel,QLineEdit, QApplication,QFileDialog, QMainWindow,QMessageBox,QGroupBox,QPushButton,QVBoxLayout,QRadioButton)

class MainWindow(QMainWindow):
  def __init__(self):
    self.directory=None
    super(MainWindow, self).__init__()
    self.gridGroupBox = QGroupBox("Settings")
    layout = QVBoxLayout()
    self.setWindowTitle('Lets Test! A simple gtest code generator tool')
    nameLabel=QLabel('Class / Method Name') 
    layout.addWidget(nameLabel)
    self.className=QLineEdit() 
    self.className.setText('')
    layout.addWidget(self.className)
    # radio buttons
    self.radio1 = QRadioButton("Class")
    self.radio1.setChecked(True)
    self.radio2 = QRadioButton("Function")
    layout.addWidget(self.radio1)
    layout.addWidget(self.radio2)
    self.selectedDir=QLabel('') 
    layout.addWidget(self.selectedDir)

    self.selectDir=QPushButton('Select Directory')
    layout.addWidget(self.selectDir)
    self.generate=QPushButton('Generate')
    layout.addWidget(self.generate)
		# connect buttons to methods
    self.selectDir.clicked.connect(self.chooseDir)
    self.generate.clicked.connect(self.generateFiles)


    # add stuff to layouts etc
    self.gridGroupBox.setLayout(layout)
    self.setCentralWidget(self.gridGroupBox)



  def chooseDir(self):
    self.directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    self.selectedDir.setText(self.directory)

  def generateFiles(self):
    if self.directory == None :
			msg=QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Directory Not Set")
			msg.setInformativeText("You need to choose a directory to put the files into")
			return msg.exec_()

    if len(self.className.text()) == 0 :
			msg=QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Class / Method name not set")
			msg.setInformativeText("please set a default Class / Method name for the code generation")
			return msg.exec_()
    cwd=self.directory+'/'+self.className.text()
    if os.path.isdir(cwd) :
      showinfo("Error", "Directory Already Exists")
      return
    os.mkdir(cwd)
    os.chdir(cwd)
    self.writeMakefile()
    if self.radio1.isChecked() :
      self.writeClassHeader()
      self.writeClassCpp()
      self.writeTestFileClass()
    else:
      self.writeFunctionHeader()
      self.writeFunctionCpp()
      self.writeTestFileFunction()
    sys.exit(0)


  def writeMakefile(self) :
    makefile='''
# Modified and inspired by cyber-dogo.org
CXX= g++
CXXFLAGS += -I.
CXXFLAGS += -std=c++1z
CXXFLAGS += -Wall -Wextra 
CXXFLAGS += -g

GTEST_LIBS = -lgtest -lgtest_main -pthread

HPP_FILES = $(wildcard *.h)
COMPILED_HPP_FILES = $(patsubst %.h,%.compiled_hpp,$(HPP_FILES))
CPP_FILES = $(wildcard *.cpp)

.PHONY: test.output
test.output: test makefile
	@./$< --gtest_shuffle

test: makefile $(CPP_FILES) $(COMPILED_HPP_FILES)
	@$(CXX) $(CXXFLAGS) -O $(CPP_FILES) $(GTEST_LIBS) -o $@

# This rule ensures header files build in their own right.
# The quality of header files is important because header files
# are #included from other files and thus have a large span
# of influence (unlike .cpp files which are not #included)

%.compiled_hpp: %.h
	@$(CXX) -x c++ $(CXXFLAGS) -c -o $@ $<
'''
    with open('Makefile', 'w') as currentFile:
      currentFile.write(makefile)

  def writeClassHeader(self) :
    header='''
#ifndef {0}_H
#define {0}_H
class {1}
{{
  public :
    {1}()=default;
    ~{1}() noexcept =default;
    {1}(const {1} &)=default;
    {1} & operator=(const {1} &)=default;
    {1}({1} &&)=default;
    {1} & operator=({1} &&)=default;
}};

#endif
'''.format(self.className.text().upper(),self.className.text())
    with open(self.className.text()+'.h', 'w') as currentFile:
      currentFile.write(header)


  def writeClassCpp(self) :
    cppfile='''
#include "{}.h"
'''.format(self.className.text())

    with open(self.className.text()+'.cpp', 'w') as currentFile:
      currentFile.write(cppfile)
  
  
  
  def writeFunctionHeader(self) :
    header='''
#ifndef {0}_H
#define {0}_H
  extern int {1}();

#endif
'''.format(self.className.text().upper(),self.className.text())
    with open(self.className.text()+'.h', 'w') as currentFile:
      currentFile.write(header)

  def writeFunctionCpp(self) :
    cppfile='''
#include "{0}.h"
int {0}()
{{
  return -99;
}}
'''.format(self.className.text())

    with open(self.className.text()+'.cpp', 'w') as currentFile:
      currentFile.write(cppfile)
  
  
  
  def writeTestFileClass(self) :
    testFile='''
#include "{0}.h"
#include <gtest/gtest.h>
using namespace ::testing;

TEST({0}, fail)
{{
    ASSERT_EQ(0,1);
}}
'''.format(self.className.text())

    with open(self.className.text()+'Tests.cpp', 'w') as currentFile:
      currentFile.write(testFile)

  
  def writeTestFileFunction(self) :
    testFile='''
#include "{0}.h"
#include <gtest/gtest.h>
using namespace ::testing;

TEST({0}, fail)
{{
    ASSERT_EQ({0}(),0);
}}
'''.format(self.className.text())

    with open(self.className.text()+'Tests.cpp', 'w') as currentFile:
      currentFile.write(testFile)



# Below runs the "main" function
if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.resize(400,200)
	mainWin.show()
	sys.exit(app.exec_())    

 
