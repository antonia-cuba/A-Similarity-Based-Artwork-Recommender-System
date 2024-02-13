from tkinter import *
from PIL import Image, ImageTk, UnidentifiedImageError
from similarity import *


# each artwork is a object containing the image filename and resulted topics filename
class Artwork():
    def __init__(self, name, topics):
        self.name = name
        self.topics = topics


# build main elements of interface
root = Tk()
root.title("Artwork recommender")
root.geometry("840x700")

# configure rows and columns starting index and weigth (width)
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

frame_main = Frame(root, bg="gray")
frame_main.grid()

# build the page for selecting the artworks - HOMEPAGE
def screen1():
    # use 'global' because we need frame1 in another function (screen2) - to remove the initial frames
    # frame for text
    global frame1
    frame1 = LabelFrame(frame_main, padx=5, pady=5)
    frame1.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    text = Label(frame1, text = "Click on one artwork and discover three more that are similar to it!")
    text.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # frame for the canvas for artwork images
    global frame_canvas
    frame_canvas = Frame(frame_main)
    frame_canvas.grid(row=2, column=0)
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)

    # add a canvas in the frame
    global canvas
    canvas = Canvas(frame_canvas)
    canvas.grid(row=0, column=0)

    # frame for artwork images
    global frame2
    frame2 = LabelFrame(canvas)

    # ADD ARTWORK BUTTONS - manual version
    # use global for the image to not be removed by the garbage collector
    # global artwork_matrix
    # artwork_matrix = Image.open(r"Artworks\12.png")
    # artwork_matrix = artwork_matrix.resize((200, 200), Image.ANTIALIAS)
    # artwork_matrix = ImageTk.PhotoImage(artwork_matrix)
    # button1 = Button(frame2, image=artwork_matrix, command=screen2)    
    # button1.grid(row=2, column=0, padx=10, pady=10)

    # global artwork2
    # artwork2 = Image.open(r"Artworks\11.png")
    # artwork2 = artwork2.resize((200, 200), Image.ANTIALIAS)
    # artwork2 = ImageTk.PhotoImage(artwork2)
    # button2 = Button(frame2, image=artwork2, command=screen2)    
    # button2.grid(row=2, column=1, padx=10, pady=10)

    # global artwork3
    # artwork3 = Image.open(r"Artworks\10.png")
    # artwork3 = artwork3.resize((200, 200), Image.ANTIALIAS)
    # artwork3 = ImageTk.PhotoImage(artwork3)
    # button3 = Button(frame2, image=artwork3, command=screen2)    
    # button3.grid(row=2, column=2, padx=10, pady=10)


    # make a list of all artworks as objects with image filename and topics filename
    global art_files
    art_files = []
    directory = "Artworks"
    # iterate through all files in directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            # update the artworks list with new artwork object
            art_files.append(Artwork(f, "Result Topics\%s.txt_4t_4w.txt" % f[9:].split(".")[0]))
            #print(art_files[i].name)
            #print(art_files[i].topics)


    # decide how many columns and rows of artworks to display
    columns = 3
    # rows = 25
    # display as many complete rows as possible
    rows = int(len(art_files) / columns)
    global artwork_img
    global artwork_matrix
    # matrix of images
    artwork_img= [[Artwork for j in range(columns)] for i in range(rows)]
    # matrix of Artwork objects
    artwork_matrix = [[Artwork for j in range(columns)] for i in range(rows)]
    # matrix of buttons
    buttons = [[Button() for j in range(columns)] for i in range(rows)]


    # add artwork images as buttons on Homepage
    k = 0
    for i in range(0, rows):
        for j in range(0, columns):
            artwork_matrix[i][j] = Artwork(art_files[k].name, art_files[k].topics)
            k=k+1
            try:
                artwork_img[i][j] = Image.open("%s" % artwork_matrix[i][j].name)
                artwork_img[i][j] = artwork_img[i][j].resize((200, 200), Image.ANTIALIAS)
                artwork_img[i][j] = ImageTk.PhotoImage(artwork_img[i][j])
                # when clicking a button, go to Recommendations page
                buttons[i][j] = Button(frame2, image = artwork_img[i][j], command=lambda i=i, j=j:[screen2(i, j)])
                buttons[i][j].grid(row=i, column=j, padx=10, pady=10)
            except UnidentifiedImageError:
                print("There is a file different from the image file types in the directory Artworks. Can not display the file as image.")

    addScrollbar(frame2, 590)


