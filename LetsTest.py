#!/usr/bin/env python

from __future__ import print_function
import os,sys
try:
  from Tkinter import *
  from tkFileDialog import askdirectory
  from tkMessageBox import showinfo
except ImportError:
  from tkinter import *


class LetsTestGUI:
  def __init__(self, master):
    self.directory=None
    self.master = master
    master.title("C++ Unit Test Generator")
    self.label = Label(master, text="Name of Class or Method")
    self.label.pack()
    self.className = StringVar()
    self.textEntry = Entry(master, textvariable=self.className)
    self.textEntry.pack()
    self.classOrFunc = IntVar()
    Radiobutton(master, text="Class", variable=self.classOrFunc, value=1).pack(anchor=W)
    Radiobutton(master, text="Function", variable=self.classOrFunc, value=2).pack(anchor=W)

    self.projDir = Button(master, text="Choose Project Directory", command=self.chooseDir)
    self.projDir.pack()
    self.generateFiles = Button(master, text="Generate Files", command=self.generateFiles)
    self.generateFiles.pack()

    self.close_button = Button(master, text="Quit", command=master.quit)
    self.close_button.pack()
    
  def chooseDir(self):
    self.directory = askdirectory()

  def generateFiles(self):
    if self.directory == None :
      showinfo("Error", "Please select a directory")
      return 
    if len(self.className.get()) == 0 :
      showinfo("Error", "Please enter a class or method name")
      return 
    cwd=self.directory+'/'+self.className.get()
    if os.path.isdir(cwd) :
      showinfo("Error", "Directory Already Exists")
      return
    os.mkdir(cwd)
    os.chdir(cwd)
    self.writeMakefile()
    self.writeClassHeader()
    self.writeClassCpp()
    self.writeTestFile()
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
'''.format(self.className.get().upper(),self.className.get())
    with open(self.className.get()+'.h', 'w') as currentFile:
      currentFile.write(header)
  def writeClassCpp(self) :
    cppfile='''
#include "{}.h"
'''.format(self.className.get())

    with open(self.className.get()+'.cpp', 'w') as currentFile:
      currentFile.write(cppfile)
  def writeTestFile(self) :
    testFile='''
#include "{0}.h"
#include <gtest/gtest.h>
using namespace ::testing;

TEST({0}, fail)
{{
    ASSERT_EQ(0,1);
}}
'''.format(self.className.get())

    with open(self.className.get()+'Tests.cpp', 'w') as currentFile:
      currentFile.write(testFile)



root = Tk()
my_gui = LetsTestGUI(root)
root.mainloop()


 
