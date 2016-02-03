ifeq ($(RELEASE), yes)
	CXXFLAGS=-march=native -O2 -pipe -std=c++11 -Wall -Wextra
else
	CXXFLAGS=-pipe -std=c++11 -Wall -Wextra
endif

CXX=g++
LIBS=-lntcore -lopencv_core -lopencv_highgui -lopencv_imgproc
OBJS=calculate_pos.o detect_highgoals.o networking.o
RM=rm -rfv

all: detect_highgoals

detect_highgoals: $(OBJS)
	g++ $(OBJS) -o detect_highgoals $(LIBS)
ifeq ($(RELEASE), yes)
	strip $@
endif

%.o: %.cpp
	$(CXX) -c $< -o $@ $(CXXFLAGS) $(LIBS)

clean:
	$(RM) detect_highgoals
	$(RM) *.o
