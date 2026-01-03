from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

# Camera position (third person view looking at the cabin floor)
camera_pos = (0, 600, 400)  # Elevated view looking down
camera_angle_x = -40  # Look downward angle
camera_angle_y = 0
fovY = 60

# Room dimensions (just the floor area)
ROOM_SIZE = 400
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
    """Draw detailed wooden floor with planks and pattern"""
    glPushMatrix()
    
    # Base floor color
    glColor3f(0.45, 0.3, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-ROOM_SIZE, -ROOM_SIZE, 0)
    glVertex3f(ROOM_SIZE, -ROOM_SIZE, 0)
    glVertex3f(ROOM_SIZE, ROOM_SIZE, 0)
    glVertex3f(-ROOM_SIZE, ROOM_SIZE, 0)
    glEnd()
    
    # Draw individual wooden planks
    plank_width = 50
    plank_length = ROOM_SIZE * 2
    num_planks = int(plank_length / plank_width)
    
    for i in range(-num_planks//2, num_planks//2):
        x_start = i * plank_width
        x_end = (i + 1) * plank_width
        
        # Alternate plank colors
        if i % 2 == 0:
            glColor3f(0.5, 0.35, 0.25)  # Light wood
        else:
            glColor3f(0.4, 0.28, 0.18)  # Dark wood
        
        glBegin(GL_QUADS)
        glVertex3f(x_start, -ROOM_SIZE, 0.1)
        glVertex3f(x_end, -ROOM_SIZE, 0.1)
        glVertex3f(x_end, ROOM_SIZE, 0.1)
        glVertex3f(x_start, ROOM_SIZE, 0.1)
        glEnd()
        
        # Draw plank separations (gaps between planks)
        glColor3f(0.25, 0.15, 0.1)
        glLineWidth(1.5)
        glBegin(GL_LINES)
        glVertex3f(x_end, -ROOM_SIZE, 0.15)
        glVertex3f(x_end, ROOM_SIZE, 0.15)
        glEnd()
    
    # Draw floorboards in the other direction (for checker pattern effect)
    for i in range(-num_planks//2, num_planks//2):
        y_start = i * plank_width
        y_end = (i + 1) * plank_width
        
        if i % 2 == 0:
            glColor4f(0.55, 0.4, 0.3, 0.3)  # Semi-transparent light wood
        else:
            glColor4f(0.45, 0.33, 0.23, 0.3)  # Semi-transparent dark wood
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_QUADS)
        glVertex3f(-ROOM_SIZE, y_start, 0.2)
        glVertex3f(ROOM_SIZE, y_start, 0.2)
        glVertex3f(ROOM_SIZE, y_end, 0.2)
        glVertex3f(-ROOM_SIZE, y_end, 0.2)
        glEnd()
        glDisable(GL_BLEND)
    
    glPopMatrix()

def draw_fireplace():
    """Draw fireplace standing on the floor"""
    glPushMatrix()
    glTranslatef(0, -ROOM_SIZE + 50, 0)
    
    # Stone fireplace base
    glColor3f(0.35, 0.35, 0.35)
    
    # Base platform
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glScalef(220, 60, 40)
    glutSolidCube(1)
    glPopMatrix()
    
    # Left pillar
    glPushMatrix()
    glTranslatef(-80, 0, 60)
    glScalef(40, 60, 120)
    glutSolidCube(1)
    glPopMatrix()
    
    # Right pillar
    glPushMatrix()
    glTranslatef(80, 0, 60)
    glScalef(40, 60, 120)
    glutSolidCube(1)
    glPopMatrix()
    
    # Mantel shelf
    glColor3f(0.25, 0.25, 0.25)
    glPushMatrix()
    glTranslatef(0, 0, 120)
    glScalef(240, 10, 15)
    glutSolidCube(1)
    glPopMatrix()
    
    # Fireplace opening
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 30, 50)
    glScalef(140, 50, 60)
    glutSolidCube(1)
    glPopMatrix()
    
    # Static fire
    pulse_scale = 0.9 + 0.1 * math.sin(object_pulse * 2)
    
    # Fire base (orange sphere)
    glColor3f(1.0, 0.5, 0.0)
    glPushMatrix()
    glTranslatef(0, 50, 60)
    glScalef(pulse_scale, pulse_scale, pulse_scale)
    glutSolidSphere(18, 16, 16)
    glPopMatrix()
    
    # Middle flames (red cones)
    glColor3f(1.0, 0.2, 0.0)
    for angle in [0, 120, 240]:
        rad_angle = math.radians(angle)
        x_offset = 10 * math.cos(rad_angle)
        z_offset = 10 * math.sin(rad_angle)
        
        glPushMatrix()
        glTranslatef(x_offset, 65, 65 + z_offset)
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(6, 20, 8, 8)
        glPopMatrix()
    
    # Top flames (yellow)
    glColor3f(1.0, 0.9, 0.2)
    for angle in [60, 180, 300]:
        rad_angle = math.radians(angle)
        x_offset = 8 * math.cos(rad_angle)
        z_offset = 8 * math.sin(rad_angle)
        
        glPushMatrix()
        glTranslatef(x_offset, 75, 70 + z_offset)
        glutSolidSphere(5, 8, 8)
        glPopMatrix()
    
    # Logs in fireplace
    glColor3f(0.35, 0.22, 0.12)
    
    # Bottom log
    glPushMatrix()
    glTranslatef(0, 20, 40)
    glRotatef(30, 0, 1, 0)
    glScalef(50, 10, 10)
    glutSolidCube(1)
    glPopMatrix()
    
    # Top log
    glPushMatrix()
    glTranslatef(0, 25, 55)
    glRotatef(-30, 0, 1, 0)
    glScalef(45, 8, 8)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()

