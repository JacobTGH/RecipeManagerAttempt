import os
from tkinter import *
from tkinter import simpledialog

# Get the current working directory
current_directory = os.getcwd()

# Create the "recipe folder" in the current working directory
recipe_folder_path = os.path.join(current_directory, "recipe folder")
if not os.path.exists(recipe_folder_path):
    os.mkdir(recipe_folder_path)

class Recipe:
    def __init__(self, title, ingredients, instructions, cooking_time, dietary_info):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions
        self.cooking_time = cooking_time
        self.dietary_info = dietary_info
    
    # Getter methods
    def get_title(self):
        return self.title
    
    def get_ingredients(self):
        return ", ".join(self.ingredients)
    
    def get_instructions(self):
        return self.instructions
    
    def get_cooking_time(self):
        return self.cooking_time
    
    def get_dietary_info(self):
        return self.dietary_info
    
    # Setter methods
    def set_title(self, title):
        self.title = title
    
    def set_ingredients(self, ingredients):
        self.ingredients = ingredients
    
    def set_instructions(self, instructions):
        self.instructions = instructions
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
    
    def set_dietary_info(self, dietary_info):
        self.dietary_info = dietary_info


class RecipeManager:
    def __init__(self):
        self.recipes = []
    
    def add_recipe(self, recipe):
        self.recipes.append(recipe)
        self.save_recipes()
    
    def update_recipe(self, recipe_index, new_recipe):
        if recipe_index >= 0 and recipe_index < len(self.recipes): # Error handling for if selected index is not in list
            self.recipes[recipe_index] = new_recipe
        self.save_recipes()
    
    def delete_recipe(self, recipe_index):
        if recipe_index >= 0 and recipe_index < len(self.recipes):
            filename = os.path.join(recipe_folder_path, f"{self.recipes[recipe_index].get_title()}.txt")
            if os.path.exists(filename):
                os.remove(filename)
            del self.recipes[recipe_index]
    
    def get_recipe(self, recipe_index):
        if recipe_index >= 0 and recipe_index < len(self.recipes):
            return self.recipes[recipe_index]
        else:
            return None
    
    def get_all_recipes(self):
        return self.recipes
    
    def save_recipes(self):  # Would use index to save the individual file, but due to it being text files this is fine for now as it won't use too much memory anyway
        for recipe in self.recipes:
            filename = os.path.join(recipe_folder_path, f"{recipe.get_title()}.txt")
            with open(filename, 'w') as file:
                file.write(f"{recipe.get_title()}\n")
                file.write(f"{recipe.get_ingredients()}\n")
                file.write(f"{recipe.get_instructions()}\n")
                file.write(f"{recipe.get_cooking_time()}\n")
                file.write(f"{recipe.get_dietary_info()}\n")
    
    def load_recipes(self):
        self.recipes = []
        if not os.path.exists(recipe_folder_path):
            return

        for file in os.listdir(recipe_folder_path):
            if file.endswith('.txt'):
                with open(os.path.join(recipe_folder_path, file), 'r') as recipe_file:
                    lines = recipe_file.readlines()
                    if len(lines) == 5:
                        title = lines[0].strip()
                        ingredients = [ingredient.strip() for ingredient in lines[1].split(",")]
                        instructions = lines[2].strip()
                        cooking_time = int(lines[3].strip())
                        dietary_info = lines[4].strip()
                        recipe = Recipe(title, ingredients, instructions, cooking_time, dietary_info)
                        self.add_recipe(recipe)


# RECIPE UI (in our main branch)

