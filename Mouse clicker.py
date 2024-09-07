import time, pyautogui, threading, keyboard, os, tkinter as tk
from pynput.mouse import Listener, Button, Controller

class MouseClicker:

    def __init__(self):
        self.twice_mouse = 2
        self.mouse_speed = None
        self.running_status = False
        self.recorded_positions = []
        self.is_recording = False
        self.mouse_listener = None
        self.auto_click_event = threading.Event()

    def on_click(self, x, y, button, pressed):
        if self.is_recording:
            if pressed:
                click_type = "0" if button == Button.left else "1"
                self.recorded_positions.append((x, y, click_type))

    def start_recording(self):
        self.start_button["bg"] = "Lavender"
        self.is_recording = True

    def stop_recording(self):
        self.start_button["bg"] = "GhostWhite"
        self.is_recording = False
        if self.recorded_positions:
            self.recorded_positions.pop()

    def mouse_speed_change(self, value):
        self.mouse_speed = round(float(value), 2)

    def auto_click(self):
        time.sleep(3)
        while not self.auto_click_event.is_set():
            for i in range(1, 2):
                pyautogui.click()
                time.sleep(self.mouse_speed)

    def stop_auto_click(self):
        self.run_button.config(text="连击")
        self.run_button.config(command=(self.run_auto_click))
        self.auto_click_event.set()

    def run_auto_click(self):
        self.auto_click_event.clear()
        threading.Thread(target=(self.auto_click)).start()
        self.run_button.config(text="stop")
        self.run_button.config(command=(self.stop_auto_click))

    def mouse_twice_change(self, values):
        self.twice_mouse = int(values)
        if self.twice_mouse < 0:
            self.run_button.config(text="连击")
            self.run_button.config(command=(self.run_auto_click))
        else:
            if self.twice_mouse >= 0:
                self.auto_click_event.set()
                self.run_button.config(text="run")
                self.run_button.config(command=(self.run_button_click))

    def run_button_click(self):
        if self.start_button["bg"] == "GhostWhite":
            self.running_status = True
        else:
            self.stop_recording()
            self.window.update()
            self.running_status = True
        time.sleep(0.5)
        remaining_clicks = int(self.twice_mouse)
        if remaining_clicks > 0:
            for i in range(1, int(self.twice_mouse) + 1):
                for positions in self.recorded_positions:
                    if self.running_status:
                        x, y, m = positions
                        pyautogui.moveTo(int(x), int(y))
                        time.sleep(self.mouse_speed)
                        if m == "0":
                            pyautogui.click()
                        if m == "1":
                            pyautogui.rightClick()
                    else:
                        return False

                remaining_clicks -= 1
                self.number_scale.set(remaining_clicks)
                self.window.update()

        time.sleep(1)
        self.number_scale.set(2)
        if remaining_clicks == 0:
            if self.shutdown_selected_value.get() == 1:
                os.system("taskkill /f /im *")
                os.system("shutdown /s /t 1")

    def on_closing(self):
        if self.mouse_listener:
            self.mouse_listener.stop()
        self.auto_click_event.set()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        os._exit(0)
        self.window.destroy()

    def clear_positions(self):
        self.number_scale.set(2)
        self.recorded_positions = []

    def on_ctrl_c(self):
        self.running_status = False
        self.auto_click_event.set()
        if self.run_button["text"] == "stop":
            self.run_button.config(text="连击")

    def passss(self):
        pass

    def create_gui(self):
        self.window = tk.Tk()
        self.window.title("鼠标点击器")
        self.window.attributes("-toolwindow", True)
        self.window.resizable(False, False)
        self.window.geometry("243x83")
        self.window.attributes("-topmost", 1)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.start_button = tk.Button((self.window), text="开录", bg="GhostWhite",
          command=(self.start_recording),
          width=5)
        self.start_button.place(x=5, y=3)
        self.stop_button = tk.Button((self.window), text="停录", bg="GhostWhite",
          command=(self.stop_recording),
          width=5)
        self.stop_button.place(x=65, y=3)
        clear_button = tk.Button((self.window), text="清理", bg="GhostWhite", command=(self.clear_positions),
          width=5)
        clear_button.place(x=124, y=3)
        self.shutdown_button = tk.Button((self.window), text="pass", bg="GhostWhite", width=5,
          command=(self.passss))
        self.shutdown_button.place(x=183, y=3)
        self.mouse_scale = tk.Scale((self.window), from_=0, to=5, resolution=0.01, orient=(tk.HORIZONTAL),
          width=15,
          length=50,
          command=(self.mouse_speed_change))
        self.mouse_scale.set(0.2)
        self.mouse_scale.place(x=0, y=38)
        self.number_scale = tk.Scale((self.window), from_=(-1), to=10000, resolution=1,
          orient=(tk.HORIZONTAL),
          width=15,
          length=100,
          command=(self.mouse_twice_change))
        self.number_scale.set(2)
        self.number_scale.place(x=45, y=38)
        self.run_button = tk.Button((self.window), text="Run", command=(self.run_button_click),
          width=3)
        self.run_button.place(x=150, y=46)
        self.shutdown_selected_value = tk.IntVar(self.window)
        self.shutdown_selected_value.set(0)
        self.check_shutdown = tk.Checkbutton((self.window), text="关机", variable=(self.shutdown_selected_value), onvalue=1, offvalue=0)
        self.check_shutdown.place(x=187, y=50)
        self.window.mainloop()

    def start(self):
        keyboard.add_hotkey("ctrl+c", self.on_ctrl_c)
        self.mouse_listener = Listener(on_click=(self.on_click))
        self.mouse_listener.start()
        self.create_gui()


if __name__ == "__main__":
    clicker = MouseClicker()
    clicker.start()