def draw_furniture():
    """Draw furniture arranged on the floor"""
    glPushMatrix()
    
    # Large Persian rug in center
    glBegin(GL_QUADS)
    # Rug base (deep red)
    glColor3f(0.7, 0.15, 0.1)
    glVertex3f(-120, -80, 0.5)
    glVertex3f(120, -80, 0.5)
    glVertex3f(120, 80, 0.5)
    glVertex3f(-120, 80, 0.5)
    
    # Rug border (gold)
    glColor3f(0.9, 0.8, 0.2)
    border = 15
    # Top border
    glVertex3f(-120, -80, 0.6)
    glVertex3f(120, -80, 0.6)
    glVertex3f(120, -80 + border, 0.6)
    glVertex3f(-120, -80 + border, 0.6)
    # Bottom border
    glVertex3f(-120, 80 - border, 0.6)
    glVertex3f(120, 80 - border, 0.6)
    glVertex3f(120, 80, 0.6)
    glVertex3f(-120, 80, 0.6)
    # Left border
    glVertex3f(-120, -80, 0.6)
    glVertex3f(-120 + border, -80, 0.6)
    glVertex3f(-120 + border, 80, 0.6)
    glVertex3f(-120, 80, 0.6)
    # Right border
    glVertex3f(120 - border, -80, 0.6)
    glVertex3f(120, -80, 0.6)
    glVertex3f(120, 80, 0.6)
    glVertex3f(120 - border, 80, 0.6)
    glEnd()
    
    # Sofa facing fireplace (left side)
    glPushMatrix()
    glTranslatef(-180, 0, 0)
    
    # Sofa base
    glColor3f(0.5, 0.3, 0.6)  # Purple fabric
    glPushMatrix()
    glTranslatef(0, 0, 35)
    glScalef(80, 40, 70)
    glutSolidCube(1)
    glPopMatrix()
    
    # Sofa back
    glPushMatrix()
    glTranslatef(0, 25, 75)
    glScalef(80, 10, 40)
    glutSolidCube(1)
    glPopMatrix()
    
    # Sofa arms
    glColor3f(0.4, 0.2, 0.5)
    # Left arm
    glPushMatrix()
    glTranslatef(-40, 0, 70)
    glScalef(10, 40, 60)
    glutSolidCube(1)
    glPopMatrix()
    # Right arm
    glPushMatrix()
    glTranslatef(40, 0, 70)
    glScalef(10, 40, 60)
    glutSolidCube(1)
    glPopMatrix()
    
    # Sofa cushions
    glColor3f(0.6, 0.4, 0.7)
    for y_pos in [-10, 10]:
        glPushMatrix()
        glTranslatef(0, y_pos, 75)
        glScalef(70, 15, 10)
        glutSolidCube(1)
        glPopMatrix()
    
    glPopMatrix()
    
    # Coffee table on rug
    glPushMatrix()
    glTranslatef(0, 0, 0)
    
    # Glass table top (semi-transparent)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.8, 0.9, 1.0, 0.6)
    glPushMatrix()
    glTranslatef(0, 0, 50)
    glScalef(60, 40, 2)
    glutSolidCube(1)
    glPopMatrix()
    glDisable(GL_BLEND)
    
    # Table legs (metal/chrome)
    glColor3f(0.7, 0.7, 0.8)
    leg_positions = [(-25, -15), (25, -15), (-25, 15), (25, 15)]
    for x, y in leg_positions:
        glPushMatrix()
        glTranslatef(x, y, 25)
        glScalef(4, 4, 50)
        glutSolidCube(1)
        glPopMatrix()
    
    # Items on table
    # Book
    glColor3f(0.2, 0.3, 0.8)
    glPushMatrix()
    glTranslatef(-15, 0, 53)
    glScalef(12, 20, 3)
    glutSolidCube(1)
    glPopMatrix()
    
    # Cup
    glColor3f(0.9, 0.9, 0.9)
    glPushMatrix()
    glTranslatef(15, -10, 53)
    glutSolidTeapot(8)
    glPopMatrix()
    
    # Candle
    glColor3f(0.9, 0.9, 0.8)
    glPushMatrix()
    glTranslatef(15, 10, 53)
    glScalef(1, 1, 2)
    glutSolidCone(4, 15, 8, 8)
    glPopMatrix()
    
    glPopMatrix()
    
    # Bookshelf (right side)
    glPushMatrix()
    glTranslatef(250, 0, 0)
    
    # Bookshelf frame
    glColor3f(0.4, 0.25, 0.15)
    glPushMatrix()
    glTranslatef(0, 0, 100)
    glScalef(20, 100, 180)
    glutSolidCube(1)
    glPopMatrix()
    
    # Shelves
    glColor3f(0.35, 0.2, 0.1)
    for height in [40, 100, 160]:
        glPushMatrix()
        glTranslatef(5, 0, height)
        glScalef(10, 95, 5)
        glutSolidCube(1)
        glPopMatrix()
    
    # Books
    book_colors = [
        (0.8, 0.2, 0.2), (0.2, 0.2, 0.8), (0.2, 0.8, 0.2),
        (0.8, 0.8, 0.2), (0.8, 0.2, 0.8), (0.2, 0.8, 0.8)
    ]
    
    for i, color in enumerate(book_colors):
        glColor3f(*color)
        row = i // 3
        col = i % 3
        glPushMatrix()
        glTranslatef(8, -40 + col * 30, 50 + row * 55)
        glRotatef(90, 0, 0, 1)
        glScalef(8, 25, 4)
        glutSolidCube(1)
        glPopMatrix()
    
    glPopMatrix()
    
    # Armchair (near bookshelf)
    glPushMatrix()
    glTranslatef(150, -120, 0)
    glRotatef(45, 0, 0, 1)
    
    # Chair base
    glColor3f(0.3, 0.5, 0.3)  # Green fabric
    glPushMatrix()
    glTranslatef(0, 0, 30)
    glScalef(40, 40, 60)
    glutSolidCube(1)
    glPopMatrix()
    
    # Chair back
    glPushMatrix()
    glTranslatef(0, 25, 70)
    glScalef(40, 10, 40)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()
    
    # Floor lamp (near armchair)
    glPushMatrix()
    glTranslatef(100, -180, 0)
    
    # Lamp base
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0, 0, 10)
    glScalef(15, 15, 20)
    glutSolidCube(1)
    glPopMatrix()
    
    # Lamp pole
    glPushMatrix()
    glTranslatef(0, 0, 110)
    glScalef(3, 3, 200)
    glutSolidCube(1)
    glPopMatrix()
    
    # Lamp shade
    glColor3f(0.9, 0.9, 0.8)
    glPushMatrix()
    glTranslatef(0, 0, 210)
    glScalef(1, 1, 1.5)
    glutSolidCone(20, 40, 12, 12)
    glPopMatrix()
    
    # Light glow
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 0.9, 0.4)
    glPushMatrix()
    glTranslatef(0, 0, 230)
    glutSolidSphere(30, 12, 12)
    glPopMatrix()
    glDisable(GL_BLEND)
    
    glPopMatrix()
    
    glPopMatrix()

