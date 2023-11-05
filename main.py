# This project draws shapes by defining connections between points
# straight edges and curved edges (with bezier curves) and then filling them in.
# Schema for Shape Storage:
# A list represents the spape. Each element in the list is either a 2-tuple or a none.
# A 2-tuple represents a point. The first element is the x coordinate and the second is the y coordinate.
# These points are connected by straight lines.
# A 4-tuple represents a pair of bezier control points. x1, y1, x2, y2 are the coordinates of the control points.
# The points before and after the 4-tuple are the endpoints of the bezier curve.

from shape_renderer import *
from shape_creater import *

# Main Loop
def main():
    print("Enter Mode:")
    print("1. Shape Creater")
    print("2. Shape Renderer")
    print("Input anything else to exit:")
    mode = input()
    if mode == "1":
        shape_creater()
        pass
    elif mode == "2":
        shape_renderer()
    else:
        print("Exiting...")
        return

if __name__ == "__main__":
    main()