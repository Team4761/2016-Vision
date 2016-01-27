ifeq ($(RELEASE), yes)
	CXXFLAGS=-march=native -O2 -pipe -std=c++11 -Wall -Wextra
else
	mode=debug
	CXXFLAGS=-pipe -std=c++11 -Wall -Wextra
endif

CXX=g++
LIBS=-lopencv_core -lopencv_highgui -lopencv_imgproc
OBJS=detect_highgoals.o

all: detect_highgoals

detect_highgoals: $(OBJS)
	g++ $(OBJS) -o detect_highgoals $(LIBS)
ifeq ($(RELEASE), yes)
	strip $@
endif

%.o: %.cpp
	$(CXX) -c $< -o $@ $(CXXFLAGS) $(LIBS)

help:
	@echo "Targets"
	@echo " * all: build everything"
	@echo " * get-target-images: download + unzip some sample images"
	@echo " * help: show this help message"
	@echo "extra info:"
	@echo " * on raspi, build with RELEASE=yes"
