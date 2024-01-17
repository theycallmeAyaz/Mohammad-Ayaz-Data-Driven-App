import tkinter as tk
import requests
import urllib.request
from PIL import Image, ImageTk
import io
#Return the height of the application.
def App_height() -> int:
    return 600

#Return the width of the application.
def App_width() -> int:
    return 800

#Return the height of the Pokemon image.
def Height_images() -> int:
    return 250

#Return the width of the Pokemon image.
def Width_images() -> int:
    return 250

#Return the hex color of the application's frames.
def FrameBorder_color() -> str:
    return "#0E2948"

#Return the hex color of the search button.
def Search_ButtonColor() -> str:
    return "#006EE6"

#Return the font family and size of the application.
def Font_family() -> str:
    return "Helvetica 11"

#Fill the application with data.
def Fill_dex(name: str):
    url = "https://pokeapi.co/api/v2/pokemon/" + name
    res = requests.get(url)
    if not res:
        ClearPoki_results()
    else:
        pokemon = res.json()
        Dex_Data(pokemon)
        DisplayImage(pokemon)
        try:
            GetPoki_info(name)
        except KeyError:
            smogon_info["text"] = "GEN 8 COMPETITIVE SMOGON OU SETS\n\nThis Pokémon is not part of the Gen 8 OU tier."

#Get Pokedex data and fill dex info label.
def Dex_Data(pokemon: dict):
    name = pokemon["forms"][0]["name"].capitalize()
    pokemon_id = pokemon["id"]
    types = Poki_Type(pokemon)
    abilities = Poki_Abillity(pokemon)
    stats = Poki_Stats(pokemon)
    formatted_str = "\nName: %s \n\nDex Number: %s\n\nType(s): %s \n\nAbilities: %s \n\nBase Stats:\n %s" % \
                    (name, pokemon_id, types, abilities, stats)
    dex_info["text"] = formatted_str

#Get image and sprite data and fill image and sprite labels.
def DisplayImage(pokemon: dict):
    try:
        Get_image(pokemon["sprites"]["other"]["official-artwork"]["front_default"])
    except AttributeError:
        dex_img.configure(image=None)
        dex_img.image = None
    try:
        GetSprite_Pixel(pokemon["sprites"]["front_default"], "front")
    except AttributeError:
        sprite_front_img.configure(image=None)
        sprite_front_img.image = None
    try:
        GetSprite_Pixel(pokemon["sprites"]["back_default"], "back")
    except AttributeError:
        sprite_back_img.configure(image=None)
        sprite_back_img.image = None

#Get the Pokemon's abilities from PokeAPI.
def Poki_Abillity(pokemon: dict) -> str:
    abilities_list = []
    for i in range(len(pokemon["abilities"])):
        abilities_list.extend([pokemon["abilities"][i]["ability"]["name"].capitalize(), ", "])
    return ''.join(abilities_list)[:-2]

#Get the Pokemon's base stats from PokeAPI.
def Poki_Stats(pokemon: dict) -> str:
    base_stat_list = []
    for i in range(len(pokemon["stats"])):
        base_stat_list.extend([pokemon["stats"][i]["stat"]["name"].capitalize() + " : " +
                               str(pokemon["stats"][i]["base_stat"]), '\n'])
    return ''.join(base_stat_list)

#Get the Pokemon's types from PokeAPI.
def Poki_Type(pokemon: dict) -> str:
    types_list = []
    for i in range(len(pokemon["types"])):
        types_list.extend([pokemon["types"][i]["type"]["name"].capitalize(), ", "])
    return ''.join(types_list)[:-2]

def Get_image(url: str):
    try:
        with urllib.request.urlopen(url) as data:
            image_data = data.read()
            
        raw_image = Image.open(io.BytesIO(image_data))
        resize_image = raw_image.resize((Height_images(), Width_images()), Image.LANCZOS)
        image = ImageTk.PhotoImage(resize_image)
        dex_img.configure(image=image)
        dex_img.image = image
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        dex_img.configure(image=None)
        dex_img.image = None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        dex_img.configure(image=None)
        dex_img.image = None

#Get the Pokemon's sprites from PokeAPI and display it in the sprites frames.
def GetSprite_Pixel(url: str, face: str):
    with urllib.request.urlopen(url) as data:
        image_data = data.read()
    raw_image = Image.open(io.BytesIO(image_data))
    image = ImageTk.PhotoImage(raw_image)
    if face == "front":
        sprite_front_img.configure(image=image)
        sprite_front_img.image = image
    if face == "back":
        sprite_back_img.configure(image=image)
        sprite_back_img.image = image

