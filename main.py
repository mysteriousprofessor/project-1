from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

class NumericKeyboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.input_field = TextInput()
        self.add_widget(self.input_field)

        buttons_layout = BoxLayout()
        buttons_layout.orientation = 'vertical'

        # Creating buttons for numeric input
        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'Clear', '0', 'Enter'
        ]

        for i in range(4):
            row_layout = BoxLayout()
            for j in range(3):
                button = Button(text=buttons[i*3 + j], background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
                button.bind(on_press=self.buttonClicked)
                row_layout.add_widget(button)
            buttons_layout.add_widget(row_layout)

        self.add_widget(buttons_layout)

    def buttonClicked(self, instance):
        if instance.text == 'Clear':
            self.input_field.text = ''
        elif instance.text == 'Enter':
            print("Entered text:", self.input_field.text)
        else:
            # Only allow input of digits and limit to 4 characters
            if instance.text.isdigit() and len(self.input_field.text) < 4:
                current_text = self.input_field.text
                if current_text == '0000':
                    self.input_field.text = instance.text
                else:
                    self.input_field.text += instance.text

class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.label = Label(text="Automatically typing:", size_hint=(1, 0.1), color=(0.2, 0.6, 1, 1))
        self.add_widget(self.label)

        self.line_edit = TextInput(readonly=True, size_hint=(1, 0.1), background_color=(0.9, 0.9, 0.9, 1))
        self.add_widget(self.line_edit)

        self.start_button = Button(text="Start", size_hint=(1, 0.1), background_color=(0.2, 0.6, 1, 1), color=(1, 1, 1, 1))
        self.start_button.bind(on_press=self.start_typing)
        self.add_widget(self.start_button)

        # Add NumericKeyboard widget directly to the layout
        self.numeric_keyboard = NumericKeyboard(size_hint=(1, 0.7))
        self.add_widget(self.numeric_keyboard)

        self.counter = 0
        self.typing_started = False

    def update_number(self, dt):
        if self.typing_started:
            self.line_edit.text = '{:04d}'.format(self.counter)
            self.counter += 1
            if self.counter > 9999:
                self.counter = 0

    def start_typing(self, instance):
        if not self.typing_started:
            Clock.schedule_interval(self.update_number, 0.1)  # Update every 100 milliseconds
            self.typing_started = True

    def stop_typing(self):
        if self.typing_started:
            Clock.unschedule(self.update_number)
            self.typing_started = False

class MyApp(App):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    MyApp().run()