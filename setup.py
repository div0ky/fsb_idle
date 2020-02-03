from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=["cv2"], excludes=[])

base = 'Console'

executables = [
    Executable('C:\\Users\\ajspurlock\\PycharmProjects\\Firestone\\idle_bot.py', base=base, targetName='Bot')
]

setup(name='Firestone_Bot',
      version='0.1',
      description='Testing',
      options=dict(build_exe=buildOptions),
      executables=executables, requires=['pyautogui'])
