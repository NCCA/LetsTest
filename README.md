# LetsTest

A simple python based gui to create simple C++ files for tests using gtest for either classes or functions.

This has been inspired by [Cyber Dojo](https://cyber-dojo.org/) where you can get a simple framework of code for testing.

This has mainly been designed as a simple framework for students to concentrate on basic Test Driven Development (TDD) in the Labs 

![demo](images/demo.gif)

The generated files can be seen in the Vec3 directory.

## Makefile

```

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

```

## Headers

```

#ifndef VEC3_H
#define VEC3_H
class Vec3
{
  public :
    Vec3()=default;
    ~Vec3() noexcept =default;
    Vec3(const Vec3 &)=default;
    Vec3 & operator=(const Vec3 &)=default;
    Vec3(Vec3 &&)=default;
    Vec3 & operator=(Vec3 &&)=default;
};

#endif
```

## CPP Files

```
#include "Vec3.h"
```

Test file

```

#include "Vec3.h"
#include <gtest/gtest.h>
using namespace ::testing;

TEST(Vec3, fail)
{
    ASSERT_EQ(0,1);
}

```