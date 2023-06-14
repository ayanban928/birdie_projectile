#import libaries
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def birdie_motion(velocity, angle, mass):
    #Converting degrees to radians for angle projectile was shot from
    theta = np.radians(angle)

    #Gravitational acceleration constant
    g = 9.8

    #time it took for birdie to fly
    t_flight = 2 * velocity * np.sin(theta) / g

    #Time interval for birdie
    t = np.linspace(0, t_flight, num=100)

    #Birdie's horizontal distance traveled (kinematics)
    x = velocity * np.cos(theta) * t

    #Birdie's vertical distance traveled (kinematics)
    y = velocity * np.sin(theta) * t - 0.5 * g * t**2

    return t, x, y

#requesting the user for velocity, angle, and mass values, if values are not positive user will be asked to input again
def correct():
    try:
        velocity = float(velocity_entry.get())
        angle = float(angle_entry.get())
        mass = float(mass_entry.get())

        if velocity <= 0 or angle <= 0 or mass <= 0:
            raise ValueError

        return velocity, angle, mass
    except ValueError:
        tk.messagebox.showerror("Invalid Input", "Please enter positive numeric values for velocity, angle, and mass.")
        return None

#animation graph for the birdie
def animate_graph(i, t, x, y, line):
    line.set_data(x[:i+1], y[:i+1])  

def traject_animation():
    inputs = correct()
    if inputs is None:
        return

    velocity, angle, mass = inputs

    #Calculating the velocity, angle, and mass of the birdie undergoing projectile motion 
    t, x, y = birdie_motion(velocity, angle, mass)

    #clear animation 
    plt.clf()

    #creating a new graph for birdie animation
    fig, ax = plt.subplots()

    # Set up the plot settings
    ax.set_xlim([0, np.max(x) + 1])
    ax.set_ylim([0, np.max(y) + 1])
    ax.set_xlabel('Horizontal Distance (m)')
    ax.set_ylabel('Vertical Distance (m)')
    ax.set_title('Projectile Motion')

    line, = ax.plot([], [], 'ro', animated=True)

    def update_animation(frame):
        animate_graph(frame, t, x, y, line)
        return line,

    #animation of birdie in the graph
    ani = animation.FuncAnimation(fig, update_animation, frames=len(t), interval=100, blit=True)

    #opening up a new tab for the animation
    animation_window = tk.Toplevel()
    animation_window.title("Animated Projectile Motion")
    animation_window.geometry("400x400")

    #canvas for animation
    canvas = FigureCanvasTkAgg(fig, master=animation_window)
    canvas._tkcanvas.pack()

    #tkinter loop for the animation tab of birdie
    animation_window.mainloop()

#GUI window for animation
window = tk.Tk()
window.title("Badminton Projectile Motion")
window.geometry("400x350")

#Labeling all the sections (velocity, angle, mass)
velocity_label = tk.Label(window, text="Initial Velocity (m/s):")
velocity_label.pack()
velocity_entry = tk.Entry(window)
velocity_entry.pack()

angle_label = tk.Label(window, text="Launch Angle (degrees):")
angle_label.pack()
angle_entry = tk.Entry(window)
angle_entry.pack()

mass_label = tk.Label(window, text="Birdie Mass (kg):")
mass_label.pack()
mass_entry = tk.Entry(window)
mass_entry.pack()

#animation button
animate_button = tk.Button(window, text="Animate", command=traject_animation)
animate_button.pack()

#run the GUI page
window.mainloop()
