# This is a sample Python script.
from tkinter import*
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

root = Tk()

def Submit():
    #top = Toplevel()
    myLabel = Label(root, text="Form has been submitted.Please wait while we process your order", font=(25))
    Window1off()
    myLabel.grid(row=12, column=0)

def Window1off():
    BudgetText.destroy()
    BudgetInputText.destroy()
    budgetInput.destroy()
    ExemptionText.destroy()
    meatCheck.destroy()
    vegetableCheck.destroy()
    fruitCheck.destroy()
    diaryCheck.destroy()
    grainCheck.destroy()
    SubmitButton.destroy()
    StartingTextEmpty2.destroy()

def SaveInputs():# used to update variables
    budgetAmount = budgetInput.get()
    MeatOption = meat.get()
    veggieOption = vegetable.get()
    fruitOption = fruit.get()
    diaryOption = fruit.get()
    grainOption = fruit.get()


#create a label Widget
StartingText = Label(root, text="Hello and Welcome to our shopping list Application", font=(30))
StartingTextEmpty = Label(root, text="  ")
StartingTextEmpty2 = Label(root, text="  ")

BudgetText = Label(root, text="Please input a budget amount in the input field without $")
BudgetInputText = Label(root, text = "PLease enter amount:")
budgetInput = Entry()
budgetInput.insert(0, "0")



ExemptionText = Label(root, text= "Please check off any food tree type you don't want in your list")
#1 is checked and 0 is unchecked
meat = IntVar()  # used later for algorithm
meatCheck = Checkbutton(root, text="Do you not want meat in your shopping list", variable= meat)

vegetable = IntVar()  # used later for algorithm
vegetableCheck = Checkbutton(root, text="Do you not want vegetables in your shopping list", variable= vegetable)

fruit = IntVar()  # used later for algorithm
fruitCheck = Checkbutton(root, text="Do you not want fruits in your shopping list", variable= fruit)

diary = IntVar()  # used later for algorithm
diaryCheck = Checkbutton(root, text="Do you not want diary in your shopping list", variable= diary)

grain = IntVar()  # used later for algorithm
grainCheck = Checkbutton(root, text="Do you not want grain like bread or rice in your shopping list", variable= grain)

SubmitButton = Button(root, text="Submit your budget", padx=100, command=Submit, fg= "white", bg= "black")

#Shoving it onto the screen
StartingText.grid(row=0, column=0)
StartingTextEmpty.grid(row=1, column= 0)
BudgetText.grid(row=2, column=0)
#BudgetInputText.grid(row=3, column=0)
budgetInput.grid(row=3, column=0)
ExemptionText.grid(row= 4, column=0)
meatCheck.grid(row= 5, column=0)
vegetableCheck.grid(row= 6, column=0)
fruitCheck.grid(row= 7, column=0)
diaryCheck.grid(row= 8, column=0)
grainCheck.grid(row= 9, column=0)
StartingTextEmpty2.grid(row=10, column= 0)

SubmitButton.grid(row=11, column=0)
root.mainloop()

# Press the green button in the gutter to run the script.
#if __name__ == '__main__':


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
