from pywinauto import application
from pywinauto import Desktop
import pywinauto

app = application.Application()

game = app.connect(title="Firestone", found_index=1)

dialog = app.windows()

print(dialog)

pywinauto.handleprops.children(app)


# app.print_control_identifiers()



# app = Application(backend="uia").start('notepad.exe')
#
# # describe the window inside Notepad.exe process
# win = app.UntitledNotepad
# # wait till the window is really open
# actionable_dlg = win.wait('visible')
#
# win.Edit.type_keys("Hello world!", with_spaces=True)
#
# file_menu = win.menu_select("File->Exit")
#
# save_dialog = win.child_window(title="Don't Save", auto_id="CommandButton_7", control_type="Button").click()
#
# # win.print_control_identifiers()
