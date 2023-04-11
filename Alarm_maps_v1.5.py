import datetime
import time
import googlemaps
import playsound

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder


class TravelTimeAlarmApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alarm_active = None
        self.optimal_departure_time = None
        self.alarm_date = None
        self.gmaps = None
        self.stop_button = None
        self.calculate_button = None
        self.optimal_departure_time_label = None
        self.travel_time_label = None
        self.alarm_date_input = None
        self.work_start_time_input = None
        self.work_address_input = None
        self.home_address_input = None

    def build(self):

        # Load the .kv file
        Builder.load_file('travel_time_alarm.kv')

        # Create the UI layout
        layout = RelativeLayout()

        # Create the input fields
        home_address_input = TextInput(text='Enter your home address')
        work_address_input = TextInput(text='Enter your work address')
        work_start_time_input = TextInput(
            text='Enter your work start time (in format HH:MM AM/PM)')
        alarm_date_input = TextInput(
            text='Enter the date for the next alarm (in format MM/DD/YYYY)')

        # Create the labels
        travel_time_label = Label(text='Estimated travel time:', font_size=20)
        optimal_departure_time_label = Label(
            text='Optimal departure time:', font_size=20)

        # Create the buttons
        calculate_button = Button(
            text='Calculate travel time', on_press=self.calculate_travel_time)
        stop_button = Button(
            text='Stop alarm', on_press=self.stop_alarm, disabled=True)

        # Add the UI elements to the layout
        layout.add_widget(home_address_input)
        layout.add_widget(work_address_input)
        layout.add_widget(work_start_time_input)
        layout.add_widget(alarm_date_input)
        layout.add_widget(travel_time_label)
        layout.add_widget(optimal_departure_time_label)
        layout.add_widget(calculate_button)
        layout.add_widget(stop_button)

        # Store the UI elements as instance variables
        self.home_address_input = home_address_input
        self.work_address_input = work_address_input
        self.work_start_time_input = work_start_time_input
        self.alarm_date_input = alarm_date_input
        self.travel_time_label = travel_time_label
        self.optimal_departure_time_label = optimal_departure_time_label
        self.calculate_button = calculate_button
        self.stop_button = stop_button

        # Initialize the Google Maps API client
        self.gmaps = googlemaps.Client(
            key='AIzaSyCWi9R7YKOipcPHmr0xVvcxzbJ76vJpmcI')

        # Initialize the alarm variables
        self.alarm_date = None
        self.optimal_departure_time = None
        self.alarm_active = False

        return layout

    def calculate_travel_time(self, arg):
        # Get the user's input
        home_address = self.home_address_input.text
        work_address = self.work_address_input.text
        work_start_time_str = self.work_start_time_input.text
        alarm_date_str = self.alarm_date_input.text

        # Parse the user's input
        work_start_time = datetime.datetime.strptime(
            work_start_time_str, "%I:%M %p").time()
        self.alarm_date = datetime.datetime.strptime(
            alarm_date_str,"%m/%d/%Y").date()
        
        # Get the current time
        now = datetime.datetime.now()

        # Calculate the time until the alarm
        time_until_alarm = datetime.datetime.combine(
            self.alarm_date, work_start_time) - now

        # Calculate the optimal departure time
        self.optimal_departure_time = datetime.datetime.now() + time_until_alarm - datetime.timedelta(minutes=30)

        # Get the travel time from Google Maps API
        directions_result = self.gmaps.directions(home_address, work_address, departure_time=self.optimal_departure_time)
        travel_time = directions_result[0]['legs'][0]['duration']['text']

        # Update the UI labels
        self.travel_time_label.text = f'Estimated travel time: {travel_time}'
        self.optimal_departure_time_label.text = f'Optimal departure time: {self.optimal_departure_time.strftime("%I:%M %p")}'

        # Enable the stop button and disable the calculate button
        self.stop_button.disabled = False
        self.calculate_button.disabled = True

        # Start the alarm
        self.start_alarm()

    def start_alarm(self):
        while self.alarm_active:
            now = datetime.datetime.now()
            if now >= self.optimal_departure_time:
                # Play the alarm sound
                playsound.playsound('alarm_sound.mp3')

    def stop_alarm(self, arg):
        # Stop the alarm and disable the stop button
        self.alarm_active = False
        self.stop_button.disabled = True

        # Enable the calculate button
        self.calculate_button.disabled = False

        
if __name__ == '__main__':
    TravelTimeAlarmApp().run()