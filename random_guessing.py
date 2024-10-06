import flet as flt
from flet import UserControl, Text, Container, Column, Row, MainAxisAlignment, TextField, colors, FilledButton
import requests
import random

class Poke(UserControl):
    def __init__(self):
        super().__init__()
        self.pokemon_name = ""  # Store the current Pokémon name
        self.score = 0  # Initialize the score

        # Initial Pokémon setup
        self.fetch_initial_pokemon()

        self.img = flt.Image(
            src=self.image_url,
            width=100,
            height=100,
            fit=flt.ImageFit.CONTAIN,
        )

    def fetch_initial_pokemon(self):
        """Fetch a random Pokémon for initial display."""
        pokemon_id = random.randint(1, 1010)
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            pokemon_data = response.json()

            self.pokemon_name = pokemon_data['name']  # Save the Pokémon name
            self.image_url = pokemon_data['sprites']['back_default']
        except requests.exceptions.RequestException as err:
            print(f"Error fetching initial Pokémon: {err}")

    def fetch_pokemon(self, e):
        """Fetch a new Pokémon and display its image."""
        pokemon_id = random.randint(1, 1010)
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            pokemon_data = response.json()

            self.pokemon_name = pokemon_data['name']  # Save the new Pokémon name
            self.image_url = pokemon_data['sprites']['front_default']

            if self.image_url:
                self.img.src = self.image_url
                self.img.update()
                self.correct_answer.value = ""  # Clear the previous answer
                self.correct_answer.update()    # Update the UI
            else:
                print(f"No image found for Pokémon ID: {pokemon_id}")
        except requests.exceptions.RequestException as err:
            print(f"Error fetching data: {err}")
        self.update()

    def check_guess(self, e):
        """Check if the entered name matches the fetched Pokémon."""
        entered_name = self.out_field.value  # Get the value from the text field
        if entered_name.lower() == self.pokemon_name.lower():
            print("Correct! You guessed the Pokémon name.")
            self.score += 1  # Increase score on correct guess
            self.correct_answer.value = "Correct!"  # Show success message
        else:
            print(f"Wrong! The correct name was {self.pokemon_name}.")
            # Display the correct Pokémon name
            self.correct_answer.value = f"Wrong! The correct name was {self.pokemon_name}."

        # Update the score display
        self.result.value = f"Score: {self.score}"
        self.correct_answer.update()
        self.result.update()

    def combined_action(self, e):
        """Check the guess and then fetch a new Pokémon."""
        self.check_guess(e)  # Check the user's guess
        self.fetch_pokemon(e)  # Fetch a new Pokémon after checking

    def build(self):
        self.out_field = TextField(
            label="Enter your guess",
            width=300,
            multiline=False,
            password=False
        )

        self.result = Text(
            value=f"Score: {self.score}",
            color=colors.ORANGE,
            size=22
        )

        self.correct_answer = Text(
            value="",
            color=colors.GREEN if self.score else colors.RED,
            size=18
        )

        combined_button = FilledButton(
            text="Check and Next Pokémon",
            style=flt.ButtonStyle(
                color={
                    flt.ControlState.HOVERED: flt.colors.GREEN,
                    flt.ControlState.FOCUSED: flt.colors.GREEN,
                    flt.ControlState.DEFAULT: flt.colors.GREEN,
                }
            ),
            on_click=self.combined_action  # Call combined function on click
        )

        return Container(
            content=Column(
                controls=[
                    Row(
                        controls=[self.result],  # Display the score here
                        alignment=MainAxisAlignment.END
                    ),
                    self.out_field,  # Input field to enter guess
                    combined_button,  # Button to check the guess and fetch a new Pokémon
                    self.correct_answer,  # Display correct answer only if the guess is wrong
                    self.img  # Display Pokémon image
                ]
            ),
        )

def myapp(page: flt.Page):
    page.theme_mode = flt.ThemeMode.DARK
    page.window_height = 400
    page.window_width = 500
    page.add(Poke())  # Add an instance of `Poke`
    page.update()

flt.app(target=myapp)
3