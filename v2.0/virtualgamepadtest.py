import vgamepad as vg

gamepad = vg.VX360Gamepad()
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
while(True):
    gamepad.reset()
    gamepad.right_trigger(value=100)
    gamepad.update()
    gamepad.right_trigger(value=200)
    gamepad.update()
    gamepad.reset()