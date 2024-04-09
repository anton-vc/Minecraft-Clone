# import libraries
# import everything from the Ursina game engine without having to call ursina all the time
from ursina import *
# import an extra module to be able to create a player
from ursina.prefabs.first_person_controller import FirstPersonController

# create an instance of the ursina app
app = Ursina()

# define game variables
# texture dictionary
textures = {
    'grass_block':   load_texture('assets/textures/grass_block.png'),
    'grass_block1':  load_texture('assets/textures/groundEarth.png'),
    'dirt_block':    load_texture('assets/textures/dirt_block.png'),
    'dirt_block1':   load_texture('assets/textures/groundMud.png'),
    'stone_block':   load_texture('assets/textures/stone_block.png'),
    'stone_block1':  load_texture('assets/textures/wallStone.png'),
    'brick_block':   load_texture('assets/textures/brick_block.png'),
    'bedrock_block': load_texture('assets/textures/stone07.png'),
    'skybox':        load_texture('assets/textures/skybox.png'),
    'arm':           load_texture('assets/textures/arm.png')
}

# load audio
punch_sound = Audio('assets/audio/punch_sound', loop = False, autoplay = False)

# standard block is a grass block
block_pick = 'grass_block'
selected_block = 'grass_block1'

# make some alterations to the window view
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.exit_button.visible = False

# update function that runs every frame
def update():
    global block_pick

    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.active()
        mini_block.active()
    else:
        arm.passive()
        mini_block.passive()

    if held_keys['1']: block_pick = 'grass_block'
    if held_keys['2']: block_pick = 'dirt_block'
    if held_keys['3']: block_pick = 'stone_block'
    if held_keys['4']: block_pick = 'brick_block'
    if held_keys['5']: block_pick = 'arm'
    if held_keys['6']: block_pick = 'arm'
    if held_keys['7']: block_pick = 'arm'
    if held_keys['8']: block_pick = 'arm'
    if held_keys['9']: block_pick = 'arm'
    if held_keys['0']: block_pick = 'arm'

# define a class for Voxel, which inherits from the Button class
class Voxel(Button):
    def __init__(self, position = (0,0,0), block_type = 'grass_block'):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/models/block',
            origin_y = 0,
            texture = textures.get(block_type),
            color = color.color(0,0,random.uniform(0.9,1)),
            scale = 0.5,
            collider = 'box'
        )

        self.block_type = block_type

    # function to create or destroy blocks
    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                voxel = Voxel(position = self.position + mouse.normal, block_type = block_pick)

            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)

# define a class for a block
class Block(Button):
    def __init__(self, position = (0,0,0), block_type = 'grass_block1'):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/models/block_model',
            scale = 1,
            origin_y = 0,
            texture = textures.get(block_type),
            color = color.color(0,0,random.uniform(0.9,1)),
            collider = 'box'
        )

        self.block_type = block_type

    # function to create or destroy blocks
    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                block = Block(position = self.position + mouse.normal, block_type = selected_block)

            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)

# define a class to put the sky texture in the sky
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = textures.get('skybox'),
            scale = 150,
            double_sided = True
        )

# define a class to be able to see an arm on the screen
class Arm(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/models/arm',
            texture = textures.get('arm'),
            scale = 0.2,
            rotation = Vec3(150,-10,0),
            position = Vec2(0.4,-0.6)
        )

    # a method to change the position of the arm when a button is clicked
    def active(self):
        self.position = Vec2(0.3,-0.5)

    # a method to change the position of the arm back to its default state
    def passive(self):
        self.position = Vec2(0.4,-0.6)

# define a class for a holding block
class Mini_Block(Entity):
    def __init__(self, block_type = 'grass_block1'):
        super().__init__(
            parent = camera,
            model = 'assets/models/block_model',
            scale = 0.2,
            texture = textures.get(block_type),
            position = (0.35, -0.25, 0.5),
            rotation = (-15, -30, -5)
        )

        self.block_type = block_type

    # a method to change the position of the mini block when a button is clicked
    def active(self):
        self.position = (0.45, -0.35, 0.6)
        self.rotation = (-5, -20, 5)

    # a method to change the position of the mini block back to its default state
    def passive(self):
        self.position = (0.35, -0.25, 0.5)
        self.rotation = (-15, -30, -5)

# create instances of Voxel in a plane
for x in range(-10, 10):
    for z in range(-10, 10):
        voxel = Voxel(position = (x,0,z), block_type = 'grass_block')

# create instances of Block in a plane
for x in range(-10, 10):
    for z in range(10, 30):
        block = Block(position = (x,0,z), block_type = 'grass_block1')

# create the player
player = FirstPersonController(
    mouse_sensitivity = Vec2(100,100),
    position = (0,5,0)
)

# create the sky
sky = Sky()

# create the arm
arm = Arm()

# create a mini block that the player holds
mini_block = Mini_Block(block_type = selected_block)

# run the app
app.run()
