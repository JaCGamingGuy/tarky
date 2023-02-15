import pymem
import pymem.process
import re

ENEMY_COLOR = (255, 0, 0)
ENEMY_HEALTH_COLOR = (255, 255, 255)
FONT = "Arial"
FONT_SIZE = 16

def prompt_value(prompt_text, default_value=None, regex=None):
    while True:
        value = input(f"{prompt_text} [{default_value}]: ") or default_value
        if regex and not re.match(regex, value):
            print("Invalid input, please try again.")
        else:
            return value

def prompt_hex(prompt_text, default_value=None):
    return prompt_value(prompt_text, default_value, regex=r"^[0-9a-fA-F]+$")

process_name = prompt_value("Process name")
player_base = int(prompt_hex("Player base address"), 16)
health_offset = int(prompt_hex("Health offset"), 16)
name_offset = int(prompt_hex("Name offset"), 16)

while True:
    try:
        pm = pymem.Pymem(process_name)
        base_address = pymem.process.module_from_name(pm.process_handle, process_name).lpBaseOfDll

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

    except pymem.exception.ProcessNotFound:
        print(f"Process {process_name} not found. Please start the game and try again.")
        process_name = prompt_value("Process name")
    except Exception as e:
        print(f"An error occurred: {e}")
