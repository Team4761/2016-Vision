#ifndef DETECT_HIGHGOALS_H
#define DETECT_HIGHGOALS_H

#include <opencv2/imgproc/imgproc.hpp>
#include <string>

/*
 * Struct for containing the return value for get_bounding_shapes(). I
 * think this is justifiable in this case since the values are very
 * closely related.
 */
struct bounding_shapes_return {
    cv::Rect rectangle;
    cv::Point2f circle_center;
    float circle_radius;
};

enum video_out_mode_t {
    NONE,
    REGULAR,
    COLORFILTER,
};

bounding_shapes_return get_bounding_shapes(cv::Mat);
void print_results_as_json(bounding_shapes_return in);
int set_exposure(int, int);
template<typename ... Args> std::string string_format(const std::string&, Args ...);


#endif
