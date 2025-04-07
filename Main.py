import pygame
import time
import math
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laundry Robot Simulation")
font = pygame.font.SysFont("Arial", 24)

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (50, 100, 200)
GREEN = (0, 200, 100)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

clock = pygame.time.Clock()

# Positions
arm_base = (WIDTH // 2, HEIGHT - 100)
dirty_bin = (150, 450)
washer_pos = (350, 300)
dryer_pos = (650, 300)
clean_bin = (850, 450)

# Timer
start_time = time.time()
last_action_time = start_time

def draw_timer():
    elapsed = int(time.time() - start_time)
    timer_text = font.render(f"Timer: {elapsed}s", True, BLACK)
    screen.blit(timer_text, (20, 20))

def draw_bins():
    for (x, y), label in [(dirty_bin, "Dirty Bin"), (clean_bin, "Clean Bin")]:
        pygame.draw.rect(screen, ORANGE, (x, y, 80, 80))
        for i in range(5):
            pygame.draw.line(screen, BLACK, (x + i * 16, y), (x + i * 16, y + 80))
            pygame.draw.line(screen, BLACK, (x, y + i * 16), (x + 80, y + i * 16))
        label_text = font.render(label, True, BLACK)
        screen.blit(label_text, (x, y - 30))

def draw_machine(pos, label):
    x, y = pos
    pygame.draw.rect(screen, GRAY, (x, y, 120, 120))
    pygame.draw.circle(screen, BLUE, (x + 60, y + 60), 40)
    pygame.draw.rect(screen, BLACK, (x + 100, y + 50, 10, 20))
    label_text = font.render(label, True, BLACK)
    screen.blit(label_text, (x, y - 30))

def draw_arm(target, grip=False):
    # Arm parts
    base_x, base_y = arm_base
    joint_x, joint_y = (base_x, base_y - 100)
    end_x, end_y = target

    pygame.draw.line(screen, BLACK, arm_base, (joint_x, joint_y), 12)
    pygame.draw.line(screen, BLACK, (joint_x, joint_y), (end_x, end_y), 8)

    # Fingers
    if grip:
        pygame.draw.line(screen, RED, (end_x, end_y), (end_x + 10, end_y - 10), 4)
        pygame.draw.line(screen, RED, (end_x, end_y), (end_x - 10, end_y - 10), 4)
    else:
        pygame.draw.line(screen, RED, (end_x, end_y), (end_x + 15, end_y - 20), 4)
        pygame.draw.line(screen, RED, (end_x, end_y), (end_x - 15, end_y - 20), 4)

def move_arm_sequence(path):
    for i, (target_x, target_y, grip) in enumerate(path):
        screen.fill(WHITE)
        draw_bins()
        draw_machine(washer_pos, "Washer")
        draw_machine(dryer_pos, "Dryer")
        draw_timer()
        draw_arm((target_x, target_y), grip)
        pygame.display.update()
        time.sleep(1)  # smooth animation timing

def check_machine_ready(machine_name):
    check_time = time.time()
    wait_duration = 15  # seconds

    print(f"Checking {machine_name}... Please wait.")
    while True:
        current_time = time.time()
        if current_time - check_time >= wait_duration:
            print(f"{machine_name} is ready.")
            return
        else:
            remaining = int(wait_duration - (current_time - check_time))
            print(f"{machine_name} not ready. Rechecking in {remaining}s...")
            time.sleep(remaining)

# Define the motion path for the robot
def run_simulation():
    global last_action_time

    def wait_for_next():
        global last_action_time  # ← Add this line
        while time.time() - last_action_time < 15:
            time.sleep(1)
        last_action_time = time.time()


    # Sequence 1: Dirty Bin → Washer
    wait_for_next()
    move_arm_sequence([
        (dirty_bin[0]+40, dirty_bin[1]-20, False),
        (dirty_bin[0]+40, dirty_bin[1]-20, True),
        (washer_pos[0]+60, washer_pos[1], True),
        (washer_pos[0]+60, washer_pos[1], False),
    ])

    check_machine_ready("Washer")

    # Sequence 2: Washer → Dryer
    wait_for_next()
    move_arm_sequence([
        (washer_pos[0]+60, washer_pos[1], False),
        (washer_pos[0]+60, washer_pos[1], True),
        (dryer_pos[0]+60, dryer_pos[1], True),
        (dryer_pos[0]+60, dryer_pos[1], False),
    ])

    check_machine_ready("Dryer")

    # Sequence 3: Dryer → Clean Bin
    wait_for_next()
    move_arm_sequence([
        (dryer_pos[0]+60, dryer_pos[1], False),
        (dryer_pos[0]+60, dryer_pos[1], True),
        (clean_bin[0]+40, clean_bin[1]-20, True),
        (clean_bin[0]+40, clean_bin[1]-20, False),
    ])

# Main loop
running = True
action_started = False

while running:
    screen.fill(WHITE)
    draw_bins()
    draw_machine(washer_pos, "Washer")
    draw_machine(dryer_pos, "Dryer")
    draw_timer()
    draw_arm((arm_base[0], arm_base[1] - 100), False)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not action_started:
        run_simulation()
        action_started = True

    clock.tick(60)

pygame.quit()
sys.exit()
