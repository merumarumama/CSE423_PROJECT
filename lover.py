from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

# Camera position (fixed third person view looking into the cabin)
camera_pos = (0, 500, 300)  # Looking down into the cabin
camera_angle_x = -30  # Look downward angle
camera_angle_y = 0
fovY = 60

# Room dimensions
ROOM_SIZE = 400
WALL_HEIGHT = 250
GRID_LENGTH = ROOM_SIZE

# Animation variables
object_pulse = 0

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1.0, 1.0, 1.0)):
    glPushAttrib(GL_CURRENT_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(*color)
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glPopAttrib()

def draw_wooden_floor():
    """Draw wooden floor with checkered pattern"""
    glBegin(GL_QUADS)
    
    num_tiles = 16
    tile_size = ROOM_SIZE * 2 / num_tiles
    
    for i in range(-num_tiles//2, num_tiles//2):
        for j in range(-num_tiles//2, num_tiles//2):
            x1 = i * tile_size
            y1 = j * tile_size
            x2 = (i + 1) * tile_size
            y2 = (j + 1) * tile_size
            
            if (i + j) % 2 == 0:
                glColor3f(0.6, 0.4, 0.25)  # Light wood
            else:
                glColor3f(0.5, 0.35, 0.2)   # Dark wood
            
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    
    glEnd()

def draw_wooden_walls():
    """Draw cabin walls with wood paneling"""
    glPushMatrix()
    
    # Back wall
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.3, 0.2)  # Dark wood
    glVertex3f(-ROOM_SIZE, ROOM_SIZE, 0)
    glVertex3f(ROOM_SIZE, ROOM_SIZE, 0)
    glVertex3f(ROOM_SIZE, ROOM_SIZE, WALL_HEIGHT)
    glVertex3f(-ROOM_SIZE, ROOM_SIZE, WALL_HEIGHT)
    glEnd()
    
    # Left wall with wood panels
    panel_width = ROOM_SIZE * 2 / 6
    for i in range(6):
        x_start = -ROOM_SIZE
        y_start = -ROOM_SIZE + i * panel_width
        y_end = y_start + panel_width
        
        glBegin(GL_QUADS)
        if i % 2 == 0:
            glColor3f(0.5, 0.35, 0.25)  # Light panel
        else:
            glColor3f(0.45, 0.3, 0.2)   # Dark panel
        
        glVertex3f(x_start, y_start, 0)
        glVertex3f(x_start, y_end, 0)
        glVertex3f(x_start, y_end, WALL_HEIGHT)
        glVertex3f(x_start, y_start, WALL_HEIGHT)
        glEnd()
    
    # Right wall with wood panels
    for i in range(6):
        x_start = ROOM_SIZE
        y_start = -ROOM_SIZE + i * panel_width
        y_end = y_start + panel_width
        
        glBegin(GL_QUADS)
        if i % 2 == 0:
            glColor3f(0.45, 0.3, 0.2)   # Dark panel
        else:
            glColor3f(0.5, 0.35, 0.25)  # Light panel
        
        glVertex3f(x_start, y_start, 0)
        glVertex3f(x_start, y_end, 0)
        glVertex3f(x_start, y_end, WALL_HEIGHT)
        glVertex3f(x_start, y_start, WALL_HEIGHT)
        glEnd()
    
    # Front wall (with fireplace opening)
    glBegin(GL_QUADS)
    glColor3f(0.4, 0.3, 0.2)
    # Left section
    glVertex3f(-ROOM_SIZE, -ROOM_SIZE, 0)
    glVertex3f(-120, -ROOM_SIZE, 0)
    glVertex3f(-120, -ROOM_SIZE, WALL_HEIGHT)
    glVertex3f(-ROOM_SIZE, -ROOM_SIZE, WALL_HEIGHT)
    
    # Right section
    glVertex3f(120, -ROOM_SIZE, 0)
    glVertex3f(ROOM_SIZE, -ROOM_SIZE, 0)
    glVertex3f(ROOM_SIZE, -ROOM_SIZE, WALL_HEIGHT)
    glVertex3f(120, -ROOM_SIZE, WALL_HEIGHT)
    
    # Top section above fireplace
    glVertex3f(-120, -ROOM_SIZE, 180)
    glVertex3f(120, -ROOM_SIZE, 180)
    glVertex3f(120, -ROOM_SIZE, WALL_HEIGHT)
    glVertex3f(-120, -ROOM_SIZE, WALL_HEIGHT)
    glEnd()
    
    # Ceiling
    glBegin(GL_QUADS)
    glColor3f(0.35, 0.25, 0.15)
    glVertex3f(-ROOM_SIZE, -ROOM_SIZE, WALL_HEIGHT)
    glVertex3f(ROOM_SIZE, -ROOM_SIZE, WALL_HEIGHT)
    glVertex3f(ROOM_SIZE, ROOM_SIZE, WALL_HEIGHT)
    glVertex3f(-ROOM_SIZE, ROOM_SIZE, WALL_HEIGHT)
    glEnd()
    
    # Wooden beams on walls
    glColor3f(0.3, 0.2, 0.1)
    beam_thickness = 12
    
    # Horizontal beams on back wall
    for height in [60, 160, 230]:
        glBegin(GL_QUADS)
        glVertex3f(-ROOM_SIZE, ROOM_SIZE - beam_thickness, height)
        glVertex3f(ROOM_SIZE, ROOM_SIZE - beam_thickness, height)
        glVertex3f(ROOM_SIZE, ROOM_SIZE, height)
        glVertex3f(-ROOM_SIZE, ROOM_SIZE, height)
        glEnd()
    
    # Vertical beams in corners
    for x in [-ROOM_SIZE, ROOM_SIZE]:
        glBegin(GL_QUADS)
        glVertex3f(x, -ROOM_SIZE, 0)
        glVertex3f(x + beam_thickness, -ROOM_SIZE, 0)
        glVertex3f(x + beam_thickness, -ROOM_SIZE, WALL_HEIGHT)
        glVertex3f(x, -ROOM_SIZE, WALL_HEIGHT)
        glEnd()
    
    glPopMatrix()

def draw_fireplace():
    """Draw stone fireplace with static fire"""
    glPushMatrix()
    glTranslatef(0, -ROOM_SIZE + 25, 0)
    
    # Stone fireplace structure
    glColor3f(0.35, 0.35, 0.35)
    
    # Base
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glScalef(200, 50, 80)
    glutSolidCube(1)
    glPopMatrix()
    
    # Left pillar
    glPushMatrix()
    glTranslatef(-75, 0, 100)
    glScalef(30, 50, 120)
    glutSolidCube(1)
    glPopMatrix()
    
    # Right pillar
    glPushMatrix()
    glTranslatef(75, 0, 100)
    glScalef(30, 50, 120)
    glutSolidCube(1)
    glPopMatrix()
    
    # Mantel
    glColor3f(0.25, 0.25, 0.25)
    glPushMatrix()
    glTranslatef(0, 0, 140)
    glScalef(220, 15, 15)
    glutSolidCube(1)
    glPopMatrix()
    
    # Fireplace opening
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 25, 70)
    glScalef(130, 60, 50)
    glutSolidCube(1)
    glPopMatrix()
    
    # Static fire
    # Base flame (orange)
    glColor3f(1.0, 0.5, 0.0)
    glPushMatrix()
    glTranslatef(0, 40, 70)
    glutSolidSphere(20, 12, 12)
    glPopMatrix()
    
    # Middle flame (red)
    glColor3f(1.0, 0.2, 0.0)
    glPushMatrix()
    glTranslatef(0, 50, 75)
    glutSolidSphere(15, 10, 10)
    glPopMatrix()
    
    # Top flames (yellow)
    glColor3f(1.0, 0.9, 0.2)
    for angle in [0, 120, 240]:
        rad_angle = math.radians(angle)
        x_offset = 12 * math.cos(rad_angle)
        z_offset = 12 * math.sin(rad_angle)
        
        glPushMatrix()
        glTranslatef(x_offset, 60, 75 + z_offset)
        glutSolidCone(8, 25, 6, 6)
        glPopMatrix()
    
    # Logs in fireplace
    glColor3f(0.4, 0.25, 0.15)
    
    # Back log
    glPushMatrix()
    glTranslatef(0, 15, 50)
    glRotatef(30, 0, 1, 0)
    glScalef(60, 12, 12)
    glutSolidCube(1)
    glPopMatrix()
    
    # Front log
    glPushMatrix()
    glTranslatef(0, 10, 60)
    glRotatef(-30, 0, 1, 0)
    glScalef(50, 10, 10)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()

def draw_furniture():
    """Draw cabin furniture"""
    glPushMatrix()
    
    # Persian rug in front of fireplace
    glBegin(GL_QUADS)
    # Main rug color
    glColor3f(0.7, 0.2, 0.1)
    glVertex3f(-100, -ROOM_SIZE + 70, 0.5)
    glVertex3f(100, -ROOM_SIZE + 70, 0.5)
    glVertex3f(100, -ROOM_SIZE + 170, 0.5)
    glVertex3f(-100, -ROOM_SIZE + 170, 0.5)
    
    # Rug border
    glColor3f(0.9, 0.8, 0.2)
    border_width = 10
    # Top border
    glVertex3f(-100, -ROOM_SIZE + 70, 0.6)
    glVertex3f(100, -ROOM_SIZE + 70, 0.6)
    glVertex3f(100, -ROOM_SIZE + 70 + border_width, 0.6)
    glVertex3f(-100, -ROOM_SIZE + 70 + border_width, 0.6)
    # Bottom border
    glVertex3f(-100, -ROOM_SIZE + 170 - border_width, 0.6)
    glVertex3f(100, -ROOM_SIZE + 170 - border_width, 0.6)
    glVertex3f(100, -ROOM_SIZE + 170, 0.6)
    glVertex3f(-100, -ROOM_SIZE + 170, 0.6)
    # Left border
    glVertex3f(-100, -ROOM_SIZE + 70, 0.6)
    glVertex3f(-100 + border_width, -ROOM_SIZE + 70, 0.6)
    glVertex3f(-100 + border_width, -ROOM_SIZE + 170, 0.6)
    glVertex3f(-100, -ROOM_SIZE + 170, 0.6)
    # Right border
    glVertex3f(100 - border_width, -ROOM_SIZE + 70, 0.6)
    glVertex3f(100, -ROOM_SIZE + 70, 0.6)
    glVertex3f(100, -ROOM_SIZE + 170, 0.6)
    glVertex3f(100 - border_width, -ROOM_SIZE + 170, 0.6)
    glEnd()
    
    # Armchair left of fireplace
    glPushMatrix()
    glTranslatef(-180, -ROOM_SIZE + 120, 0)
    
    # Chair base
    glColor3f(0.5, 0.35, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, 30)
    glScalef(50, 50, 60)
    glutSolidCube(1)
    glPopMatrix()
    
    # Chair back
    glPushMatrix()
    glTranslatef(0, 30, 70)
    glScalef(50, 10, 40)
    glutSolidCube(1)
    glPopMatrix()
    
    # Chair arms
    glColor3f(0.45, 0.3, 0.15)
    # Left arm
    glPushMatrix()
    glTranslatef(-30, 0, 60)
    glScalef(10, 50, 30)
    glutSolidCube(1)
    glPopMatrix()
    # Right arm
    glPushMatrix()
    glTranslatef(30, 0, 60)
    glScalef(10, 50, 30)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()
    
    # Coffee table in center
    glPushMatrix()
    glTranslatef(0, -50, 0)
    
    # Table top
    glColor3f(0.4, 0.25, 0.15)
    glPushMatrix()
    glTranslatef(0, 0, 45)
    glScalef(80, 50, 5)
    glutSolidCube(1)
    glPopMatrix()
    
    # Table legs
    glColor3f(0.35, 0.2, 0.1)
    leg_positions = [(-35, -20), (35, -20), (-35, 20), (35, 20)]
    for x, y in leg_positions:
        glPushMatrix()
        glTranslatef(x, y, 22)
        glScalef(6, 6, 45)
        glutSolidCube(1)
        glPopMatrix()
    
    glPopMatrix()
    
    # Bookshelf on right wall
    glPushMatrix()
    glTranslatef(ROOM_SIZE - 20, 0, 0)
    
    # Shelf frame
    glColor3f(0.45, 0.3, 0.2)
    glPushMatrix()
    glTranslatef(0, 0, 120)
    glScalef(15, 120, 180)
    glutSolidCube(1)
    glPopMatrix()
    
    # Shelves
    glColor3f(0.4, 0.25, 0.15)
    for height in [40, 100, 160]:
        glPushMatrix()
        glTranslatef(0, 0, height)
        glScalef(12, 115, 5)
        glutSolidCube(1)
        glPopMatrix()
    
    # Books
    book_colors = [(0.8, 0.2, 0.2), (0.2, 0.2, 0.8), (0.2, 0.8, 0.2), 
                   (0.8, 0.8, 0.2), (0.8, 0.2, 0.8)]
    
    for i, color in enumerate(book_colors):
        glColor3f(*color)
        glPushMatrix()
        glTranslatef(5, -50 + i * 20, 50 + (i % 3) * 40)
        glScalef(8, 15, 30)
        glutSolidCube(1)
        glPopMatrix()
    
    glPopMatrix()
    
    # Hanging ceiling lamp
    glPushMatrix()
    glTranslatef(0, 100, 220)
    
    # Chain
    glColor3f(0.6, 0.6, 0.6)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3, 3, 40, 8, 8)
    glPopMatrix()
    
    # Lamp shade
    glColor3f(1.0, 1.0, 0.9)
    glutSolidSphere(18, 16, 16)
    
    # Light glow (transparent sphere)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 0.8, 0.3)
    glutSolidSphere(30, 12, 12)
    glDisable(GL_BLEND)
    
    glPopMatrix()
    
    glPopMatrix()

