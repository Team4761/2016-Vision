#include <algorithm>
#include <cmath>
#include "detect_highgoals.hpp"
#include <opencv2/imgproc/imgproc.hpp>

using namespace cv;
using namespace std;

// The constants k1, k2, and k3 can be solved for ahead of time, as they rely only upon the camera and targets in use (neither of which will be changing during the competition)
float k1 = 0.0;
float k2 = 0.0;
float k3 = 0.0;

//Function prototypes
Point2f doCalculations(bounding_shapes_return, bounding_shapes_return);
bool leftmostTargetSort(bounding_shapes_return, bounding_shapes_return);

#if __cplusplus <= 199711L
// IF not using C++11 use an array (pointer) and an array size int
	Point2f calculateRobotPosition(bounding_shapes_return* allFoundTargets, int numberOfTargets)
	{	
		// Order all of the found targets from leftmost -> rightmost
		sort(allFoundTargets, allFoundTargets+numberOfTargets, leftmostTargetSort);
		bounding_shapes_return target0 = allFoundTargets[0];
		bounding_shapes_return target1 = allFoundTargets[1];
		
		return doCalculations(target0, target1);	
	}
#else
// ELSE IF using C++11 use a vector
	Point2f calculateRobotPosition(vector<bounding_shapes_return> allFoundTargets)
	{	
		// Order all of the found targets from leftmost -> rightmost
		sort(allFoundTargets.begin(), allFoundTargets.end(), leftmostTargetSort);
		bounding_shapes_return target0 = allFoundTargets[0];
		bounding_shapes_return target1 = allFoundTargets[1];
		
		return doCalculations(target0, target1);	
	}
#endif

Point2f doCalculations(bounding_shapes_return target0, bounding_shapes_return target1)
{
	#warning Sort of just guessing on value for vp now...
	int vp = 240;
	// Solve for the angle of the robot relative to the tower (where the angle of the edge between the faces with targets is denoted as vp [the equation should be run once for each such point, calculating a number of possible solutions]), and the radius (distance of the robot from the "center" of the tower)
	float theta = k1 * (target1.rectangle.br().x - target1.rectangle.tl().x - target0.rectangle.tl().x + target0.rectangle.br().x) + vp;
	float radius = k2 / (target0.rectangle.tl().y - target0.rectangle.br().y + target1.rectangle.tl().y - target1.rectangle.br().y - k3);
	
	// Solve for the robot's x and y positions, where x and y represent the position of the robot [in whatever unit the constants (k1, k2, k3) 	were calculated] in relation to the "center" of the tower
	float x = radius * cos(theta);
	float y = radius * sin(theta);
	
	return Point2f(x, y);
}

bool leftmostTargetSort(bounding_shapes_return a, bounding_shapes_return b)
{
	return a.rectangle.tl().x < b.rectangle.tl().x;
}