class RecipeManagementApp:
    def __init__(self, manager):
        self.manager = manager
        
        self.window = Tk()
        self.window.title("Recipe Management System")
        
        self.recipe_listbox = Listbox(self.window, width=50)
        self.recipe_listbox.pack(side=LEFT, fill=Y)
        self.recipe_listbox.bind('<<ListboxSelect>>', self.show_recipe_details)
        
        self.recipe_details_label = Label(self.window, text="Recipe Details", font=("Arial", 14, "bold"))
        self.recipe_details_label.pack()
        
        self.title_label = Label(self.window, text="Title:")
        self.title_label.pack()
        
        self.ingredients_label = Label(self.window, text="Ingredients:")
        self.ingredients_label.pack()
        
        self.instructions_label = Label(self.window, text="Instructions:")
        self.instructions_label.pack()
        
        self.cooking_time_label = Label(self.window, text="Cooking Time:")
        self.cooking_time_label.pack()
        
        self.dietary_info_label = Label(self.window, text="Dietary Information:")
        self.dietary_info_label.pack()
        
        self.add_button = Button(self.window, text="Add Recipe", command=self.add_recipe)
        self.add_button.pack()
        
        self.update_button = Button(self.window, text="Update Recipe", command=self.update_recipe)
        self.update_button.pack()
        
        self.delete_button = Button(self.window, text="Delete Recipe", command=self.delete_recipe)
        self.delete_button.pack()
        
        self.load_recipes()
    
    def show_recipe_details(self, event):
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            recipe = self.manager.get_recipe(selected_index[0])
            if recipe:
                self.title_label.config(text=f"Title: {recipe.get_title()}")
                self.ingredients_label.config(text=f"Ingredients: {recipe.get_ingredients()}")
                self.instructions_label.config(text=f"Instructions: {recipe.get_instructions()}")
                self.cooking_time_label.config(text=f"Cooking Time: {recipe.get_cooking_time()} minutes")
                self.dietary_info_label.config(text=f"Dietary Information: {recipe.get_dietary_info()}")
    
    def add_recipe(self):
        title = simpledialog.askstring("Add Recipe", "Enter the title:")
        ingredients = simpledialog.askstring("Add Recipe", "Enter the ingredients (comma-separated):")
        instructions = simpledialog.askstring("Add Recipe", "Enter the instructions:")
        cooking_time = simpledialog.askinteger("Add Recipe", "Enter the cooking time (in minutes):")
        dietary_info = simpledialog.askstring("Add Recipe", "Enter the dietary information:")
        
        recipe = Recipe(title, [ingredient.strip() for ingredient in ingredients.split(",")], instructions, cooking_time, dietary_info)
        self.manager.add_recipe(recipe)
        self.refresh_recipe_list()
    
    def update_recipe(self):
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            recipe = self.manager.get_recipe(selected_index[0])
            if recipe:
                title = simpledialog.askstring("Update Recipe", "Enter the title:", initialvalue=recipe.get_title())
                ingredients = simpledialog.askstring("Update Recipe", "Enter the ingredients (comma-separated):", initialvalue=recipe.get_ingredients())
                instructions = simpledialog.askstring("Update Recipe", "Enter the instructions:", initialvalue=recipe.get_instructions())
                cooking_time = simpledialog.askinteger("Update Recipe", "Enter the cooking time (in minutes):", initialvalue=recipe.get_cooking_time())
                dietary_info = simpledialog.askstring("Update Recipe", "Enter the dietary information:", initialvalue=recipe.get_dietary_info())
                
                updated_recipe = Recipe(title, [ingredient.strip() for ingredient in ingredients.split(",")], instructions, cooking_time, dietary_info)
                self.manager.update_recipe(selected_index[0], updated_recipe)
                self.refresh_recipe_list()
    
    def delete_recipe(self):
        selected_index = self.recipe_listbox.curselection()
        if selected_index:
            self.manager.delete_recipe(selected_index[0])
            self.refresh_recipe_list()
    
    def refresh_recipe_list(self):
        self.recipe_listbox.delete(0, END)
        recipes = self.manager.get_all_recipes()
        for recipe in recipes:
            self.recipe_listbox.insert(END, recipe.get_title())
    
    def save_recipes(self):
        self.manager.save_recipes()
    
    def load_recipes(self):
        self.manager.load_recipes()
        self.refresh_recipe_list()
    
    def run(self):
        self.window.mainloop()


manager = RecipeManager()
app = RecipeManagementApp(manager)
app.run()