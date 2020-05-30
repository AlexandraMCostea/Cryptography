from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.title("Tema 1 Criptografie")
root.geometry("630x200")
root['background'] = "#008000"


# Creating menu
CipherList = [
    "Caesar",
    "Vigenere"
]

cipherVar = StringVar(root)
cipherVar.set(CipherList[0])

cipherOpt = OptionMenu(root, cipherVar, *CipherList)
cipherOpt.config(width=10, font=('Helvetica', 12))
cipherOpt.grid(row = 0, column = 0)
cipherOpt.configure(background="grey")

#Choose file for encryption/decryption
def openFile():
    global filename
    global data
    filename = filedialog.askopenfilename(title="Choose a file.", filetypes=(("text files","*.txt"),("All files","*.*")))
    
    #To make sure you won't introduce the wrong type of file and get an error just use the following line instead
    #filename = filedialog.askopenfilename(title="Choose a file.", filetypes=(("text files","*.txt")))
    
    browse.insert(END, filename)
    with open(filename) as file:
        data = file.read()

btn = Button(root, text="Choose file", font=40, command=openFile)
btn.grid(row=2, column=1)
browse = Entry(root, font=40, width=31)
browse.grid(row=2, column=2, columnspan=2)



#Enter key for cipher and verify key
keyLabel = Label(root, text = "Introduce the key:", font=40).grid(row=3, column=1)
keyEntry = Entry(root, font=40)
keyEntry.grid(row=3,column=2, padx=10, pady=10)

def verifyKey():
    global key
    key = keyEntry.get()
    if cipherVar.get() == "Caesar":
        if key.isnumeric() != 0:
            print("Cheie ok")
            messagebox.showinfo("Info", "Cheie verificata si inregistrata!")
        else:
            print("cheie not ok")
            messagebox.showerror("Error", "Cheie invalida!")
            keyEntry.delete(0, END)

    if cipherVar.get() == "Vigenere":
        regex = re.compile('[@_!#$%^&*()<>0123456789?/\\| }{~:]')
        if (regex.search(key) == None):
            print("Cheie ok")
            messagebox.showinfo("Info", "Cheie verificata si inregistrata!")
        else:
            print("Cheie not ok")
            messagebox.showerror("Error", "Cheie invalida!")
            keyEntry.delete(0, END)
    return

btnKey = Button(root, text="Apply key", font=40, command=verifyKey)
btnKey.grid(row=3, column=3, padx=10, pady=10)


#Caesar cipher
def encodeCaesar(text, s):
    result = ""
    # transverse the plain text
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters in plain text
        if (char == " "):
            result += " "
        elif (char.isupper()):
            result += chr((ord(char) + s - 65) % 26 + 65)
        # Encrypt lowercase characters in plain text
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result


def decodeCaesar(text, s):
    s = 26-s
    result = ""
    # transverse the plain text
    for i in range(len(text)):
        char = text[i]
        # Encrypt uppercase characters in plain text
        if (char == " "):
            result += " "
        elif (char.isupper()):
            result += chr((ord(char) + s - 65) % 26 + 65)
        # Encrypt lowercase characters in plain text
        else:
            result += chr((ord(char) + s - 97) % 26 + 97)
    return result


# Vigenère cipher

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def translateMessage(key, message, mode):
    translated = []  # stores the encrypted/decrypted message string
    keyIndex = 0
    key = key.upper()

    for symbol in message:
        num = LETTERS.find(symbol.upper())
        if num != -1:
            if mode == 'encrypt':
                num += LETTERS.find(key[keyIndex])

            elif mode == 'decrypt':
                num -= LETTERS.find(key[keyIndex])

            num %= len(LETTERS)

            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
            keyIndex += 1

            if keyIndex == len(key):
                keyIndex = 0
        else:
            translated.append(symbol)
    return ''.join(translated)



def encrypt():
    with open(filename) as file:
        data = file.read()
        if cipherVar.get() == "Caesar":
            with open(filename, "w") as file:
                encoded = encodeCaesar(data, int(key))
                file.write(encoded)
        else:
            with open(filename, "w") as file:
                file.write(translateMessage(key, data, "encrypt"))

    file.close()

def decrypt():
    with open(filename) as file:
        data = file.read()
        if cipherVar.get() == "Vigenere":
            with open(filename, "w") as file:
                file.write(translateMessage(key, data, "decrypt"))
        else:
            with open(filename, "w") as file:
                file.write(decodeCaesar(data, int(key)))
    file.close()

encryptBtn = Button(root, text="Encrypt", font=40, command=encrypt)
encryptBtn.grid(row=4, column=1)
decryptBtn = Button(root, text="Decrypt", font=40, command=decrypt)
decryptBtn.grid(row=4, column=2)

root.mainloop()