# build the page for displaying the recommended artworks - RECOMMENDATIONS PAGE
def screen2(i, j):
    # remove the text and images from the first screen
    frame1.destroy()
    frame2.destroy()

    ii = i
    jj = j
    
    # new frame
    global frame3
    frame3 = LabelFrame(canvas, padx=5, pady=5)
    frame3.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    text = Label(frame3, text = "The artwork you've chosen:")
    text.grid(row=1, column=1, padx=10, pady=10)

    # display the image of the clicked artwork as a button, to maintain design
    global clicked_artwork
    clicked_artwork= Image.open("%s" % artwork_matrix[i][j].name)
    clicked_artwork= clicked_artwork.resize((200, 200), Image.ANTIALIAS)
    clicked_artwork= ImageTk.PhotoImage(clicked_artwork)
    button_clicked_artwork = Button(frame3, image = clicked_artwork)    
    button_clicked_artwork.grid(row=2, column=1, padx=10, pady=10)

    text = Label(frame3, text = "The 3 most similar artworks:")
    text.grid(row=3, column=1, padx=10, pady=10)


    # decide how many recommended artworks to display
    # columns should not exceed 3
    columns = 3
    rows = 1

    # matrix of buttons
    buttons = [[Button() for j in range(columns)] for i in range(rows)]

    # compute similarity values
    # change version of function depending on what similarity method you want to use
    # computeSimilarity1 or computeSimilarity2 or computeSimilarity3
    similar_art = computeSimilarity1(artwork_matrix[i][j].topics)

    # extracts the keys of the dictionary as a list; contains the topics files
    similar_art = list(similar_art)

    k = 0
    ok = 0
    i = 0
    j = 0
    p = 0
    # check to not exceed the predefined number of recommended artworks
    while p<rows*columns and k < len(similar_art):
        ok = 0
        # get the images filenames for the similar art
        for a in art_files:
            if similar_art[k] == a.topics and similar_art[k] != artwork_matrix[ii][jj].topics:
                art_name = a.name
                ok = 1
        # if similar artwork has been found, display its image on button
        if ok == 1:
            artwork_img[i][j] = Image.open("%s" % art_name)
            artwork_img[i][j] = artwork_img[i][j].resize((200, 200), Image.ANTIALIAS)
            artwork_img[i][j] = ImageTk.PhotoImage(artwork_img[i][j])
            buttons[i][j] = Button(frame3, image = artwork_img[i][j])
            buttons[i][j].grid(row=i+4, column=j, padx=10, pady=10)
            j = j + 1
            # check if max number of images on a row has been reached, start a new row
            if j == columns:
                j = 0
                i = i + 1
            p = p + 1
        k = k + 1

    button1 = Button(frame3, text="Try another artwork", command=lambda:[screen1(), frame3.destroy()])    
    button1.grid(row=rows+4, column=1, padx=10, pady=10)

    addScrollbar(frame3, 620)

# add vertical scrollbar of heigth 'h' to the canvas of 'frame'
def addScrollbar(frame, h):
    vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)

    frame2.update_idletasks()
    frame_canvas.config(width=980 + vsb.winfo_width(), height=500)

    canvas.create_window((1,1), window=frame, anchor="nw")
    # configure the scroll region of the canvas
    canvas.config(scrollregion=canvas.bbox("all"), width=680, height=h)

    # start at the top position of the scrollbar
    canvas.yview_moveto(0)


# call function to display Homepage
screen1()

root.mainloop()
