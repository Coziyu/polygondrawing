from util import * 
from primative_renderer import *

def save_shape(shape, width, height, filename):
    path = os.path.join("shapes", filename)
    file = open(path, "w+")
    outputShape = convert_shape_to_central_origin_coords(copy.deepcopy(shape), width, height)
    for i in range(len(outputShape)):
        if len(outputShape[i]) == 2:
            file.write(str(outputShape[i][0]) + "," + str(outputShape[i][1]) + "\n")
        elif len(outputShape[i]) == 4:
            file.write(str(outputShape[i][0]) + "," + str(outputShape[i][1]) + "," + str(outputShape[i][2]) + "," + str(outputShape[i][3]) + "\n")
    file.close()

def add_control_points(shape):
    if len(shape) == 0:
        add_point(shape)
    start = shape[-1]
    control= (start[0] + 50, start[1], start[0], start[1] + 50)
    shape.append(control)

def add_point(shape):
    if len(shape) == 0:
        shape.append((400, 400))
    else:
        # Place the point so that it is 50 pixels away from the last point in the shape randomly in a circle
        last_point = shape[-1]
        angle = random.random() * 2 * math.pi
        radius = 50
        new_point = (round(last_point[0] + radius * math.cos(angle)), round(last_point[1] + radius * math.sin(angle)))
        shape.append(new_point)

def shape_creater(window_width = 800, window_height = 800):
    pygame.init()

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Shape Creater")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial" , 18 , bold = True)

    # To keep track of any changes to the newshape array
    history = Stack()
    # The shape that is being created
    currentShape = history.peek() #! Do not convert this to pygame coordinates
    running = True


    heldPointIndex = 0
    heldControlIndex = 0

    evAddPoint = False
    evAddCurve = False
    evRemovingPoint = False
    evDraggingPoint = False
    evDraggingControl = False
    evDroppedPoint = False
    evDragInitiated = False
    evPrintHistory = False
    evUndo = False
    evRedo = False
    evSave = False
    # Poll Update Render Loop:
    while running:
        # Poll Events
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False
            if events.type == pygame.MOUSEBUTTONDOWN:
                # If LB is held on a point, move that point
                if events.button == pygame.BUTTON_LEFT:
                    evDragInitiated = True
                # If RB is held on a point, remove that point
                elif events.button == pygame.BUTTON_RIGHT:
                    evRemovingPoint = True

            if events.type == pygame.MOUSEBUTTONUP:
                if events.button == pygame.BUTTON_LEFT:
                    evDroppedPoint = True
                if events.button == pygame.BUTTON_RIGHT:
                    evRemovingPoint = False

            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    running = False
                elif events.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    evUndo = True
                elif events.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    evRedo = True
                elif events.key == pygame.K_i and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    evAddCurve = True
                elif events.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    evSave = True
                elif events.key == pygame.K_i:
                    evAddPoint = True
                elif events.key == pygame.K_TAB:
                    evPrintHistory = True
            
        # Update
        # ! Should probably refactor into a function with a swutch statement 
        # ! using unique eventcodes to handle events buttt this is a school project so I don't care
        if evPrintHistory:
            history.print()
            evPrintHistory = False

        elif evUndo:
            print("Undoing")
            currentShape = history.pop()
            evUndo = False

        elif evRedo:
            print("Redoing")
            currentShape = history.unpop()
            evRedo = False

        elif evSave:
            print("Saving")
            outFileName = input("Enter a filename: ")
            if outFileName == "":
                # Creates "shape (n).txt" where n is the number of shapes saved
                outFileName = f"shape_{str(len(os.listdir('shapes')))}.txt"
            save_shape(currentShape, window_width, window_height, outFileName)
            # Removes "Saving" from the terminal and replaces it with "Saved"
            print("\033[F\033[K\033[F\033[KSaved")
            evSave = False

        elif evDragInitiated:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(currentShape)):
                if len(currentShape[i]) == 2 and (distance(currentShape[i], mouse_pos) < 5):
                    print("Moving Point")
                    currentShape = history.append(currentShape)
                    evDraggingPoint = True
                    heldPointIndex = i
                    break
                elif len(currentShape[i]) == 4 and (distance(currentShape[i][0:2], mouse_pos) < 5):
                    print("Moving Control Point")
                    currentShape = history.append(currentShape)
                    evDraggingControl = True
                    heldPointIndex = i
                    heldControlIndex = 0
                    break
                elif len(currentShape[i]) == 4 and (distance(currentShape[i][2:4], mouse_pos) < 5):
                    print("Moving Control Point")
                    currentShape = history.append(currentShape)
                    evDraggingControl = True
                    heldPointIndex = i
                    heldControlIndex = 1
                    break
            evDragInitiated = False

        elif evDroppedPoint:
            if evDraggingPoint or evDraggingControl:
                print("Dropped Point")
                evDraggingPoint = False
                evDraggingControl = False
            evDroppedPoint = False

        elif evDraggingPoint:
            mouse_pos = pygame.mouse.get_pos()
            currentShape[heldPointIndex] = (round(mouse_pos[0]), round(mouse_pos[1]))
        
        elif evDraggingControl:
            mouse_pos = pygame.mouse.get_pos()
            if heldControlIndex == 0:
                currentShape[heldPointIndex] = (round(mouse_pos[0]), round(mouse_pos[1]), currentShape[heldPointIndex][2], currentShape[heldPointIndex][3])
            elif heldControlIndex == 1:
                currentShape[heldPointIndex] = (currentShape[heldPointIndex][0], currentShape[heldPointIndex][1], round(mouse_pos[0]), round(mouse_pos[1]))

        elif evAddPoint:
            # Add a point to the shape
            currentShape = history.append(currentShape)
            print("Adding Point")
            add_point(currentShape)
            evAddPoint = False

        elif evAddCurve:
            # Add a curve to the shape
            currentShape = history.append(currentShape)
            print("Adding Curve")
            add_control_points(currentShape)
            add_point(currentShape)
            evAddCurve = False

        elif evRemovingPoint:
            # Remove a point from the shape
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(currentShape)):
                if len(currentShape[i]) == 2 and distance(currentShape[i], mouse_pos) < 5:
                    print("Removing Point")
                    currentShape = history.append(currentShape)
                    currentShape.pop(i)
                    break
        


        # Render
        # shape = convert_shape_to_pygame_coords(newshape, window_width, window_height)
        window.fill((0, 0, 0))
        for i in range(0,len(currentShape)):
            # The modulo handles wrapping around to the beginning of the list
            render_point(currentShape[i], window)
            render_connection(currentShape[i], currentShape[(i + 1) % len(currentShape)], currentShape[(i + 2) % len(currentShape)], window)        
            
        pygame.display.flip()