import pymem
import pymem.process

PROCESS_NAME = "EscapeFromTarkov.exe"
ENEMY_COLOR = (255, 0, 0)
ENEMY_HEALTH_COLOR = (255, 255, 255)
FONT = "Arial"
FONT_SIZE = 16

pm = pymem.Pymem(PROCESS_NAME)
base_address = pymem.process.module_from_name(pm.process_handle, PROCESS_NAME).lpBaseOfDll

player_base = base_address + 0x123456 #replace this with the player base address
health_offset = 0x12 #replace this with the health offset
name_offset = 0x34 #replace this with the name offset

while True:
    player_list = []
    for i in range(10): #change this to the number of players you want to display
        player_address = player_base + i*0x100 #replace 0x100 with the player offset
        health = pm.read_int(player_address + health_offset)
        name = pm.read_string(player_address + name_offset)
        if health > 0 and name != "":
            player_list.append((name, health, player_address))
    
    for player in player_list:
        name, health, address = player
        position = pm.read_vector3(address + 0x20) #replace this with the player position offset
        screen_position = pm.world_to_screen(position)

        if screen_position.z > 0:
            screen_position.x = int(screen_position.x)
            screen_position.y = int(screen_position.y)

            pm.draw_rect(screen_position.x - 50, screen_position.y - 50, 100, 100, ENEMY_COLOR)
            pm.draw_text(screen_position.x, screen_position.y - 60, name, FONT, FONT_SIZE, ENEMY_COLOR)
            pm.draw_text(screen_position.x, screen_position.y - 40, f"Health: {health}%", FONT, FONT_SIZE, ENEMY_HEALTH_COLOR)