def setup_lighting():
    """Setup lighting for the open scene"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    
    # Main ambient light (like sunlight)
    glLightfv(GL_LIGHT0, GL_POSITION, [300, 300, 500, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.4, 0.4, 0.4, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    # Fireplace light
    glLightfv(GL_LIGHT1, GL_POSITION, [0, -ROOM_SIZE + 50, 60, 1])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.7, 0.3, 0.1, 1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.3, 0.15, 0.05, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.5, 0.25, 0.1, 1.0])

def keyboardListener(key, x, y):
    """Handle keyboard inputs for camera movement"""
    global camera_pos, camera_angle_x, camera_angle_y
    
    key = key.decode('utf-8').lower()
    x, y, z = camera_pos
    
    # Camera movement
    if key == 'w':  # Move camera forward/zoom in
        z = max(z - 30, 200)
    elif key == 's':  # Move camera backward/zoom out
        z = min(z + 30, 800)
    elif key == 'a':  # Move camera left
        x -= 30
    elif key == 'd':  # Move camera right
        x += 30
    elif key == 'q':  # Move camera up
        y += 30
    elif key == 'e':  # Move camera down
        y = max(y - 30, 200)
    elif key == 'r':  # Reset camera
        x, y, z = (0, 600, 400)
        camera_angle_x = -40
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
        print(f"Screen click: ({x}, {y})")

def setupCamera():
    """Configure the third-person camera view"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    x, y, z = camera_pos
    
    # Look at the center of the floor area
    look_x = 0
    look_y = 0
    look_z = 50
    
    # Apply camera rotation
    rad_y = math.radians(camera_angle_y)
    rad_x = math.radians(camera_angle_x)
    
    # Rotate look-at point
    rotated_x = look_x * math.cos(rad_y) - look_z * math.sin(rad_y)
    rotated_z = look_x * math.sin(rad_y) + look_z * math.cos(rad_y)
    
    # Apply pitch
    final_look_z = rotated_z * math.cos(rad_x)
    final_look_y = rotated_z * math.sin(rad_x)
    
    gluLookAt(x, y, z,
              rotated_x, final_look_y, final_look_z,
              0, 0, 1)

