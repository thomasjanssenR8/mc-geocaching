import math
import os
from mcpi.minecraft import Minecraft
from mcpi import block, vec3, event
from time import sleep

# Define block IDs
stone = 1
flower = 38
grass = 2
tnt = 46
lava = 10
water = 8
air = 0
torch = 50
wood_planks = 5
door_wood = 64
chest = 54
snow = 80
obsidian = 49
books = 47

def start_game():
    """Initialize the game"""
    # Initialize the game
    global mc, x, y, z
    mc = Minecraft.create()
    mc.setting('world_immutable', True)
    mc.postToChat('Hello world! Ready to start geocaching?')

    # Init player position and environment
    mc.player.setPos(0, 1, 0)
    x, y, z = mc.player.getPos()
    mc.setBlocks(-128, -64, -128, 128, 64, 128, air)
    mc.setBlocks(-128, 0, -128, 128, 0, 128, grass)

def build_door(x, y, z, block=door_wood):
    """Create a door at the give coordinates"""
    mc.setBlock(x, y, z, block, 0)
    mc.setBlock(x, y+1, z, block, 8)

def check_block_hit(x,y,z):
	"""Wait until a block at the given coordinates is hit by the player's pickaxe."""
    hit = False
    while not hit:
        block_events = mc.events.pollBlockHits()
        for event in block_events:
            if event.pos.x==x and event.pos.y==y and event.pos.z==z:
                print('Block hit!')
                hit = True
        sleep(0.1)

def GC001():
    """GC#001: Tutorial"""
    # Build a cave from woodplanks, add 4 torches and a door
    mc.setBlocks(-4, +0, -4, +4, +4, +4, wood_planks)
    mc.setBlocks(-3, +1, -3, +3, +3, +3, air)
    mc.setBlock(+3, +3, +3, torch)
    mc.setBlock(+3, +3, -3, torch)
    mc.setBlock(-3, +3, +3, torch)
    mc.setBlock(-3, +3, -3, torch)
    build_door(4, 1, 0)

    # Show text when the player opens the door
    while(mc.getBlockWithData(4, 1, 0).data is not 4):
        sleep(0.1)
    mc.postToChat('Geocache GC#001: A magical discovery')
    mc.postToChat('Right click with your pickaxe to open a geocache!')

    mc.setBlock(12, 1, 0, chest,4)
    check_block_hit(12, 1, 0)  # check if chest is hit
    mc.setBlock(12, 1, 0, books)  # turn chest into books
    mc.postToChat('Congrats! You just found your first virtual geocache!')
    sleep(3)

def GC002():
    """GC#002: QR-code"""
    mc.postToChat("Let's make it somewhat more challenging...")
    mc.postToChat("I expect a Quick Response!")
    sleep(2)

    # Create and read QR code file
    os.system("qrencode -t ASCII 'Well done! Go to (48, 1, 15) for the next adventure!' | sed 's/  / /g' | sed 's/##/#/g' > /home/pi/Desktop/geocaching-mc/mcqr.txt")
    qrc = open('/home/pi/Desktop/geocaching-mc/mcqr.txt', 'r')
    qr_array = []
    for line in qrc:
        qr_array.append(line)
    qrc.close()

    qr_x, qr_y, qr_z = 30, 1, -20  # nPos
    pposy = 1

    # Build QR code
    for i in reversed(qr_array):
        qr_y = pposy + len(i)
        for j in range(0, len(i)):
            if i[j] == " ":
                block = snow
            if i[j] == "#":
                block = obsidian
            qr_y = qr_y-1
            mc.setBlock(qr_x, qr_y, qr_z, block)
        qr_z = qr_z+1

    mc.setBlocks(31, 1, -20, 51, 1, 20, flower)
    check_block_hit(48, 1, 15)  # if player hits correct flower, turn it into a chest
    mc.setBlock(48, 1, 15, chest, 3)
    check_block_hit(48, 1, 15)  # if player opens chest, turn into books
    mc.setBlock(48, 1, 15, books)
    mc.postToChat('You found the geocache, well done!')

def GC003():
    # Turn lava into stone using water
    mc.postToChat('Watch out! VOLCANOOOOOOOOOOOO !!!')
    mc.setBlocks(51, 0, -3, 55, 8, 3, lava)
    mc.setBlocks(49, 0, -5, 57, 6, 5, lava)
    mc.setBlocks(47, 0, -7, 59, 4, 7, lava)
    sleep(15)
    mc.setBlocks(51, 0, -3, 55, 8, 3, water)
    mc.postToChat('The next geocache is a T5 (You might get wet...)')
    mc.setBlock(52, 0, 2, chest, 1)
    check_block_hit(52, 0, 2)  # Turn chest into books if player hits it
    mc.setBlock(52, 0, 2, books)
    mc.postToChat('Wooohooow!! You found your first T5 cache! :D')
    sleep(3)
    mc.postToChat('There is a hint in the logbook for the next cache: LUCIFER')

def GC004():
    mc.setBlocks(70, 1, 0, 77, 8, 7, tnt, 0)
    mc.setBlock(74, 9, 4, stone)
    mc.setBlock(74, 10, 4, torch)
    check_block_hit(74, 10, 4)
    mc.setBlocks(70, 1, 0, 77, 8, 7, chest, 1)
    mc.postToChat('More geocaches yet to come! \n HAPPY GEOCACHING')


start_game()
GC001()
GC002()
GC003()
GC004()