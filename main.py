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
import numpy as np
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
    position_status = ""
    restart_status = ""
    save_status = ""

    def restart(self):
        self.results = defaultdict(list)
        self.restart_status = "Restarted in {}\n".format(self.get_time())
        try:
            accelerometer.enable()
            Clock.schedule_interval(self.update, 1.0 / 10)
        except:
            self.display.text = "Failed to start accelerometer\n"

    def update(self, dt):
        self.position_status = \
            'Telephone is in ' \
            '{}\n'.format('static' if self.check_static() else 'hand')
        try:
            x, y, z = accelerometer.acceleration[0], \
                      accelerometer.acceleration[1], \
                      accelerometer.acceleration[2]
            self.results['X'].append(x)
            self.results['Y'].append(y)
            self.results['Z'].append(z)
            self.results['time'].append(self.get_time())
            text = "Accelerometer:\n" \
                   "X = %.2f\n" \
                   "Y = %.2f\n" \
                   "Z = %.2f\n" % (x, y, z)
        except:
            text = "Cannot read accelerometer!\n"
        self.display.text = self.position_status + "\n" + \
                            text + "\n" + \
                            self.restart_status + \
                            self.save_status

    def save(self):
        if self.restart_status != "":
            self.save_status = "Saved in {}\n".format(self.get_time())
            download_dir_path = ""
            if platform == "android":
                from android.storage import primary_external_storage_path
                dir = primary_external_storage_path()
                download_dir_path = os.path.join(dir, "Download")
            data_dir = os.path.join(download_dir_path, "data")
            if not os.path.exists(data_dir):
                os.mkdir(data_dir)
            file_name = "{}.json".format(self.get_time())
            file_path = os.path.join(data_dir, file_name)
            with open(file_path, "w") as outfile:
                json.dump(self.results, outfile)

    @staticmethod
    def get_time():
        return datetime.now().strftime("%H-%M-%S")

    def check_one_static(self, axis):
        Q1 = np.percentile(self.results[axis], 25)
        Q3 = np.percentile(self.results[axis], 75)
        return abs(Q1 - Q3) <= 0.05

    def check_static(self):
        if len(self.results) == 0:
            return True
        answer = True
        for axis in ['X', 'Y', 'Z']:
            answer = answer and self.check_one_static(axis)
        return answer


class MainApp(App):

    def build(self):
        return Container()


if __name__ == "__main__":
    app = MainApp()
    app.run()
    accelerometer.disable()
