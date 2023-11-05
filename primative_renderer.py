from util import * 

def render_point(point, window):
    # Draw a point at the point
    if len(point) == 2:
        pygame.draw.circle(window, (255, 255, 255), point, 5)
    elif len(point) == 4:
        # Draw the control points, and colour them based on their coordinates
        color = (max(10,(point[0] * point[2]) % 255), 
                 max(10,(point[1] * point[3]) % 255), 
                 max(10,(point[0] * point[3]) % 255))
        pygame.draw.circle(window, color, point[0:2], 5)
        pygame.draw.circle(window, color, point[2:4], 5)

# Handles drawing a straight line between two points
def render_line(p1, p2, window):
    # Draw a line from p1 to p2
    pygame.draw.line(window, (255, 255, 255), p1, p2)

# Handles drawing a bezier curve between two points
def render_bezier(p1, c1, c2, p2, window):
    # Draw a bezier curve from p1 to p2 with control points c1 and c2
    line_segs = computeBezier(p1, c1, c2, p2)
    for i in range(len(line_segs) - 1):
        pygame.draw.line(window, (255, 255, 255), line_segs[i], line_segs[i + 1])

def render_connection(p1, p2, p3, window):
    if len(p1) == 2 and len(p2) == 2:
            # Draw a line
            render_line(p1, p2, window)
    elif len(p1) == 2 and len(p2) == 4:
        # Since p2 has 4 elements, it must be a pair of bezier control points 
        # Draw a bezier curve
        control_point_1 = p2[0:2]
        control_point_2 = p2[2:4]
        render_bezier(p1, control_point_1, control_point_2, p3, window)
    elif len(p1) == 4:
        pass
    else:
        print("Error: Invalid Shape")
        return
