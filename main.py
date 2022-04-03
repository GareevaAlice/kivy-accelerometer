from kivy.app import App
from plyer import accelerometer
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.utils import platform

import os
import json
from datetime import datetime
from collections import defaultdict

kv_path = './kv/'
for kv in os.listdir(kv_path):
    Builder.load_file(kv_path + kv)


class RestartButton(Button):
    pass


class SaveButton(Button):
    pass


class Container(GridLayout):
    display = ObjectProperty()
    results = defaultdict(list)

    def restart(self):
        self.results = defaultdict(list)
        try:
            accelerometer.enable()
            Clock.schedule_interval(self.update, 1)
        except:
            self.display.text = "Failed to start accelerometer"

    def update(self, dt):
        try:
            x, y, z = accelerometer.acceleration[0], \
                      accelerometer.acceleration[1], \
                      accelerometer.acceleration[2]
            self.results['X'].append(x)
            self.results['Y'].append(y)
            self.results['Z'].append(z)
            self.results['time'].append(self.get_time())
            self.display.text = "Accelerometer:\n" \
                                "X = %.2f\n" \
                                "Y = %.2f\n" \
                                "Z = %2.f " % (x, y, z)
        except:
            self.display.text = "Cannot read accelerometer!"

    def save(self):
        download_dir_path = ""
        if platform == "android":
            from android.storage import primary_external_storage_path
            dir = primary_external_storage_path()
            download_dir_path = os.path.join(dir, "Download")
        file_name = "{}.json".format(self.get_time())
        file_path = os.path.join(download_dir_path, file_name)
        with open(file_path, "w") as outfile:
            json.dump(self.results, outfile)

    def get_time(self):
        return datetime.now().strftime("%H-%M-%S")


class MainApp(App):

    def build(self):
        return Container()


if __name__ == "__main__":
    app = MainApp()
    app.run()