def setup_lighting():
    """Setup lighting for the scene"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    
    # Main ceiling light
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 100, 220, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 0.9, 1.0])
    
    # Fireplace light
    glLightfv(GL_LIGHT1, GL_POSITION, [0, -ROOM_SIZE + 40, 70, 1])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.8, 0.4, 0.2, 1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.4, 0.2, 0.1, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.5, 0.25, 0.1, 1.0])

def keyboardListener(key, x, y):
    """Handle keyboard inputs for camera movement"""
    global camera_pos, camera_angle_x, camera_angle_y
    
    key = key.decode('utf-8').lower()
    x, y, z = camera_pos
    
    # Camera movement
    if key == 'w':  # Move camera forward (zoom in)
        z = max(z - 20, 150)
    elif key == 's':  # Move camera backward (zoom out)
        z = min(z + 20, 600)
    elif key == 'a':  # Move camera left
        x -= 20
    elif key == 'd':  # Move camera right
        x += 20
    elif key == 'q':  # Move camera up
        y += 20
    elif key == 'e':  # Move camera down
        y = max(y - 20, 200)
    elif key == 'r':  # Reset camera
        x, y, z = (0, 500, 300)
        camera_angle_x = -30
        camera_angle_y = 0
    
    camera_pos = (x, y, z)
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    """Handle special key inputs for camera rotation"""
    global camera_angle_x, camera_angle_y
    
    if key == GLUT_KEY_UP:
        camera_angle_x += 5
    elif key == GLUT_KEY_DOWN:
        camera_angle_x -= 5
    elif key == GLUT_KEY_LEFT:
        camera_angle_y -= 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle_y += 5
    
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    """Handle mouse inputs"""
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print(f"Mouse clicked at screen coordinates: ({x}, {y})")

def setupCamera():
    """Configure the third-person camera view"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    x, y, z = camera_pos
    
    # Calculate look-at point (center of room)
    look_x = 0
    look_y = 0
    look_z = 100
    
    # Apply camera rotation
    rad_y = math.radians(camera_angle_y)
    rad_x = math.radians(camera_angle_x)
    
    # Rotate look-at point around Y axis
    rotated_x = look_x * math.cos(rad_y) - look_z * math.sin(rad_y)
    rotated_z = look_x * math.sin(rad_y) + look_z * math.cos(rad_y)
    
    # Apply X rotation (pitch)
    final_look_z = rotated_z * math.cos(rad_x)
    final_look_y = rotated_z * math.sin(rad_x)
    
    gluLookAt(x, y, z,
              rotated_x, final_look_y, final_look_z,
              0, 0, 1)

