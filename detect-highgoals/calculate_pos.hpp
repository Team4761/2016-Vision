#ifndef CALCULATE_POS_H
#define CALCULATE_POS_H

#if __cplusplus <= 199711L
Point2f calculateRobotPosition(bounding_shapes_return*, int);
#else
Point2f calculateRobotPosition(vector<bounding_shapes_return>)
#endif

#endif
