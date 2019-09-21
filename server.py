import eel
import myDes

eel.init('web')
my_options = {
    'mode': "chrome-app",  # or "chrome",
    'host': 'localhost',
    'port': 8080,
    # 'chromeFlags': ["--start-fullscreen", "--browser-startup-dialog"]
    'chromeFlags': ["--start-fullscreen"]
}

eel.start('main.html', options=my_options)