def update_scene():
    """Update scene animations"""
    global object_pulse
    object_pulse += 0.015
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
    
    # Draw the scene (no walls or roof)
    draw_wooden_floor()
    draw_fireplace()
    draw_furniture()
    
    # Draw HUD info
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    
    draw_text(10, 770, "Open Cabin Floor Layout - Third Person View", color=(1.0, 0.9, 0.3))
    draw_text(10, 740, "WASD: Move Camera | Q/E: Camera Height", color=(0.9, 0.9, 0.9))
    draw_text(10, 710, "Arrow Keys: Rotate View | R: Reset Camera", color=(0.9, 0.9, 0.9))
    draw_text(10, 680, f"Camera Position: ({camera_pos[0]:.0f}, {camera_pos[1]:.0f}, {camera_pos[2]:.0f})", 
              color=(0.7, 0.8, 1.0))
    draw_text(10, 650, f"Camera Angles: X={camera_angle_x}°, Y={camera_angle_y}°", color=(0.7, 0.8, 1.0))
    draw_text(10, 620, "No Walls/Roof - Open Floor Plan", color=(0.8, 0.6, 0.4))
    
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
    wind = glutCreateWindow(b"Open Cabin Floor - No Walls or Roof")
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    # Set background color to simulate sky/outdoors
    glClearColor(0.2, 0.25, 0.3, 1.0)  # Bluish-gray for open sky
    
    # Enable smooth shading
    glShadeModel(GL_SMOOTH)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
