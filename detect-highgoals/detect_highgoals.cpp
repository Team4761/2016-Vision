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

#include <iostream>
#include <memory>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

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

enum video_out_mode_t {
    NONE,
    REGULAR,
    COLORFILTER,
};

//Constants
const Scalar color_lbound = Scalar(20, 40, 5);
const Scalar color_ubound = Scalar(70, 115, 30);
const Scalar contour_color = Scalar(255, 255, 255); //white
const string window_name = "Highgoal Detection Demo";
const string json_format = "{\"rectangle\":{\"top_left\":{\"x\":%d,\"y\":%d},\"width\":%d,\"height\":%d},\"circle\":{\"center\":{\"x\":%g,\"y\":%g},\"radius\":%g}}";

//Function prototypes
bounding_shapes_return get_bounding_shapes(Mat);
void print_results_as_json(bounding_shapes_return in);
template<typename ... Args> string string_format(const string&, Args ...);

int main(int argc, char **argv) {
    video_out_mode_t vidoutmode;
    if(argc == 2) {
        if(strcmp(argv[1], "regular") == 0) {
            vidoutmode = REGULAR;
        }
        else if(strcmp(argv[1], "colorfilter") == 0) {
            vidoutmode = COLORFILTER;
        }
        else {
            cout << "Invalid video output mode!" << endl;
            return -1;
        }
    }
    else {
        vidoutmode = NONE;
    }
    VideoCapture cap(0);
    if(!cap.isOpened()) {
        cout << "Cannot open video capture device" << endl;
        return -1;
    }
    namedWindow(window_name, CV_WINDOW_AUTOSIZE);
    Mat image, output;
    char key;
    bounding_shapes_return shapes;
    while(1) {
        bool success = cap.read(image);
        if(!success) {
            cout << "Cannot read frame from video file" << endl;
            return -1;
        }
        try {
			shapes = get_bounding_shapes(image);
			if(vidoutmode != NONE) {
				if(vidoutmode == COLORFILTER) {
					inRange(image, color_lbound, color_ubound, output);
				}
				else {
					output = image;
				}
				rectangle(output, shapes.rectangle.tl(), shapes.rectangle.br(), contour_color, 1, 1, 0);
				circle(output, shapes.circle_center, (int)shapes.circle_radius, contour_color, 1, 1, 0);
				imshow(window_name, output);
				key = waitKey(10);
				if(char(key) == 27) { //quit if ESC is pressed
					break;
				}
			}
			print_results_as_json(shapes);
		}
		catch(Exception e) {
			//cout << e.what() << endl;
			//probably shouldn't pass silently, but whatever
		}
    }
    cap.release();
}

/*
 * Image goes in, gets run through a few filters and a final result pops
 * out, contained in a struct.
 */
bounding_shapes_return get_bounding_shapes(Mat input_img) {
    Mat rgb_out;
    inRange(input_img, color_lbound, color_ubound, rgb_out);
    
    vector<vector<Point>> contours;
    findContours(rgb_out, contours, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
    
    vector<vector<Point>> contours_poly(contours.size());
    double current_contour_length;
    double largest_contour_length;
    vector<Point> largest_contour;
    for(unsigned int i = 0; i < contours.size(); i++) {
        approxPolyDP(Mat(contours[i]), contours_poly[i], 3, true);
        current_contour_length = arcLength(contours_poly[i], true);
        if(current_contour_length > largest_contour_length) {
            largest_contour = contours_poly[i];
            largest_contour_length = current_contour_length;
        }
    }
    
    Point2f bounding_circle_center;
    float bounding_circle_radius;
    Rect bounding_rect = boundingRect(Mat(largest_contour));
    minEnclosingCircle((Mat)largest_contour, bounding_circle_center, bounding_circle_radius);
    
    bounding_shapes_return ret;
    ret.rectangle = bounding_rect;
    ret.circle_center = bounding_circle_center;
    ret.circle_radius = bounding_circle_radius;
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
 * String formatting function.
 * 
 * http://stackoverflow.com/a/26221725/4541644
 */
template<typename ... Args> string string_format(const std::string& format, Args ... args) {
    size_t size = snprintf(nullptr, 0, format.c_str(), args ...) + 1;
    unique_ptr<char[]> buf(new char[ size ]); 
    snprintf(buf.get(), size, format.c_str(), args ...);
    return string(buf.get(), buf.get() + size - 1);
}