def update_scene():
    """Update any scene animations"""
    global object_pulse
    object_pulse += 0.01
    if object_pulse > 2 * math.pi:
        object_pulse -= 2 * math.pi

def showScreen():
    """Main display function"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    update_scene()
    setup_lighting()
    setupCamera()
    
    # Draw the cabin scene
    draw_wooden_floor()
    draw_wooden_walls()
    draw_fireplace()
    draw_furniture()
    
    # Draw HUD info
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    
    draw_text(10, 770, "Cozy Cabin Interior - Third Person View", color=(1.0, 0.9, 0.3))
    draw_text(10, 740, "WASD: Move Camera | Q/E: Camera Height", color=(0.9, 0.9, 0.9))
    draw_text(10, 710, "Arrow Keys: Rotate View | R: Reset Camera", color=(0.9, 0.9, 0.9))
    draw_text(10, 680, f"Camera Position: ({camera_pos[0]:.0f}, {camera_pos[1]:.0f}, {camera_pos[2]:.0f})", 
              color=(0.7, 0.8, 1.0))
    draw_text(10, 650, f"Camera Angles: X={camera_angle_x}°, Y={camera_angle_y}°", color=(0.7, 0.8, 1.0))
    
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
    
    glutSwapBuffers()

def idle():
    """Idle function for continuous updates"""
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(100, 100)
    wind = glutCreateWindow(b"Cozy Cabin Interior - Third Person View")
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    # Set background color to dark gray
    glClearColor(0.15, 0.15, 0.15, 1.0)
    
    # Enable smooth shading
    glShadeModel(GL_SMOOTH)
    
    glutMainLoop()

if __name__ == "__main__":
    main()