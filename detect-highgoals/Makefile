ifeq ($(RELEASE), yes)
	CXXFLAGS=-march=native -O2 -pipe -std=c++11 -Wall -Wextra
else
	mode=debug
	CXXFLAGS=-pipe -std=c++11 -Wall -Wextra
endif

CXX=g++
LIBS=-lopencv_core -lopencv_highgui -lopencv_imgproc
EXECUTABLES=detect_highgoals

all: $(EXECUTABLES)

%: %.cpp
	$(CXX) $< -o $@ $(CXXFLAGS) $(LIBS)
ifeq ($(RELEASE), yes)
	strip $@
endif

get-target-images:
	curl -o RealFullField.zip https://usfirst.collab.net/sf/frs/do/downloadFile/projects.wpilib/frs.2016_field_images.vision_target_images_for_2016/frs1207?dl=1
	unzip -q RealFullField.zip
	rm -rf __MACOSX RealFullField.zip RealFullField/.DS_Store
	chmod -x RealFullField/*.jpg

help:
	@echo "Targets"
	@echo " * all: build everything"
	@echo " * get-target-images: download + unzip some sample images"
	@echo " * help: show this help message"
	@echo "extra info:"
	@echo " * on raspi, build with RELEASE=yes"
