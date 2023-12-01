import pyautogui
import time


def start_server():
    time.sleep(2)
    start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/dreamdrawer/LMstudio_icon.png')
    if start_button is not None:
        pyautogui.click(start_button)
    time.sleep(10)

    start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/dreamdrawer/LMstudio_server_tab.png')
    if start_button is not None:
        pyautogui.click(start_button)

    time.sleep(2)
    # Locate Start Server button
    start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/dreamdrawer/LMstudio_start_server_button.png')
    if start_button is not None:
        pyautogui.click(start_button)

    time.sleep(2)
    # Locate Start Server button
    start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/dreamdrawer/LMstudio_activity_icon.png')
    if start_button is not None:
        pyautogui.click(start_button)

    time.sleep(10)

def stop_server():
    
    # Locate Start Server button
    activity_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/dreamdrawer/LMstudio_activity_icon.png')
    activity_button_light = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/dreamdrawer/LMstudio_activity_icon_light.png')
    if activity_button is not None:
        pyautogui.click(activity_button, button='right')
    elif activity_button is None:
        pyautogui.click(activity_button_light, button='right')

    time.sleep(2)
    # # Locate Start Server button
    # start_button = pyautogui.locateCenterOnScreen('/home/lunkwill/projects/dreamdrawer/LMstudio_x.png')
    # if start_button is not None:
    #     pyautogui.click(start_button)

    pyautogui.press('alt')
    pyautogui.press('c')

#stop_server()