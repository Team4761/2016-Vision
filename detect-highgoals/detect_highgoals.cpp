/*
 * detect_highgoals.cpp
 * 
 * Program for detecting highgoals for the 2016 game (Stronghold). Run
 * with "./detect_highgoals YOURFILE" where "YOURFILE" is the path to
 * the image file.
 * 
 * Compile with "make" or "make RELEASE=yes" depending on what flags you
 * wish to compile with. See "make help" for more information.
 */

#include <cstdio>
#include <iostream>
#include <memory>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <string>

using namespace cv;
using namespace std;

/*
 * Struct for containing the return value for get_bounding_shapes(). I
 * think this is justifiable in this case since the values are very
 * closely related.
 */
struct bounding_shapes_return {
	Rect rectangle;
	Point2f circle_center;
	float circle_radius;
	
};

//Constants
const Scalar color_lbound = Scalar(101, 99, 0);
const Scalar color_ubound = Scalar(255, 255, 121);
const Scalar contour_color = Scalar(255, 255, 255); //white
const string window_name = "Highgoal Detection Demo";
const string json_format = "{\"rectangle\":{\"top_left\":{\"x\":%d,\"y\":%d},\"width\":%d,\"height\":%d},\"circle\":{\"center\":{\"x\":%g,\"y\":%g},\"radius\":%g}}";

//Function prototypes
bounding_shapes_return get_bounding_shapes(Mat);
void print_results_as_json(bounding_shapes_return in);
void show_results(Size, bounding_shapes_return);
template<typename ... Args> string string_format(const string&, Args ...);

int main(int argc, char **argv) {
	if(argc != 2) {
		cout << "Incorrect number of arguments!" << endl;
		return -1;
	}
	Mat image = imread(argv[1], 1);
	if(!image.data) {
		cout << "No image data!" << endl;
		return -1;
	}
	namedWindow(window_name, CV_WINDOW_AUTOSIZE);
	bounding_shapes_return shapes = get_bounding_shapes(image);
	print_results_as_json(shapes);
}

/*
 * Image goes in, gets run through a few filters and a final result pops
 * out, contained in a struct.
 */
bounding_shapes_return get_bounding_shapes(Mat input_img) {
	Mat rgb_out;
	inRange(input_img, color_lbound, color_ubound, rgb_out);
	
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;
	findContours(rgb_out, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
	
	vector<vector<Point>> contours_poly(contours.size());
	vector<Rect> boundRect(contours.size());
	vector<Point2f> center(contours.size());
	vector<float> radius(contours.size());
	
	Rect largestRect;
	Point2f largestCircleCenter;
	float largestCircleRadius;
	for(unsigned int i = 0; i < contours.size(); i++) {
		approxPolyDP(Mat(contours[i]), contours_poly[i], 3, true);
		boundRect[i] = boundingRect(Mat(contours_poly[i]));
		minEnclosingCircle((Mat)contours_poly[i], center[i], radius[i]);
		if(boundRect[i].area() > largestRect.area()) {
			largestRect = boundRect[i];
		}
		if(radius[i] > largestCircleRadius) {
			largestCircleCenter = center[i];
			largestCircleRadius = radius[i];
		}
	}
	bounding_shapes_return ret;
	ret.rectangle = largestRect;
	ret.circle_center = largestCircleCenter;
	ret.circle_radius = largestCircleRadius;
	return ret;
}

/*
 * Takes in a result from get_bounding_shapes and prints it out as JSON.
 */
void print_results_as_json(bounding_shapes_return in) {
	string ret = string_format(json_format, in.rectangle.tl().x,
								in.rectangle.tl().y, in.rectangle.width,
								in.rectangle.height, in.circle_center.x,
								in.circle_center.y, in.circle_radius);
	cout << ret << endl;
}

/*
 * Takes in a result from get_bounding_shapes and draws them onto a new
 * window.
 */
void show_results(Size size, bounding_shapes_return in) {
	//drawContours(drawing, contours_poly, i, color, 1, 8, vector<Vec4i>(), 0, Point());
	Mat drawing = Mat::zeros(size, CV_8UC3);
	rectangle(drawing, in.rectangle.tl(), in.rectangle.br(), contour_color, 1, 1, 0);
	circle(drawing, in.circle_center, (int)in.circle_radius, contour_color, 1, 1, 0);
	imshow(window_name, drawing);
	waitKey(0);
}

/*
 * String formatting function.
 * 
 * http://stackoverflow.com/a/26221725/4541644
 */
template<typename ... Args> string string_format(const std::string& format, Args ... args) {
    size_t size = snprintf(nullptr, 0, format.c_str(), args ...) + 1; // Extra space for '\0'
    unique_ptr<char[]> buf(new char[ size ]); 
    snprintf(buf.get(), size, format.c_str(), args ...);
    return string(buf.get(), buf.get() + size - 1); // We don't want the '\0' inside
}
