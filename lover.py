from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Player position
player_pos = [0, 0, 10]   # x, y, z (z slightly above floor)
player_speed = 20


# Camera position (third person view looking at the cabin floor)
camera_pos = (0, 600, 400)  # Elevated view looking down
camera_angle_x = -40  # Look downward angle
camera_angle_y = 0
fovY = 60

# Room dimensions (just the floor area)
ROOM_SIZE = 400

# Animation variables
object_pulse = 0

# Current scene (1=Cabin, 2=Kitchen, 3=Bedroom)
current_scene = 1

# Kitchen dimensions
KITCHEN_SIZE = 300
# Bedroom dimensions
BEDROOM_SIZE = 350

def draw_player():
    """Draw the player as a simple character"""
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])

    # Body
    glColor3f(0.2, 0.8, 0.2)
    glPushMatrix()
    glScalef(20, 20, 30)
    glutSolidCube(1)
    glPopMatrix()

    # Head
    glColor3f(0.9, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glutSolidSphere(10, 16, 16)
    glPopMatrix()

    glPopMatrix()


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1.0, 1.0, 1.0)):
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

def draw_wooden_floor():
    """Draw striped wooden floor with two shades of brown"""
    glBegin(GL_QUADS)
    
    # Create stripes in the x-direction
    stripe_width = 50
    num_stripes = int((ROOM_SIZE * 2) / stripe_width)
    
    for i in range(-num_stripes//2, num_stripes//2):
        x_start = i * stripe_width
        x_end = (i + 1) * stripe_width
        
        # Alternate between two shades of brown
        if i % 2 == 0:
            glColor3f(0.6, 0.4, 0.25)  # Light brown
        else:
            glColor3f(0.45, 0.3, 0.2)   # Dark brown
        
        # Draw the stripe across the entire floor
        glVertex3f(x_start, -ROOM_SIZE, 0)
        glVertex3f(x_end, -ROOM_SIZE, 0)
        glVertex3f(x_end, ROOM_SIZE, 0)
        glVertex3f(x_start, ROOM_SIZE, 0)
    
    glEnd()

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
    
    # Large purple rug (bigger and simpler)
    rug_width = 300  # Increased from 240
    rug_height = 200  # Increased from 160
    
    # Main purple rectangle
    glColor3f(0.6, 0.2, 0.8)  # Purple color
    glBegin(GL_QUADS)
    glVertex3f(-rug_width/2, -rug_height/2, 0.5)
    glVertex3f(rug_width/2, -rug_height/2, 0.5)
    glVertex3f(rug_width/2, rug_height/2, 0.5)
    glVertex3f(-rug_width/2, rug_height/2, 0.5)
    glEnd()
    
    # Simple border - INCREASE Z VALUE TO PREVENT FLICKERING
    glColor3f(0.9, 0.9, 0.2)  # Yellow border
    border_width = 10
    border_height = 0.8  # Increased from 0.6 to prevent z-fighting
    
    glBegin(GL_QUADS)
    # Top border
    glVertex3f(-rug_width/2, -rug_height/2, border_height)
    glVertex3f(rug_width/2, -rug_height/2, border_height)
    glVertex3f(rug_width/2, -rug_height/2 + border_width, border_height)
    glVertex3f(-rug_width/2, -rug_height/2 + border_width, border_height)
    # Bottom border
    glVertex3f(-rug_width/2, rug_height/2 - border_width, border_height)
    glVertex3f(rug_width/2, rug_height/2 - border_width, border_height)
    glVertex3f(rug_width/2, rug_height/2, border_height)
    glVertex3f(-rug_width/2, rug_height/2, border_height)
    # Left border
    glVertex3f(-rug_width/2, -rug_height/2, border_height)
    glVertex3f(-rug_width/2 + border_width, -rug_height/2, border_height)
    glVertex3f(-rug_width/2 + border_width, rug_height/2, border_height)
    glVertex3f(-rug_width/2, rug_height/2, border_height)
    # Right border
    glVertex3f(rug_width/2 - border_width, -rug_height/2, border_height)
    glVertex3f(rug_width/2, -rug_height/2, border_height)
    glVertex3f(rug_width/2, rug_height/2, border_height)
    glVertex3f(rug_width/2 - border_width, rug_height/2, border_height)
    glEnd()
    
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
    
    # Wooden armchair (near bookshelf)
    glPushMatrix()
    glTranslatef(150, -120, 0)
    glRotatef(45, 0, 0, 1)
    
    # Chair base - Brown wood color
    glColor3f(0.45, 0.3, 0.2)
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

# ================= KITCHEN FUNCTIONS =================
def draw_kitchen_floor():
    """Draw kitchen floor with tile pattern"""
    glBegin(GL_QUADS)
    
    tile_size = 40
    num_tiles = int((KITCHEN_SIZE * 2) / tile_size)
    
    for i in range(-num_tiles//2, num_tiles//2):
        for j in range(-num_tiles//2, num_tiles//2):
            x_start = i * tile_size
            x_end = (i + 1) * tile_size
            y_start = j * tile_size
            y_end = (j + 1) * tile_size
            
            # Checkerboard pattern
            if (i + j) % 2 == 0:
                glColor3f(0.85, 0.85, 0.85)  # Light gray tile
            else:
                glColor3f(0.7, 0.7, 0.7)     # Dark gray tile
            
            glVertex3f(x_start, y_start, 0)
            glVertex3f(x_end, y_start, 0)
            glVertex3f(x_end, y_end, 0)
            glVertex3f(x_start, y_end, 0)
    
    glEnd()

def draw_kitchen_furniture():
    """Draw kitchen furniture and appliances"""
    glPushMatrix()
    
    # Kitchen counter (L-shaped)
    glColor3f(0.8, 0.7, 0.6)  # Light wood color
    glPushMatrix()
    glTranslatef(-KITCHEN_SIZE/2 + 50, -KITCHEN_SIZE/2 + 50, 25)
    glScalef(300, 50, 50)
    glutSolidCube(1)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(KITCHEN_SIZE/2 - 100, -KITCHEN_SIZE/2 + 50, 25)
    glScalef(100, 50, 50)
    glutSolidCube(1)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(-KITCHEN_SIZE/2 + 50, KITCHEN_SIZE/2 - 100, 25)
    glScalef(50, 200, 50)
    glutSolidCube(1)
    glPopMatrix()
    
    # Countertop (marble)
    glColor3f(0.95, 0.95, 0.95)
    glPushMatrix()
    glTranslatef(-KITCHEN_SIZE/2 + 50, -KITCHEN_SIZE/2 + 50, 50)
    glScalef(300, 50, 2)
    glutSolidCube(1)
    glPopMatrix()
    
    # Refrigerator
    glColor3f(0.9, 0.9, 1.0)
    glPushMatrix()
    glTranslatef(KITCHEN_SIZE/2 - 40, 0, 100)
    glScalef(30, 80, 60)
    glutSolidCube(1)
    glPopMatrix()
    
    # Refrigerator handle
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(KITCHEN_SIZE/2 - 55, 0, 100)
    glScalef(2, 15, 2)
    glutSolidCube(1)
    glPopMatrix()
    
    # Stove
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(-KITCHEN_SIZE/2 + 100, KITCHEN_SIZE/2 - 100, 25)
    glScalef(60, 60, 50)
    glutSolidCube(1)
    glPopMatrix()
    
    # Stove burners
    glColor3f(0.5, 0.5, 0.5)
    for x_offset in [-20, 20]:
        for y_offset in [-20, 20]:
            glPushMatrix()
            glTranslatef(-KITCHEN_SIZE/2 + 100 + x_offset, KITCHEN_SIZE/2 - 100 + y_offset, 50)
            glutSolidTorus(3, 8, 12, 12)
            glPopMatrix()
    
    # Sink
    glColor3f(0.8, 0.8, 0.9)
    glPushMatrix()
    glTranslatef(-KITCHEN_SIZE/2 + 200, -KITCHEN_SIZE/2 + 50, 25)
    glScalef(80, 40, 20)
    glutSolidCube(1)
    glPopMatrix()
    
    # Sink bowl
    glColor3f(0.6, 0.6, 0.7)
    glPushMatrix()
    glTranslatef(-KITCHEN_SIZE/2 + 200, -KITCHEN_SIZE/2 + 50, 35)
    glScalef(1, 1, 0.8)
    glutSolidSphere(20, 16, 16)
    glPopMatrix()
    
    # Kitchen table
    glColor3f(0.6, 0.4, 0.3)
    glPushMatrix()
    glTranslatef(100, 100, 30)
    glScalef(80, 120, 60)
    glutSolidCube(1)
    glPopMatrix()
    
    # Tabletop
    glColor3f(0.5, 0.35, 0.25)
    glPushMatrix()
    glTranslatef(100, 100, 60)
    glScalef(90, 130, 5)
    glutSolidCube(1)
    glPopMatrix()
    
    # Chairs around table
    chair_positions = [(60, 160), (140, 160), (60, 40), (140, 40)]
    for x, y in chair_positions:
        glPushMatrix()
        glTranslatef(x, y, 30)
        
        # Chair seat
        glColor3f(0.4, 0.3, 0.2)
        glPushMatrix()
        glTranslatef(0, 0, 25)
        glScalef(20, 20, 5)
        glutSolidCube(1)
        glPopMatrix()
        
        # Chair back
        glPushMatrix()
        glTranslatef(0, 10, 45)
        glScalef(20, 5, 30)
        glutSolidCube(1)
        glPopMatrix()
        
        # Chair legs
        glColor3f(0.3, 0.2, 0.1)
        for leg_x in [-8, 8]:
            for leg_y in [-8, 8]:
                glPushMatrix()
                glTranslatef(leg_x, leg_y, 12)
                glScalef(3, 3, 25)
                glutSolidCube(1)
                glPopMatrix()
        
        glPopMatrix()
    
    # Cabinet above counter
    glColor3f(0.7, 0.6, 0.5)
    glPushMatrix()
    glTranslatef(-KITCHEN_SIZE/2 + 150, -KITCHEN_SIZE/2 + 50, 125)
    glScalef(200, 50, 40)
    glutSolidCube(1)
    glPopMatrix()
    
    glPopMatrix()

# ================= BEDROOM FUNCTIONS =================
def draw_bedroom_floor():
    """Draw bedroom floor with carpet"""
    glBegin(GL_QUADS)
    
    # Main carpet area
    glColor3f(0.3, 0.5, 0.7)  # Blue carpet
    glVertex3f(-BEDROOM_SIZE, -BEDROOM_SIZE, 0)
    glVertex3f(BEDROOM_SIZE, -BEDROOM_SIZE, 0)
    glVertex3f(BEDROOM_SIZE, BEDROOM_SIZE, 0)
    glVertex3f(-BEDROOM_SIZE, BEDROOM_SIZE, 0)
    
    # Wooden border around carpet
    border_width = 20
    glColor3f(0.5, 0.35, 0.25)
    # Top border
    glVertex3f(-BEDROOM_SIZE, BEDROOM_SIZE - border_width, 0.1)
    glVertex3f(BEDROOM_SIZE, BEDROOM_SIZE - border_width, 0.1)
    glVertex3f(BEDROOM_SIZE, BEDROOM_SIZE, 0.1)
    glVertex3f(-BEDROOM_SIZE, BEDROOM_SIZE, 0.1)
    # Bottom border
    glVertex3f(-BEDROOM_SIZE, -BEDROOM_SIZE, 0.1)
    glVertex3f(BEDROOM_SIZE, -BEDROOM_SIZE, 0.1)
    glVertex3f(BEDROOM_SIZE, -BEDROOM_SIZE + border_width, 0.1)
    glVertex3f(-BEDROOM_SIZE, -BEDROOM_SIZE + border_width, 0.1)
    # Left border
    glVertex3f(-BEDROOM_SIZE, -BEDROOM_SIZE, 0.1)
    glVertex3f(-BEDROOM_SIZE + border_width, -BEDROOM_SIZE, 0.1)
    glVertex3f(-BEDROOM_SIZE + border_width, BEDROOM_SIZE, 0.1)
    glVertex3f(-BEDROOM_SIZE, BEDROOM_SIZE, 0.1)
    # Right border
    glVertex3f(BEDROOM_SIZE - border_width, -BEDROOM_SIZE, 0.1)
    glVertex3f(BEDROOM_SIZE, -BEDROOM_SIZE, 0.1)
    glVertex3f(BEDROOM_SIZE, BEDROOM_SIZE, 0.1)
    glVertex3f(BEDROOM_SIZE - border_width, BEDROOM_SIZE, 0.1)
    
    glEnd()

def draw_bedroom_furniture():
    """Draw bedroom furniture"""
    glPushMatrix()
    
    # Bed
    glColor3f(0.8, 0.1, 0.3)  # Red bed frame
    glPushMatrix()
    glTranslatef(-100, 0, 30)
    glScalef(180, 120, 60)
    glutSolidCube(1)
    glPopMatrix()
    
    # Mattress
    glColor3f(0.9, 0.9, 0.95)
    glPushMatrix()
    glTranslatef(-100, 0, 90)
    glScalef(190, 130, 30)
    glutSolidCube(1)
    glPopMatrix()
    
    # Pillows
    glColor3f(0.2, 0.5, 0.8)
    for y_offset in [-40, 40]:
        glPushMatrix()
        glTranslatef(-180, y_offset, 105)
        glScalef(20, 40, 10)
        glutSolidCube(1)
        glPopMatrix()
    
    # Bedside tables
    for x_offset in [-200, 0]:
        glPushMatrix()
        glTranslatef(x_offset, 100, 40)
        
        # Table
        glColor3f(0.4, 0.25, 0.15)
        glPushMatrix()
        glTranslatef(0, 0, 40)
        glScalef(50, 50, 80)
        glutSolidCube(1)
        glPopMatrix()
        
        # Tabletop
        glColor3f(0.35, 0.2, 0.1)
        glPushMatrix()
        glTranslatef(0, 0, 80)
        glScalef(60, 60, 5)
        glutSolidCube(1)
        glPopMatrix()
        
        # Lamp on table
        glColor3f(0.9, 0.9, 0.7)
        glPushMatrix()
        glTranslatef(0, 0, 110)
        glutSolidCone(10, 30, 12, 12)
        glPopMatrix()
        
        # Lamp base
        glColor3f(0.7, 0.7, 0.5)
        glPushMatrix()
        glTranslatef(0, 0, 85)
        glScalef(1, 1, 1.5)
        glutSolidCone(8, 20, 12, 12)
        glPopMatrix()
        
        glPopMatrix()
    
    # Wardrobe
    glColor3f(0.5, 0.35, 0.25)
    glPushMatrix()
    glTranslatef(200, 0, 100)
    glScalef(60, 120, 200)
    glutSolidCube(1)
    glPopMatrix()
    
    # Wardrobe doors
    glColor3f(0.4, 0.3, 0.2)
    for y_offset in [-40, 40]:
        glPushMatrix()
        glTranslatef(230, y_offset, 100)
        glScalef(2, 50, 180)
        glutSolidCube(1)
        glPopMatrix()
    
    # Wardrobe handles
    glColor3f(0.8, 0.8, 0.8)
    for y_offset in [-40, 40]:
        glPushMatrix()
        glTranslatef(231, y_offset, 100)
        glutSolidSphere(3, 8, 8)
        glPopMatrix()
    
    # Dresser
    glColor3f(0.6, 0.45, 0.35)
    glPushMatrix()
    glTranslatef(200, -150, 50)
    glScalef(100, 60, 100)
    glutSolidCube(1)
    glPopMatrix()
    
    # Dresser drawers
    glColor3f(0.5, 0.35, 0.25)
    for y_offset in [-20, 20]:
        glPushMatrix()
        glTranslatef(230, -150 + y_offset, 50)
        glScalef(5, 25, 40)
        glutSolidCube(1)
        glPopMatrix()
    
    # Mirror above dresser
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.8, 0.9, 1.0, 0.3)
    glPushMatrix()
    glTranslatef(200, -150, 150)
    glScalef(110, 70, 5)
    glutSolidCube(1)
    glPopMatrix()
    glDisable(GL_BLEND)
    
    # Mirror frame
    glColor3f(0.3, 0.2, 0.1)
    glPushMatrix()
    glTranslatef(200, -150, 152)
    glScalef(120, 80, 10)
    glutSolidCube(1)
    glPopMatrix()
    
    # Desk
    glColor3f(0.4, 0.3, 0.2)
    glPushMatrix()
    glTranslatef(-100, -150, 40)
    glScalef(120, 60, 80)
    glutSolidCube(1)
    glPopMatrix()
    
    # Desk chair
    glPushMatrix()
    glTranslatef(-100, -220, 30)
    
    # Chair seat
    glColor3f(0.3, 0.2, 0.5)
    glPushMatrix()
    glTranslatef(0, 0, 25)
    glScalef(40, 40, 10)
    glutSolidCube(1)
    glPopMatrix()
    
    # Chair back
    glPushMatrix()
    glTranslatef(0, 20, 60)
    glScalef(40, 10, 50)
    glutSolidCube(1)
    glPopMatrix()
    
    # Chair legs
    glColor3f(0.2, 0.2, 0.2)
    for leg_x in [-15, 15]:
        for leg_y in [-15, 15]:
            glPushMatrix()
            glTranslatef(leg_x, leg_y, 12)
            glScalef(4, 4, 25)
            glutSolidCube(1)
            glPopMatrix()
    
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
    
    # Additional light (position depends on scene)
    if current_scene == 1:  # Cabin - fireplace light
        glLightfv(GL_LIGHT1, GL_POSITION, [0, -ROOM_SIZE + 50, 60, 1])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.7, 0.3, 0.1, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.3, 0.15, 0.05, 1.0])
    elif current_scene == 2:  # Kitchen - overhead light
        glLightfv(GL_LIGHT1, GL_POSITION, [0, 0, 300, 1])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.9, 0.9, 0.8, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.5, 0.5, 0.4, 1.0])
    else:  # Bedroom - bedside lamp light
        glLightfv(GL_LIGHT1, GL_POSITION, [-200, 100, 140, 1])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.8, 0.8, 0.6, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.4, 0.4, 0.3, 1.0])
    
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.5, 0.25, 0.1, 1.0])

