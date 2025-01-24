from tkinter import *
from tkinter import filedialog
import numpy as np
import cv2
from PIL import Image, ImageTk


# Create the root window
window = Tk()
window.title('CMSC 165 Hackathon')
window.geometry("")
window.config(background = "white")


# function used to resize the image 
def ResizeUsingRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)


def countPollens():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Img files", "*.jpg*"), ("all files", "*.*")))
    
    # read the image as grayscale
    raw_image = cv2.imread(filename,0)
    # blur the image
    blur_image = cv2.medianBlur(raw_image, 5)
    # convert grayscale to color
    color_img = cv2.cvtColor(blur_image,cv2.COLOR_GRAY2BGR)
    # Apply HoughCircles Transformation to get the circles from blur_image
    # image1
    circles = cv2.HoughCircles(blur_image,cv2.HOUGH_GRADIENT,0.5,30,param1=20,param2=27,minRadius=20,maxRadius=50)
    # cast the circle parameters to integers
    circles = np.uint16(np.around(circles))

    # retrieve amount of circles detected by HoughCircles
    dark = 0
    light = 0
    
    # draw the circles using a for loop
    # count the amount of circles too
    for i in circles[0,:]:
        # draw outer circle
        color = int (raw_image[i[1], i[0]])

        if (color > 65):
            # draw center of the circle
            cv2.circle(color_img,(i[0],i[1]),i[2],(0,0,255),2)
            cv2.circle(color_img,(i[0],i[1]),2,(0,0,255),3)
            light = light + 1
        else:
            # draw center of the circle
            cv2.circle(color_img,(i[0],i[1]),i[2],(0,255,255),2)
            cv2.circle(color_img,(i[0],i[1]),2,(0,255,255),3)
            dark = dark + 1

    # resize the image for displaying
    resize = ResizeUsingRatio(color_img, width=1280)

    # print the amount of circles
    print("counted light pollens: ", light)
    print("counted dark pollens: ", dark)

    # exit
    # cv2.destroyAllWindows()

    # Change label contents
    # label_file_explorer.configure(text="File Opened: "+ filename)
    for label in window.grid_slaves():
        label.grid_forget()

    img2 = Image.fromarray(color_img).resize((700, 500))
    imgtk = ImageTk.PhotoImage(image=img2)
    label = Label(image=imgtk)
    label.image = imgtk

    # Create a Label to display the image
    output_img = Label(window, image= imgtk)
    output_img.grid(column=2, row=1, rowspan=3, columnspan=3, padx=5, pady=5)

    btn_frame = Frame(window, bg="white")
    button_explore = Button(btn_frame, text = "BROWSE IMAGES", font=("Poppins", 10, "bold"), width=15, height=2, command=countPollens)
    button_save = Button(btn_frame, text = "SAVE IMAGE", font=("Poppins", 10, "bold"), width=15, height=2, command=lambda: save(img2))
    button_exit = Button(btn_frame, text = "EXIT", font=("Poppins", 10, "bold"), width=15, height=2, command=exit)

    button_explore.grid(column=1, row=1, padx=5, pady=5)
    button_save.grid(column=1, row=2, padx=5, pady=5)
    button_exit.grid(column=1,row=3, padx=5, pady=5)
    btn_frame.grid(column=1, row=1, pady=0)

    result_frame = Frame(window, bg="white", highlightbackground="black", highlightthickness=2)

    light_count = light
    dark_count = dark
    
    data_lbl = Label(result_frame, text = "DATA:", font=("Poppins", 12, "bold"), height=2, fg = "black", bg = "white")
    light_lbl = Label(result_frame, text = "Light-Colored Pollens", font=("Poppins", 10, "bold"), height=2, fg = "black", bg = "white")
    dark_lbl = Label(result_frame, text = "Dark-Colored Pollens", font=("Poppins", 10, "bold"), height=2, fg = "black", bg = "white")
    light_count_lbl = Label(result_frame, text = str(light_count), font=("Poppins", 10, "bold"), height=2, fg = "black", bg = "white")
    dark_count_lbl = Label(result_frame, text = str(dark_count), font=("Poppins", 10, "bold"), height=2, fg = "black", bg = "white")

    data_lbl.grid(column=1, row=1, rowspan=2, padx=50)
    light_lbl.grid(column=2, row=1, padx=50)
    dark_lbl.grid(column=2, row=2, padx=50)
    light_count_lbl.grid(column=3, row=1, padx=50)
    dark_count_lbl.grid(column=3, row=2, padx=50)
    result_frame.grid(column=3, row=4, pady=10)


def save(img_result):
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    img_result.save(filename)

# START PROMPT
label_file_explorer = Label(window, text = "CMSC 165 HACKATHON", font=("Poppins", 25, "bold"), height=2, fg = "black", bg = "white")
button_explore = Button(window, text = "BROWSE IMAGES", font=("Poppins", 10, "bold"), width=20, height=2, command=countPollens)
button_exit = Button(window, text = "EXIT", font=("Poppins", 10, "bold"), width=20, height=2, command=exit)

label_file_explorer.grid(column=1, row=1, columnspan=2)
button_explore.grid(column=1, row=2, padx=20, pady=20)
button_exit.grid(column=2,row=2, padx=20, pady=20)

# Let the window wait for any events
window.mainloop()