#ifndef CALCULATE_POS_H
#define CALCULATE_POS_H

#include <opencv2/imgproc/imgproc.hpp>

#if __cplusplus <= 199711L
cv::Point2f calculateRobotPosition(bounding_shapes_return*, int);
#else
cv::Point2f calculateRobotPosition(vector<bounding_shapes_return>)
#endif

#endif