def keyboardListener(key, x, y):
    """Handle keyboard inputs for camera movement and scene switching"""
    global camera_pos, camera_angle_x, camera_angle_y, current_scene
    
    key = key.decode('utf-8').lower()
    
    # Scene switching
    if key == '1':
        current_scene = 1  # Cabin
        print("Switched to Cabin scene")
    elif key == '2':
        current_scene = 2  # Kitchen
        print("Switched to Kitchen scene")
    elif key == '3':
        current_scene = 3  # Bedroom
        print("Switched to Bedroom scene")
    
    # Camera movement (only if not switching scenes)
    elif key in ['w', 's', 'a', 'd', 'q', 'e', 'r']:
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
    """Arrow keys move the player"""
    global player_pos

    if key == GLUT_KEY_UP:
        player_pos[1] += player_speed
    elif key == GLUT_KEY_DOWN:
        player_pos[1] -= player_speed
    elif key == GLUT_KEY_LEFT:
        player_pos[0] -= player_speed
    elif key == GLUT_KEY_RIGHT:
        player_pos[0] += player_speed
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
    
    # Draw the appropriate scene based on current_scene
    if current_scene == 1:
        # Draw Cabin scene
        draw_wooden_floor()
        draw_player()
        draw_fireplace()
        draw_furniture()
        scene_name = "CABIN"
    elif current_scene == 2:
        # Draw Kitchen scene
        draw_kitchen_floor()
        draw_player()
        draw_kitchen_furniture()
        scene_name = "KITCHEN"
    else:  # current_scene == 3
        # Draw Bedroom scene
        draw_bedroom_floor()
        draw_player()
        draw_bedroom_furniture()
        scene_name = "BEDROOM"
    
    # Draw HUD info
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    
    draw_text(10, 770, f"Current Scene: {scene_name} - Press 1, 2, or 3 to switch", color=(1.0, 0.9, 0.3))
    draw_text(10, 740, "WASD: Move Camera | Q/E: Camera Height", color=(0.9, 0.9, 0.9))
    draw_text(10, 710, "Arrow Keys: Rotate View | R: Reset Camera", color=(0.9, 0.9, 0.9))
    draw_text(10, 680, f"Camera Position: ({camera_pos[0]:.0f}, {camera_pos[1]:.0f}, {camera_pos[2]:.0f})", 
              color=(0.7, 0.8, 1.0))
    draw_text(10, 650, f"Camera Angles: X={camera_angle_x}°, Y={camera_angle_y}°", color=(0.7, 0.8, 1.0))
    draw_text(10, 620, "1=Cabin | 2=Kitchen | 3=Bedroom", color=(0.8, 0.6, 0.4))
    
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
    wind = glutCreateWindow(b"Multi-Scene: Cabin, Kitchen, Bedroom")
    
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
