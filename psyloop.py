import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from funcs import *
import os, json, threading
import tkinter as tk
import cv2
from tkinter import ttk

def get_filename(projname,path):
    # put the lowest unused number after the projname to get the filename
    filename = projname
    initlen = len(projname)
    filename = filename + '1'
    while(os.path.exists(path+"\\psyloops\\"+filename+'.txt')):
        filename = str(filename[0:initlen])+str(int(filename[initlen:len(filename)+1])+1)
    return filename

def apply_function(expression, z_, t_):
    z = z_
    t = t_
    x = z_.real
    y = z_.imag
    r = abs(z_)
    th = (np.angle(z_) + 1/4)/(2*pi)
    code = f"result = {expression}"
    exec(code, globals(), locals())
    return locals()['result']

def generate_image(input_str, settings,t):
    try:
        h = 320
        w = 480
        fps = float(settings["fps"])
        scale = float(settings["scale"])
        drift = complex(settings["drift"])

        dz = 2 / min(h, w)
        dt = 1 / fps
        yy = np.arange(-(h/2)*dz, (h/2)*dz, dz)
        xx = np.arange(-(w/2)*dz, (w/2)*dz, dz)
        x, y = np.meshgrid(xx, yy)
        z = x + 1j * y
        z = z * scale + drift
        F = apply_function("gray(" + input_str + ")", z, t)

        data = np.dstack(F) * 255
        frame = data.astype(np.uint8)
        image = Image.fromarray(frame)
        return image
    except Exception as e:
        return None

def render(expression,settings):

    expression = "gray("+expression+")"

    projname = settings["projname"]
    h = int(settings["h"])
    w = int(settings["w"])
    fps = float(settings["fps"])
    duration = float(settings["duration"])
    scale = float(settings["scale"])
    drift = complex(settings["drift"])
    numscreencaps = int(settings["numscreencaps"])
    path = settings["path"]

    loadbar = ":::::::::::::::::::::::::"
    cwd = os.getcwd()

    # make a psyloops folder if the path directory doesn't have one
    directory = os.path.join(path, 'psyloops')
    if not os.path.isdir(directory):
        os.makedirs(directory)

    # initialize numframes,seconds,minutes,dt
    numframes = int(fps * duration)
    s = duration
    s = s % (24 * 3600)
    m = s // 60
    s %= 60
    dt = 1 / fps

    # initialize x,y,z
    dz = 2/min(h,w)
    yy = np.arange(-(h/2)*dz,(h/2)*dz,dz)
    xx = np.arange(-(w/2)*dz,(w/2)*dz,dz)
    x, y = np.meshgrid(xx,yy)
    z = x + 1j * y
    z = z * scale + drift
    # initialize r, th

    filename = get_filename(projname,path)

    # write the description with items 1-6
    descrip = open(path+"\\psyloops\\"+filename+'.txt',"w")
    # 1) put func in
    descrip.write("func = "+expression+"\n\n")
    # 2) then a snapshot of the settings file
    for setting in settings.keys():
        descrip.write(setting + '=' + str(settings[setting])+'\n')
    # 3) then a timestamp for the duration
    timestamp = "%02d:%02d" % (m, s)
    descrip.write("\n\n"+"#info"+"\n"+"duration: "+timestamp+"\n")
    # 4) a snapshoot of the funcs file
    funcs_file = open(cwd+'\\funcs.py',"r")
    funcs_text = funcs_file.read()
    descrip.write(funcs_text)
    funcs_file.close()
    # done with the description
    descrip.close()

    # make a screencaps directory
    os.system("mkdir "+path+"\\psyloops\\"+filename+ "_screencaps")

    # mp4 writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path+'\\psyloops\\'+filename+'.mp4', fourcc, fps, (w,h))

    # loop
    for k in range(numframes):

        t = k/numframes

        print(str(k)+"th frame of "+str(numframes),end='\r')

        F = apply_function(expression,z,t)

        data = np.dstack(F)*255
        frame = data.astype(np.uint8)
        out.write(frame)

        if((t*numscreencaps-floor(t*numscreencaps))<dt):
            image = Image.fromarray(frame)
            image.save(path+"\\psyloops\\"+filename+'_screencaps\\'+filename+"_"+str(int(t*numscreencaps))+'.png')

    out.release()
    cv2.destroyAllWindows()
    os.system(path+'\\psyloops\\'+filename+'.mp4')

    print()

