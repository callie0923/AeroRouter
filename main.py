import tkinter as tk

# Create a GUI window
window = tk.Tk()
window.title("Flight Options")
window.geometry("800x600")

# Create a label to display the output
result_label = tk.Label(window, text="Click the button to display flight information.")
result_label.pack()

# Function to display flight options
def display_flight_options():
    result_label.config(text="Flight information displayed.")

# Create a button to generate flight options
run_button = tk.Button(window, text="Generate Flight Options", command=display_flight_options)
run_button.pack()

# Start the GUI main loop
window.mainloop()
