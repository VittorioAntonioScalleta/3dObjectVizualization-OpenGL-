import pygame 
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

vertextxt = "vertex.txt"
facestxt = "faces.txt" 

paints = [  
    (0, 255, 0),    # green
    (255, 0, 0),    # red
    (255, 255, 0),  # yellow
    (0, 255, 255),  # cyan
    (0, 0, 255),    # blue
    (255, 255, 255) # white
]

def get_list(txtname):
    listname = []
    with open(txtname) as f:
        for line in f:
            line = line.rstrip(",\r\n").replace("(", '').replace(")", "").replace(" ", '')
            row = list(line.split(","))
            listname.append(row)
    listname = [[float(j) for j in i] for i in listname]
    return listname

modelVerts = get_list(vertextxt) 
modelFaces = get_list(facestxt) 

def draw_faces(current_color):
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(1.0, 1.0)
    glBegin(GL_TRIANGLES) 
    for eachface in modelFaces:
        for eachvert in eachface: 
            glVertex3fv(modelVerts[int(eachvert)])
    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)

def draw_edges():
    glColor3f(0, 0, 0)  # Black color for edges
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_TRIANGLES)
    for eachface in modelFaces:
        for eachvert in eachface:
            glVertex3fv(modelVerts[int(eachvert)])
    glEnd()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def setup_lighting():
    glEnable(GL_LIGHTING)               # Enable lighting
    glEnable(GL_LIGHT0)                 # Enable light source 0
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 1])  # Light position
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])  # Ambient light
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])  # Diffuse light
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])       # Specular light
    
    # Material properties
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [1, 1, 1, 1])  # Reflect ambient and diffuse light
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])             # Reflect specular light
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)                       # Shininess factor

def draw_light_source():
    # Position of the light
    light_pos = [1, 1, 1]
    
    # Temporarily disable lighting
    glDisable(GL_LIGHTING)
    
    # Draw the light source as a white sphere
    glColor3f(1, 1, 0)  # Yellow for light source
    glPushMatrix()
    glTranslatef(*light_pos)
    glutSolidCube(1)  # Small sphere to represent the light
    glPopMatrix()
    
    # Re-enable lighting
    glEnable(GL_LIGHTING)

def main():
    pygame.init()
    display = (800, 800)
    pygame.display.set_caption("RENDERING OBJECT WITH LIGHTING")
    FPS = pygame.time.Clock() 
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, 1, 0.1, 50)
    glTranslate(0, 0, -5) 
    glRotate(-90, 1, 0, 0)

    # Enable depth test and backface culling
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    # Setup lighting
    setup_lighting()

    Left = False
    Right = False
    Up = False
    Down = False
    color_index = 0

    def moveOBJ():
        if Left:
            glRotate(-1, 0, 0, 1)
        if Right:
            glRotate(1, 0, 0, 1)
        if Up:
            glRotate(1, 1, 0, 0)
        if Down:
            glRotate(-1, 1, 0, 0)

    current_color = paints[color_index]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_a:
                    Left = True
                if event.key == K_d:
                    Right = True
                if event.key == K_w:
                    Up = True
                if event.key == K_s:
                    Down = True
                if event.key == K_c:  # Change color on pressing 'C'
                    color_index = (color_index + 1) % len(paints)
                    current_color = paints[color_index]
            if event.type == KEYUP:
                if event.key == K_a:
                    Left = False
                if event.key == K_d:
                    Right = False
                if event.key == K_w:
                    Up = False
                if event.key == K_s:
                    Down = False
        
        pygame.display.flip()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_faces(current_color)
        draw_edges()
        draw_light_source()  # Render the light source
        moveOBJ()
        FPS.tick(60)

main()
