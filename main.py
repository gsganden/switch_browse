import pygame
from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button as MouseButton
import time

# Initialize pygame for joystick handling
pygame.init()
pygame.joystick.init()

# Initialize controllers
keyboard = Controller()
mouse = MouseController()

# Button mapping for up/down (you may need to adjust these numbers)
BUTTON_MAPPING = {
    0: "J",  # A
    1: "E",  # B
    # 2: "J", # X
    # 3: "A", # Y
    11: Key.up,  # Up button
    12: Key.down,  # Down button
    13: Key.page_up,  # Right button
    14: Key.page_down,  # Left button
}


def get_joystick():
    """Detect and return the first connected joystick."""
    if pygame.joystick.get_count() == 0:
        print("No gamepad detected.")
        return None
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected to {joystick.get_name()}")
    return joystick


def main():
    joystick = get_joystick()
    if not joystick:
        return

    pressed_keys = set()  # Track pressed keys to avoid spamming
    pressed_mouse_buttons = set()  # Track pressed mouse buttons
    SCROLL_SPEED = 2  # Adjust this value to change scroll sensitivity
    MOUSE_SPEED = 12  # Reduced by 40% from 20 to make movement slower
    DEADZONE = 0.15  # Ignore small movements

    try:
        while True:
            pygame.event.pump()

            # Handle buttons
            for button in range(
                joystick.get_numbuttons()
            ):  # Check all possible buttons
                if joystick.get_button(button):
                    print(f"Button {button} pressed")  # Debug print for button presses

            # Handle buttons (original functionality)
            for button, key in BUTTON_MAPPING.items():
                if joystick.get_button(button):
                    if key not in pressed_keys:
                        keyboard.press(key)
                        pressed_keys.add(key)
                else:
                    if key in pressed_keys:
                        keyboard.release(key)
                        pressed_keys.remove(key)

            # Handle mouse button clicks
            # Button 10 for left click, Button 8 for right click
            if joystick.get_button(10):  # "R"
                if MouseButton.left not in pressed_mouse_buttons:
                    mouse.press(MouseButton.left)
                    pressed_mouse_buttons.add(MouseButton.left)
            else:
                if MouseButton.left in pressed_mouse_buttons:
                    mouse.release(MouseButton.left)
                    pressed_mouse_buttons.remove(MouseButton.left)
                    
            if joystick.get_button(8):  # Right stick click
                if MouseButton.right not in pressed_mouse_buttons:
                    mouse.press(MouseButton.right)
                    pressed_mouse_buttons.add(MouseButton.right)
            else:
                if MouseButton.right in pressed_mouse_buttons:
                    mouse.release(MouseButton.right)
                    pressed_mouse_buttons.remove(MouseButton.right)

            # Handle left stick scrolling
            y_axis = -joystick.get_axis(
                1
            )  # Left stick Y-axis (negated to reverse direction)
            if abs(y_axis) > DEADZONE:
                # Subtract deadzone to make movement smoother
                adjusted_y = y_axis - (DEADZONE if y_axis > 0 else -DEADZONE)
                scroll_amount = int(adjusted_y * SCROLL_SPEED)
                mouse.scroll(0, scroll_amount)
                
            # Handle right stick mouse movement
            # Right stick is typically axes 2 (X) and 3 (Y)
            x_axis = joystick.get_axis(2)  # Right stick X-axis
            y_axis = joystick.get_axis(3)  # Right stick Y-axis
            
            if abs(x_axis) > DEADZONE or abs(y_axis) > DEADZONE:
                # Apply deadzone and calculate movement
                adjusted_x = 0
                adjusted_y = 0
                
                if abs(x_axis) > DEADZONE:
                    adjusted_x = x_axis - (DEADZONE if x_axis > 0 else -DEADZONE)
                
                if abs(y_axis) > DEADZONE:
                    adjusted_y = y_axis - (DEADZONE if y_axis > 0 else -DEADZONE)
                
                # Get current mouse position
                current_pos = mouse.position
                
                # Calculate new position
                new_x = current_pos[0] + int(adjusted_x * MOUSE_SPEED)
                new_y = current_pos[1] + int(adjusted_y * MOUSE_SPEED)
                
                # Move mouse to new position
                mouse.position = (new_x, new_y)

            time.sleep(0.01)  # Prevents high CPU usage

    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
