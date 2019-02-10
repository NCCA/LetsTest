
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