def on_press():
    input_str = input_text.get("1.0", "end-1c")

    if input_str.strip():  # Check if input string is not empty or just whitespace
        # Extract values from form fields
        form_values = {}
        for label_text, entry in form_entries.items():
            form_values[label_text] = entry.get()

        render(input_str, form_values)

def load_settings():
    cwd = os.getcwd()
    settings_path = os.path.join(cwd, 'psyloop_settings.json')

    if not os.path.exists(settings_path):
        settings = {
            "projname": 'newproj',
            "h": 480,
            "w": 720,
            "fps": 60.0,
            "duration": 4.0,
            "bitdepth": 8,
            "scale": 1.0,
            "drift": "0+0j",
            "numscreencaps": 10,
            "path": 'C:\\Users\\bbhan\\Videos'
        }
        with open(settings_path, 'w') as settings_file:
            json.dump(settings, settings_file)

    with open(settings_path, 'r') as settings_file:
        settings = json.load(settings_file)

    return settings


def update_frame():
    global current_frame, t,total_frames,dt
    if paused:
        return
    if current_frame < total_frames:
        form_values = {}
        for label_text, entry in form_entries.items():
            form_values[label_text] = entry.get()
        input_str = input_text.get("1.0", "end-1c")
        t = current_frame * dt
        image = generate_image(input_str, form_values, t)
        if image:
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo
            current_frame += 1
            error_label.config(text="")
            generate_button.config(state="normal")
            root.after(int(1000*dt),update_frame)
        else:
            error_label.config(text="Invalid input")
            generate_button.config(state="disabled")
    else:
        current_frame = 0

def toggle_pause():
    global paused
    if paused:
        paused = False
        pause_button.config(text="Pause")
        update_frame()  # Restart the animation
    else:
        paused = True
        pause_button.config(text="Resume")
# Define your settings and input_str here
settings = load_settings()

current_frame = 0
t = 0.0
fps = float(settings["fps"])
dt = 1 / fps
total_frames = int(settings["duration"] * fps)  # Adjust the total number of frames as needed

root = tk.Tk()
root.title("Image Generator")

# Text Box
input_text = tk.Text(root, height=5, width=30)
input_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Bind the update function to the <KeyRelease> event of the text box
input_text.bind("<KeyRelease>", lambda event: update_frame())


default_form_values = {
    "projname": 'newproj',
    "h": 480,
    "w": 720,
    "fps": 60.0,
    "duration": 4.0,
    "bitdepth": 8,
    "scale": 1.0,
    "drift": "0+0j",
    "numscreencaps": 10,
    "path": 'C:\\Users\\bbhan\\Videos'
}
paused = False
# Pause Button
pause_button = tk.Button(root, text="Pause", command=toggle_pause)
pause_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Error label
error_label = tk.Label(root, fg="red")
error_label.grid(row=2, column=0, columnspan=2, sticky="nsew")

# Form with default values
form_frame = tk.Frame(root)
form_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

form_entries = {}

for row, (label_text, default_value) in enumerate(default_form_values.items()):
    label = tk.Label(form_frame, text=label_text)
    label.grid(column=0, row=row, padx=5, pady=5)

    entry = tk.Entry(form_frame)
    entry.insert(0, str(default_value))  # Insert default value
    entry.grid(column=1, row=row, padx=5, pady=5)
    form_entries[label_text] = entry

# Image display label
image_label = tk.Label(root)
image_label.grid(row=0, column=1, rowspan = 4, padx=10, pady=10, sticky="nsew")  # Adjusted to top-right


# Generate Image button
generate_button = tk.Button(root, text="Generate Video", state="disabled", command=on_press)
generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Configure grid row and column weights to make the layout responsive
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=3)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)

update_frame()

root.mainloop()


# MAKE IT SO THAT IT IF YOU FINISH T=0 TO 1 OF THE DEMO ANIMATION, IT WILL SAVE THAT AS FILENAME_MINI YEAH.
