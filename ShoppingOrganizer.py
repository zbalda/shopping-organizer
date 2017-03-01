""" Main Demo
    Zachary Balda
"""

from tkinter import *
import tkinter.filedialog
import csv

class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title("Shopping Organizer")
        self.headerFont = ("Helvetica", "10")
        
        self.addComponents()
        
        # Much of the information will be stored in arrays
        # Each column in our CSV file (item name, price, section, shelf, etc.) gets its own array
        # Index position 2 in any of our arrays (once they contain information) will correspond to index
        # position 2 in any other of its arrays
        # For example 2% Milk costs $4.78 and is in section 2 and shelf 4
            # if 2% Milk is in index position 3 in the item names array, index position 3 in the other
            # arrays (price, section, shelf) will have the corresponding information about that item ($4.78, section 2, shelf 4)
        self.searchResultsItemNames = []
        self.searchResultsItemPrices = []
        self.searchResultsItemSections = []
        self.searchResultsItemShelfs = []

        self.nameReferences = []
        self.priceReferences = []
        self.buttonReferences = []
        
        self.itemNameReferences = []
        self.itemPriceReferences = []
        self.itemSectionReferences = []
        self.itemShelfReferences = []
        
        self.searchResultsNameReferences = []
        self.searchResultsPriceReferences = []

        self.sectionOrganizer = []
        self.nameOrganizer = []
        self.priceOrganizer = []
        self.shelfOrganizer = []

        self.radVar = IntVar()
        
        self.totalItemSections = 30
        self.totalPrice = 0

    def addComponents(self):
        Label(self, text = "Item Search", font = self.headerFont).grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "sew")

        self.Line1 = Frame(height = 2, bg = "#808080")
        self.Line1.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "we")

        self.txtSearchInput = Entry(self)
        self.txtSearchInput.grid(row = 3, column = 0, ipadx = 25, padx = 5, pady = 5, sticky = "nsew")

        self.btnSearch = Button(self, text = "Search", command = self.getSearchResults)
        self.btnSearch.grid(row = 3, column = 1, ipadx = 35, padx = 5, pady = 5, sticky = "we")

        self.btnFindItem = Button(self, text = "Locate Item", command = self.findItem)
        self.btnFindItem.grid(row = 4, column = 0, ipadx = 15, padx = 5, pady = 5, sticky = "we")

        self.btnAddToList = Button(self, text = "Add to List", command = self.addToList)
        self.btnAddToList.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = "we")

        # Search results are packed into this frame
        self.searchResultsNamesFrame = Frame(self)
        self.searchResultsNamesFrame.grid(row = 5, column = 0, padx = 25, pady = 10, sticky = "nw")
        self.searchResultsPricesFrame = Frame(self)
        self.searchResultsPricesFrame.grid(row = 5, column = 1, ipadx = 10, padx = 20, pady = 10, sticky = "nw")

        Label(self, text = "Shopping List", font = self.headerFont).grid(row = 1, column = 2, columnspan = 3, padx = 5, pady = 5, sticky = "sew")

        self.Line2 = Frame(height = 2, bg = "#808080")
        self.Line2.grid(row = 2, column = 2, columnspan = 3, padx = 5, sticky = "we")

        self.btnViewMap = Button(self, text = "View Map", command = self.ViewMap)
        self.btnViewMap.grid(row = 3, column = 2, ipadx = 15, padx = 5, sticky = "we")

        self.btnFindItems = Button(self, text = "Find Items", command = self.FindItems)
        self.btnFindItems.grid(row = 3, column = 3, columnspan = 2, ipadx = 12, padx = 5, sticky = "we")

        self.lblTotalPrice = Label(self, text = "Total:")
        self.lblTotalPrice.grid(row = 4, column = 2, ipadx = 10, padx = 5, sticky = "we")

        self.lblTotal = Label(self, text = "$0")
        self.lblTotal.grid(row = 4, column = 3, columnspan = 2, ipadx = 10, padx = 4, sticky = "w")

        # Shopping list info is gridded into this frame
        self.shoppingListFrame = Frame(self)
        self.shoppingListFrame.grid(row = 5, column = 2, columnspan = 3, padx = 15, pady = 9, sticky = "nsew")
        
    def getSearchResults(self):
        # Remove all previous search results at the start of each search
        self.removeSearchResults()

        # Get the entered text
        searchEntry = self.txtSearchInput.get()
        searchEntry = searchEntry.upper()

        # Each column in the CSV file will get its own array
        self.itemNames = []
        self.keyTerms1 = []
        self.keyTerms2 = []
        self.keyTerms3 = []
        self.itemPrices = []
        self.itemSections = []
        self.itemShelfs = []

        # Those are narrowed down to only the search results
        self.searchResultsItemNames = []
        self.searchResultsItemPrices = []
        self.searchResultsItemSections = []
        self.searchResultsItemShelfs = []
    
        # Here we go through the CSV file and add terms to their arrays line by line
        file = open("Store Database.csv", "r")
        for line in file:
            currentLine = line.split(",")
            (Name, KT1, KT2, KT3, Price, Section, Shelf, Status) = currentLine
            self.itemNames.append(Name)
            self.keyTerms1.append(KT1)
            self.keyTerms2.append(KT2)
            self.keyTerms3.append(KT3)
            self.itemPrices.append(Price)
            self.itemSections.append(Section)
            self.itemShelfs.append(Shelf)

        file.close()
 
        # Each item in the CSV file has 3 key terms.
        # This here goes through each line in the CSV file, and checks the three terms for any matches
        # If there are any matches, it adds those to the search results arrays
        for i in range(0, len(self.itemNames)):
            # If the search entry is blank the search button wont do anything
            if searchEntry == "":
                pass
            elif searchEntry == self.keyTerms1[i]:
                self.searchResultsItemNames.append(self.itemNames[i])
                self.searchResultsItemPrices.append(self.itemPrices[i])
                self.searchResultsItemSections.append(self.itemSections[i])
                self.searchResultsItemShelfs.append(self.itemShelfs[i])
            elif searchEntry == self.keyTerms2[i]:
                self.searchResultsItemNames.append(self.itemNames[i])
                self.searchResultsItemPrices.append(self.itemPrices[i])
                self.searchResultsItemSections.append(self.itemSections[i])
                self.searchResultsItemShelfs.append(self.itemShelfs[i])
            elif searchEntry == self.keyTerms3[i]:
                self.searchResultsItemNames.append(self.itemNames[i])
                self.searchResultsItemPrices.append(self.itemPrices[i])
                self.searchResultsItemSections.append(self.itemSections[i])
                self.searchResultsItemShelfs.append(self.itemShelfs[i])
            else:
                pass

        # Now we create GUI objects for the search results
        self.searchResultsNameReferences = []
        self.searchResultsPriceReferences = []
        # The first button created will hold the value 0, the second 1, etc.
        # This is important because that value will later be accessed and used to find the
        # index positions of the selected information in the search results. For example,
        # if the second button is selected, the value 1 will be returned. This number
        # corresponds to the index position of the information about that button in the search result arrays
        self.radVar = IntVar()
        for i in range(0, len(self.searchResultsItemNames)):
            name = self.searchResultsItemNames[i]
            price = self.searchResultsItemPrices[i]
            price = str(price)
            price = ("${}".format(price))
            # Here (which I will do a lot), I append a gui object to an array. I do this to be able to access and remove it later
            # OnceI create the object, I then find the last object added to the array (the one we just created) and grid it
            self.searchResultsNameReferences.append(Radiobutton(self.searchResultsNamesFrame, text = name, variable = self.radVar, value = i))
            self.searchResultsNameReferences[-1].pack()
            self.searchResultsPriceReferences.append(Label(self.searchResultsPricesFrame, text = price))
            self.searchResultsPriceReferences[-1].pack(pady = 2)

    def removeSearchResults(self):
        # This method is called at the start of each search
        # Search results are packed into a frame. Here we remove all of those from that frame with pack_forget
        for radioButton in self.searchResultsNameReferences:
            radioButton.pack_forget()
        # We do the same for labels
        for label in self.searchResultsPriceReferences:
            label.pack_forget()
        # Next we actaully remove them from their arrays
        del self.searchResultsNameReferences
        del self.searchResultsPriceReferences

    def findItem(self):
        # This method opens up a window giving information about the item that is currently selected
        # If there are no search results, the method does nothing
        if len(self.searchResultsItemNames) != 0:
            # Here we take the value of the radio button which represents the index position of the
            # information we need in the search results arrays
            selectedItem = self.radVar.get()

            # We narrow now our search results to the search item we have selected
            itemName = self.searchResultsItemNames[selectedItem]
            itemPrice = self.searchResultsItemPrices[selectedItem]
            itemSection = self.searchResultsItemSections[selectedItem]
            itemShelf = self.searchResultsItemShelfs[selectedItem]

            itemName = ("{}".format(itemName))
            itemPrice = ("Price: ${}".format(itemPrice))
            itemSection = ("Section: {}".format(itemSection))
            itemShelf = ("Shelf: {}".format(itemShelf))

            # We create the window we want to put the information in
            self.itemDetails = Toplevel(self)
            self.itemDetails.title(itemName)

            # Next we label and grid the information
            Label(self.itemDetails, text = itemName).grid(row = 1, column = 0, padx = 10, pady = 20)
            Label(self.itemDetails, text = itemPrice).grid(row = 1, column = 1, padx = 10, pady = 20)
            Label(self.itemDetails, text = itemSection).grid(row = 1, column = 2, padx = 10, pady = 20)
            Label(self.itemDetails, text = itemShelf).grid(row = 1, column = 3, padx = 10, pady = 20)
       
    def addToList(self):
        # This method takes our selected item and adds it to the shopping list
        # If there are no search results, the method does nothing
        if len(self.searchResultsItemNames) != 0:
            # Next we are going to do almost the same thing we did with the findItem method
            selectedItem = self.radVar.get()

            # Get the information we need about our selected item in search results
            self.itemName = self.searchResultsItemNames[selectedItem]
            self.itemPrice = self.searchResultsItemPrices[selectedItem]
            # Add a $ to the item price
            self.itemPriceText = str(self.itemPrice)
            self.itemPriceText = ("${}".format(self.itemPrice))
            self.itemSection = self.searchResultsItemSections[selectedItem]
            self.itemShelf = self.searchResultsItemShelfs[selectedItem]

            # Next we want to add the button to the end of the shopping list item information arrays and to the
            # end of the shopping list gui objects
            i = len(self.buttonReferences)
            # Row position must get + 1 since rows start at 1
            rowPosition = len(self.buttonReferences) + 1

            # Shopping list info is gridded to its own frame
            # Like we did with getting the search results, here we are going to append our gui objects to
            # the arrays we have created for holding name, price, etc. info for the shopping list
            # After doing that we find the last object created and grid it
            self.nameReferences.append(Label(self.shoppingListFrame, text = self.itemName))
            self.nameReferences[-1].grid(row = rowPosition, column = 0, ipadx = 10, pady = 1)
            self.priceReferences.append(Label(self.shoppingListFrame, text = self.itemPriceText))
            self.priceReferences[-1].grid(row = rowPosition, column = 1, ipadx = 12, pady = 1)
            # Simply put, each button needs to know how to 'delete itself'
            # Here, we give each button a number that corresponds to its index position in the button references array (this number is i above)
            # Each button is gridded to that position
            # This works until we remove one of the buttons. After that, their grid position does not
            # reflect their index position in the button references array
            # To fix that, we give the command of the botton a value corresponding to the point it was
            # created at that can be accessed and changed later
            self.buttonReferences.append(Button(self.shoppingListFrame, text = "x", command = lambda position = i: self.removeListItem(position)))
            self.buttonReferences[-1].grid(row = rowPosition, column = 2, padx = 20, pady = 1, sticky = "nsew")

            # Not all information is gridded. Some is just needed to be accessed later
            self.itemNameReferences.append(self.itemName)
            self.itemPriceReferences.append(self.itemPrice)
            self.itemSectionReferences.append(self.itemSection)
            self.itemShelfReferences.append(self.itemShelf)

            # See calcTotal method for info
            self.calcTotal()

    def removeListItem(self, i):
        # Each button has its own value that corresponds to its index position in its own array
        # When a button is clicked, that value is passed through this method as i

        # The first thing we do is remove that button and its corresponding info from the grid
        self.nameReferences[i].grid_forget()
        self.priceReferences[i].grid_forget()
        self.buttonReferences[i].grid_forget()

        # Next we actually delete that button and its corresponding information 
        del self.nameReferences[i]
        del self.priceReferences[i]
        del self.buttonReferences[i]

        del self.itemNameReferences[i]
        del self.itemPriceReferences[i]
        del self.itemSectionReferences[i]
        del self.itemShelfReferences[i]

        # Next, we reassign the index position value (newPosition) to each button and gui item
        # so that each button command correctly represents its position in the button references array
        # Enumerate splits the for loop into number value and object reference.
        # Each button object is then given the command value 'newPosition' and re-gridded to that position
        for newPosition, button in enumerate(self.buttonReferences):
            button.configure(command = lambda position=newPosition: self.removeListItem(position))
            self.nameReferences[newPosition].grid(row = newPosition + 1, column = 0, ipadx = 10, pady = 1)
            self.priceReferences[newPosition].grid(row = newPosition + 1, column = 1, ipadx = 12, pady = 1)
            self.buttonReferences[newPosition].grid(row = newPosition + 1, column = 2, padx = 20, pady = 1)

        self.calcTotal()

    def ViewMap(self):
        # The view map method simply creates a window and adds a png image to it
        self.map = Toplevel(self)
        self.map.title("Map")
        self.map.geometry("896x695")

        pngImage = PhotoImage(file = "Grocery Store Layout Map.png")
        imageLabel = Label(self.map, image = pngImage).grid()
        # Image not defined error
        imageLabel.image = pngImage
        self.map.grid()

    def FindItems(self):
        # If there are no items in the shopping list, this method does nothing
        if len(self.nameReferences) != 0:
            # First, we create a window that will hold our organized information
            self.organizerWindow = Toplevel(self)
            self.organizerWindow.title("Organizer")

            # The row starts at 1 and every time a label or labels are added it increments by 1
            textRow = 1
            includedSections = []
            # The first thing we do is find every section that we will need to go to
            # This for loop finds every section included in itemSectionReferences and adds them
            # to a array (values of the item sections in the array are in ascending order)
            # Sample includedSections value after it is run: [1, 2, 2, 4, 5, 5, 7, 8, 8, 8]
            for i in range(1, self.totalItemSections):
                for x in range(0, len(self.itemSectionReferences)):
                    a = int(self.itemSectionReferences[x])
                    if a == i:
                        includedSections.append(a)
            # This here removes all repeated values in the included sections
                # [1, 2, 2, 4, 5, 5, 7, 8, 8, 8] > [1, 2, 4, 5, 7, 8]
            includedSections = sorted(set(includedSections))
            # Next, we go through each position in the included sections, take the value of that
            # position, create a label for it, and find all items in the shopping list that have that value
            for i in range(0, len(includedSections)):
                # titleInt holds the calue of the section in the included sections array ay position i
                titleInt = includedSections[i]
                titleText = ("Section {}".format(str(titleInt)))
                sectionTitle = Label(self.organizerWindow, text = titleText)
                sectionTitle.grid(row = textRow, column = 0, columnspan = 3, sticky = "nsew")
                textRow += 1
                # Here we search each item section value in the shopping list and see if it matches our value
                for x in range(0, len(self.itemSectionReferences)):
                    a = int(self.itemSectionReferences[x])
                    # If an item section does match our valuem we create labels for it
                    if a == titleInt:
                        # We get the text values for the labels we are going to create
                        name = self.itemNameReferences[x]
                        price = self.itemPriceReferences[x]
                        shelf = self.itemShelfReferences[x]

                        price = ("${}".format(str(price)))
                        shelf = ("Shelf: {}".format(shelf))

                        # We create the labels and grid them
                        nameOrganizer = Label(self.organizerWindow, text = name)
                        nameOrganizer.grid(row = textRow, column = 0, ipadx = 10)
                        priceOrganizer = Label(self.organizerWindow, text = price)
                        priceOrganizer.grid(row = textRow, column = 1)
                        shelfOrganizer = Label(self.organizerWindow, text = shelf)
                        shelfOrganizer.grid(row = textRow, column = 2, ipadx = 10)

                        # The row position is then incremented
                        textRow += 1

            # When then grab the total price of the shopping list and add its label to the end
            textRow += 1
            text = ("Total: {}".format(self.totalPrice))
            total = Label(self.organizerWindow, text = text)
            total.grid(row = textRow, column = 0, columnspan = 3, pady = 15, sticky = "we")

            textRow += 1
            # Last, we create two buttons. One that opens our map image
            # and another that runs the closeOrganizer function that closes our window
            btnViewMap = Button(self.organizerWindow, text = "View Map", command = self.ViewMap)
            btnViewMap.grid(row = textRow, column = 0, columnspan = 2, ipadx = 10, padx = 5, pady = 10, sticky = "we")
            btnClose = Button(self.organizerWindow, text = "Close", command = self.closeOrganizer)
            btnClose.grid(row = textRow, column = 2, ipadx = 10, padx = 5, pady = 10, sticky = "we")  
                        
    def closeOrganizer(self):
        # Note: If more than one organizer is open, it can only remove the last one
        self.organizerWindow.destroy()

    def calcTotal(self):
        # Calc total is called every time an item is added or removed from the shopping list
        # First, it sets the total back to zero
        self.totalPrice = 0.0
        # Next, it goes through each index position in the itemPriceReferences (price information about all shopping list items) and
        # adds them together to get the current total price
        for a in range(0, len(self.itemPriceReferences)):
            price = self.itemPriceReferences[a]
            price = float(price)
            self.totalPrice = self.totalPrice + price
        self.totalPrice = round(self.totalPrice, 2)
        self.totalPrice = str(self.totalPrice)
        self.totalPrice = ("${}".format(self.totalPrice))
        # Then, it takes that total and updates the total price label
        self.lblTotal = Label(self, text = self.totalPrice)
        self.lblTotal.grid(row = 4, column = 3, columnspan = 2, ipadx = 10, padx = 4, sticky = "w")

def main():
    a = App()
    a.mainloop()

if __name__ == "__main__":
    main()