#Get the Pokemon's competitive data from smogun and display it in the frames
#(Poke API DOESNT HAVE COMPETITIVE DATA OF POKEMON GEN 3 till Gen 8 therefore needed external api).
#the following api (https://smogon-usage-stats.herokuapp.com/gen8ou/) had expired/stopped working recently but this feature will work in future as intended
def GetPoki_info(name: str):
    url = "https://smogon-usage-stats.herokuapp.com/gen8ou/" + name
    try:
        res = requests.get(url)
        # Raise exception if status is not OK
        res.raise_for_status()  
    except (requests.HTTPError, requests.ConnectionError):
        smogon_info["text"] = "ALL-TIME GEN COMPETITIVE SMOGON OU SETS\n\nThis Pokémon has no competitive data."
    else:
        try:
            pokemon = res.json()
            smogon_info["text"] = "ANY GEN COMPETITIVE SMOGON OU SETS\n\n" + GetPoki_response(pokemon)
        except ValueError:
            smogon_info["text"] = "ANY COMPETITIVE SMOGON OU SETS\n\nUnable to fetch competitive data."

#Get Smogon data and return a formatted string.
def GetPoki_response(pokemon: dict) -> str:
    try:
        sm_ability = list(pokemon["abilities"].keys())[0]
        sm_moves = ", ".join(list(pokemon["moves"].keys())[0:4])
        sm_item = list(pokemon["items"].keys())[0]
        sm_ev = GetPoki_EV(pokemon)
        if len(sm_ability) and len(sm_moves) and len(sm_item) and len(sm_ev) > 0:
            return "Ability: %s \nMoveset: %s \nItem: %s \nSpread: %s" \
                        % (sm_ability, sm_moves, sm_item, sm_ev)
        else:
            return "Incomplete competitive information for this Pokémon."
    except IndexError:
        return "Incomplete competitive information for this Pokémon."

#Get recommended nature + EV spread from Smogon Usage Stats API.
def GetPoki_EV(pokemon: dict) -> str:
    try:
        nature = list(pokemon["spreads"].keys())[0]
        ev = list(pokemon["spreads"][nature].keys())[0]
        return nature.capitalize() + ", " + ev
    except IndexError:
        return "Incomplete spread information for this Pokémon."

#Clear application of all data if no valid response is received.
#Preconditions required=none
def ClearPoki_results():
    dex_info["text"] = "Info on this Pokémon does not exist."
    smogon_info["text"] = ""
    sprite_front_img.configure(image=None)
    sprite_front_img.image = None
    sprite_back_img.configure(image=None)
    sprite_back_img.image = None
    dex_img.configure(image=None)
    dex_img.image = None

# TKinter Application
root = tk.Tk()

# Prevent window from being resized
root.resizable(False, False)

# Application title and icon
root.title("Python Pokedex By Mohammad Ayaz")
root.iconbitmap('pkdex_icon.ico')


# Application dimensions
canvas = tk.Canvas(root, height=App_height(), width=App_width())
canvas.pack()

# Application background
background_image = tk.PhotoImage(file='bgimage.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relheight=1, relwidth=1)

# Frame for search bar
SearchFrame = tk.Frame(root,bg="#FF2759")
SearchFrame.place(relx=0.05, rely=0.025, relwidth=0.9, relheight=0.08)

# Search bar
search = tk.Entry(SearchFrame, font=20)
search.place(relx=0.017, rely=0.1, relwidth=0.75, relheight=0.8)

# Search button
SearchButton = tk.Button(SearchFrame, text="Search", bg=Search_ButtonColor(), fg="white",
                          command=lambda: Fill_dex(search.get().lower()))
SearchButton.place(relx=0.78, rely=0.1, relwidth=0.2, relheight=0.8)

# Frame for the pokedex info and official art
Frame1_Info = tk.Frame(root, bg=FrameBorder_color())
Frame1_Info.place(relx=0.05, rely=0.125, relwidth=0.9, relheight=0.505)

# Pokedex info display
dex_info = tk.Label(Frame1_Info, text="Instructions:\nTo Search for a Pokémon,\n Enter the Pokémon's Name\n or Dex Number!\n \nType the name in format:\n Example:Scizor-Mega", font=Font_family())
dex_info.place(relx=0.38, rely=0.025, relwidth=0.6, relheight=0.95)

# Pokedex image display
dex_img = tk.Label(Frame1_Info)
dex_img.place(relx=0.017, rely=0.025, relwidth=0.346, relheight=0.95)

# Frame for Smogon data and game sprites
info_frame_2 = tk.Frame(root, bg=FrameBorder_color())
info_frame_2.place(relx=0.05, rely=0.65, relwidth=0.9, relheight=0.32)

# Game sprite display (front and back) - note, there are some issues with S/S exclusive sprites such as bg color
sprite_front_img = tk.Label(info_frame_2, bg="black")
sprite_front_img.place(relx=0.017, rely=0.025, relwidth=0.17, relheight=0.95)
sprite_back_img = tk.Label(info_frame_2, bg="black", fg="white")
sprite_back_img.place(relx=0.195, rely=0.025, relwidth=0.17, relheight=0.95)

# Smogon Gen 8 OU display
smogon_info = tk.Label(info_frame_2, font=Font_family())
smogon_info.place(relx=0.38, rely=0.025, relwidth=0.6, relheight=0.95)

root.mainloop()
