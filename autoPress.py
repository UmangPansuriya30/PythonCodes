import pyautogui
import time
while True:
    pyautogui.press('ctrl')
    time.sleep(3)  


# import pyautogui
# import time

# # Time interval (in seconds) between switching tabs
# INTERVAL = 5  # Change this value as you like


# time.sleep(3)  # Delay before starting (so you can prepare)

# try:
#     while True:
#         # Hold down Alt
#         pyautogui.keyDown('alt')
#         # Press Tab once
#         for _ in range(5):  # Switch two windows ahead
#             pyautogui.press('tab')
#         # Release Alt
#         pyautogui.keyUp('alt')

#         time.sleep(INTERVAL)  # Wait before next switch

# except KeyboardInterrupt:
#     print("\nAutomation stopped by user.")
