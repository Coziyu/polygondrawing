from primative_renderer import *

def shape_renderer(filename, window_width = 800, window_height = 800):
    # Initialize pygame
    pygame.init()

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Shape Renderer")

    # TODO: Change this slightly
    # Take is a list of points and draws a shape connecting them with straight lines for now
    shape = read_shape(os.path.join(config.OUTPUT_FOLDER, filename))
    # print(shape)

    # Shape has coordinates where (0,0) is the center of the screen
    # Whereas pygame has (0,0) as the top left corner
    shape = convert_shape_to_pygame_coords(shape, window_width, window_height)
    # print(shape)

    # Draw the shape
    window.fill((0, 0, 0))
    for i in range(0,len(shape)):
        # The modulo handles wrapping around to the beginning of the list
        render_connection(shape[i], shape[(i + 1) % len(shape)], shape[(i + 2) % len(shape)], window)
        
    pygame.display.flip()
    
    # Show the window until it is closed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 
    