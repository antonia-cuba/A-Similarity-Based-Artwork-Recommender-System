* Code related to the implementation of an artwork recommender system based on natural language processing of artwork descriptions

Content of source files:
- similarity.py - back-end part of the app, functions to compute similarity between topics of descriptions of artworks documents
- gui.py - the user interface in Tkinter
- Artworks folder - contains images of artworks
- Descriptions of artworks folder - contains the descriptions of artworks in txt documents
- Result Topics - contains the topics of the descriptions, extracted with the LDA program
- BSP4_TM_GUI-main folder - contains the LDA program developed by Julien Simon

To open the application, extract files, open the inner folder "BSP2 Artwork recommender - Antonia Cuba" in a code editor and run the file gui.py. 
The similarity measurement method can be changed in line 165 of gui.py.

To use the LDA program, open the program.py file and change the file name on line 354. The file with topics will be saved in the Result Topics folder. 
Then, extract the txt file with the topics from the subfolders and place it in the main Result Topics folder. The subfolders can be deleted.