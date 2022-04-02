from kivy.app import App
from plyer import accelerometer
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.utils import platform

from datetime import datetime
import os

kv_path = './kv/'
for kv in os.listdir(kv_path):
    Builder.load_file(kv_path + kv)


class RestartButton(Button):
    pass


class SaveButton(Button):
    pass


class Container(GridLayout):
    display = ObjectProperty()
    results = dict()

    def restart(self):
        self.results = dict()
        try:
            accelerometer.enable()
            Clock.schedule_interval(self.update, 1)
        except:
            self.display.text = "Failed to start accelerometer"

    def update(self, dt):
        try:
            result = dict()
            result['x'] = accelerometer.acceleration[0]
            result['y'] = accelerometer.acceleration[0]
            result['z'] = accelerometer.acceleration[0]
            self.results[self.get_time()] = result
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
            outfile.write(str(self.results))

    def get_time(self):
        return datetime.now().strftime("%H:%M:%S")


class MainApp(App):

    def build(self):
        return Container()


if __name__ == "__main__":
    app = MainApp()
    app.run()
