#include <cstdio>
#include <iostream>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace cv;
using namespace std;

Mat src;

int blue_lower = 0;
int blue_upper = 255;
int green_lower = 0;
int green_upper = 255;
int red_lower = 0;
int red_upper = 255;
int max_bgr = 255;

void show_help();
void tuner_callback(int, void*);

int main(int argc, char** argv) {
	if(argc != 2) {
		cout << "Incorrect number arguments!" << endl;
		cout << "Try the --help flag for help." << endl;
		return -1;
	}
	
	if(strcmp(argv[1], "--help") == 0) {
		show_help();
		return 0;
	}
	
	src = imread(argv[1], 1);

	const char* source_window = "Source";
	namedWindow(source_window, CV_WINDOW_AUTOSIZE);
	imshow(source_window, src);

	createTrackbar("Blue Lower:", "Source", &blue_lower, max_bgr, tuner_callback);
	createTrackbar("Blue Upper:", "Source", &blue_upper, max_bgr, tuner_callback);
	createTrackbar("Green Lower:", "Source", &green_lower, max_bgr, tuner_callback);
	createTrackbar("Green Upper:", "Source", &green_upper, max_bgr, tuner_callback);
	createTrackbar("Red Lower:", "Source", &red_lower, max_bgr, tuner_callback);
	createTrackbar("Red Upper:", "Source", &red_upper, max_bgr, tuner_callback);
	
	tuner_callback(0, 0);

	waitKey(0);
	return 0;
}

void tuner_callback(int, void*) {
	Mat output;
	inRange(src, Scalar(blue_lower, green_lower, red_lower), Scalar(blue_upper, green_upper, red_upper), output);
	namedWindow("Mask", CV_WINDOW_AUTOSIZE);
	imshow("Mask", output);
}

void show_help() {
	cout << "Vision tuner program" << endl;
	cout << "  Run: ./tuner PATH-TO-IMAGE" << endl;
	cout << "  Use: Move the sliders around until you see something you like." << endl;
}
