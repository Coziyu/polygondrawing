from util import * 
from primative_renderer import *

def save_shape(shape, width, height, filename):
    path = os.path.join(config.OUTPUT_FOLDER, filename)
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

def show_action_notification(message, msgcolor, bgcolor, alpha, font, window):
    # Render the message
    text = font.render(message, True, msgcolor, bgcolor)
    text.set_alpha(alpha * 255)
    # Generate Text Box
    textBox = text.get_rect()
    # Flush the text box to the bottom right corner
    textBox.bottomright = window.get_rect().bottomright
    # Display the message
    window.blit(text, textBox)


def shape_creater(fileName, window_width = 800, window_height = 800):
    pygame.init()

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(f"Shape Creater: {'New Shape' if fileName == '' else fileName}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Courier New" , 12)        

    if fileName == "":
        # If no filename is specified, create a new shape
        currentShape = []
    else:
        # Load the shape from the file
        currentShape = read_shape(os.path.join(config.OUTPUT_FOLDER,fileName))
        currentShape = convert_shape_to_pygame_coords(currentShape, window_width, window_height)

    # To keep track of changes to the shape
    history = Stack(currentShape)
    running = True

    #! A message object should it's own class tbh
    #! Then we have have a message handler that handles the messages
    #! With that, we can do message queues,
    #! easier message customization via notification types
    #! And more importantly, the code is cleaner
    #* actnNotif is short for action notification
    #* This is the small notification at the bottom right
    #* that appears when an action is performed
    actnNotifStartTime = -1
    currTime = 0
    currNotifMessage = ""
    notifAlpha = 0

    #* Indices of the hovered point and control points that are howevered over
    hoveredPointIndex = 0
    hoveredControlIndex = 0 # Tells us which control point is being hovered over

    evNewActnNotif = False
    evShowingActnNotif = False

    evCheckForInteractable = False
    evHoverInteractable = False

    evAddPoint = False
    evAddCurve = False
    evRemovingPoint = False
    evHoverPoint = False
    evHoverControl = False
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
        #* Poll Events
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                running = False

            if events.type == pygame.MOUSEMOTION:
                evCheckForInteractable = True

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
            
        #* Update
        currTime = pygame.time.get_ticks()

        if evCheckForInteractable and not (evDraggingPoint or evDraggingControl):
            mouse_pos = pygame.mouse.get_pos()
            # Check is cursor is over a point
            for i in range(len(currentShape)):
                if len(currentShape[i]) == 2 and (distance(currentShape[i], mouse_pos) < 5):
                    hoveredPointIndex = i
                    evHoverPoint = True
                    break
                elif len(currentShape[i]) == 4 and (distance(currentShape[i][0:2], mouse_pos) < 5):
                    hoveredPointIndex = i
                    hoveredControlIndex = 0
                    evHoverControl = True
                    break
                elif len(currentShape[i]) == 4 and (distance(currentShape[i][2:4], mouse_pos) < 5):
                    hoveredPointIndex = i
                    hoveredControlIndex = 1
                    evHoverControl = True
                    break
                else:
                    evHoverPoint = False
                    evHoverControl = False
                    hoveredPointIndex = None
            evHoverInteractable = evHoverPoint or evHoverControl

            if evHoverInteractable:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            evCheckForInteractable = False

        # ! Should refactor into a function with a switch statement 
        # ! that takes in unique eventcodes to handle events 
        # ! buttt this is a school project so I don't care
        if evPrintHistory:
            history.print()
            evPrintHistory = False
        
        elif evUndo:
            print("Undoing")
            currentShape = history.pop()
            evNewActnNotif = True
            currNotifMessage = "Undo"
            evUndo = False

        elif evRedo:
            print("Redoing")
            currentShape = history.unpop()
            evNewActnNotif = True
            currNotifMessage = "Redo"
            evRedo = False

        elif evSave:
            print("Saving")
            if fileName == "":
                outFileName = input("Enter a filename: ")
                if outFileName == "":
                    # Creates "shape (n).txt" where n is the number of shapes saved
                    outFileName = f"shape_{str(len(os.listdir('shapes')))}"
                outFileName += ".txt"
            else:
                outFileName = fileName
            save_shape(currentShape, window_width, window_height, outFileName)
            # Removes "Saving" from the terminal and replaces it with "Saved"
            print("\033[F\033[K\033[F\033[KSaved")
            fileName = outFileName
            evNewActnNotif = True
            currNotifMessage = f"Saved file to {os.path.join(os.getcwd(), config.OUTPUT_FOLDER, fileName)}"
            evSave = False

        elif evDragInitiated:
            if evHoverInteractable:
                print("Moving Point" if evHoverPoint else "Moving Control Point")
                currentShape = history.append(currentShape)
                evDraggingPoint = evHoverPoint
                evDraggingControl = evHoverControl
            evDragInitiated = False

        elif evDroppedPoint:
            if evDraggingPoint or evDraggingControl:
                print("Dropped Point")
                evDraggingPoint = False
                evDraggingControl = False
                evNewActnNotif = True
                currNotifMessage = "Moved Point" if evDraggingPoint else "Moved Control Point"
            evDroppedPoint = False

        elif evDraggingPoint:
            mouse_pos = pygame.mouse.get_pos()
            currentShape[hoveredPointIndex] = (round(mouse_pos[0]), round(mouse_pos[1]))
        
        elif evDraggingControl:
            mouse_pos = pygame.mouse.get_pos()
            if hoveredControlIndex == 0:
                currentShape[hoveredPointIndex] = (round(mouse_pos[0]), round(mouse_pos[1]), currentShape[hoveredPointIndex][2], currentShape[hoveredPointIndex][3])
            elif hoveredControlIndex == 1:
                currentShape[hoveredPointIndex] = (currentShape[hoveredPointIndex][0], currentShape[hoveredPointIndex][1], round(mouse_pos[0]), round(mouse_pos[1]))

        elif evAddPoint:
            # Add a point to the shape
            currentShape = history.append(currentShape)
            print("Adding Point")
            add_point(currentShape)
            evNewActnNotif = True
            currNotifMessage = "Added Point"
            evAddPoint = False

        elif evAddCurve:
            # Add a curve to the shape
            currentShape = history.append(currentShape)
            print("Adding Curve")
            add_control_points(currentShape)
            add_point(currentShape)
            evNewActnNotif = True
            currNotifMessage = "Added Curve"
            evAddCurve = False

        elif evRemovingPoint:
            # Remove a point from the shape
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(currentShape)):
                if len(currentShape[i]) == 2 and distance(currentShape[i], mouse_pos) < 5:
                    print("Removing Point")
                    currentShape = history.append(currentShape)
                    currentShape.pop(i)
                    evNewActnNotif = True 
                    currNotifMessage = "Removed Point"
                    break

        #! Important to always handle subsequent events on the next frame
        #! Prevent timing issues when facing blocking events like 
        #! saving a new file
        elif evNewActnNotif:
            actnNotifStartTime = currTime
            notifAlpha = 1

            evShowingActnNotif = True
            evNewActnNotif = False



        #* Render Objects
        # shape = convert_shape_to_pygame_coords(newshape, window_width, window_height)
        window.fill((0, 0, 0))
        for i in range(0,len(currentShape)):
            # The modulo handles wrapping around to the beginning of the list
            render_point(currentShape[i], window)
            render_connection(currentShape[i], currentShape[(i + 1) % len(currentShape)], currentShape[(i + 2) % len(currentShape)], window)


        #* Render UI Elements

        if evShowingActnNotif:
            show_action_notification(currNotifMessage, (255, 255, 255), (0, 100, 0), notifAlpha,font, window)
            if currTime - actnNotifStartTime > 2000:
                currNotifMessage = ""
                actnNotifStartTime = -1
                evShowingActnNotif = False
            elif currTime - actnNotifStartTime > 1000:
                # Fades the notification out over 1 second
                # map time diff to alpha [1000:2000] -> [1,0]
                notifAlpha = max(1 - (currTime - actnNotifStartTime - 1000)/1000, 0)
    

            
        pygame.display.flip()