from tkinter import Tk, filedialog, Button, Label, Text
import cv2
import numpy as np

# Function to encode text into an image
def encode_text():
    file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("JPEG Images", "*.jpg")])
    if not file_path:
        return
    
    img = cv2.imread(file_path)
    hidden_text = text_box.get("1.0", "end-1c")
    binary_text = ''.join(format(ord(char), '08b') for char in hidden_text)
    binary_text += '1111111111111110'  # 16-bit Delimiter to mark end of message
    
    data_index = 0
    for row in img:
        for pixel in row:
            for channel in range(3):
                if data_index < len(binary_text):
                    pixel[channel] = (pixel[channel] & ~1) | int(binary_text[data_index])
                    data_index += 1
    
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Images", "*.png")])
    if save_path:
        cv2.imwrite(save_path, img)
        status_label.config(text="Image saved successfully!", fg="green")

# Function to decode text from an image
def decode_text():
    file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("JPEG Images", "*.jpg")])
    if not file_path:
        return
    
    img = cv2.imread(file_path)
    binary_text = ""
    
    for row in img:
        for pixel in row:
            for channel in range(3):
                binary_text += str(pixel[channel] & 1)
    
    # Stop extracting when the delimiter is found
    delimiter = "1111111111111110"
    end_index = binary_text.find(delimiter)
    if end_index != -1:
        binary_text = binary_text[:end_index]  # Remove anything after the delimiter

    # Convert binary to text
    extracted_text = "".join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))

    text_box.delete("1.0", "end")
    text_box.insert("1.0", extracted_text)

# GUI Setup
root = Tk()
root.title("Steganography Tool")
root.geometry("400x300")

Label(root, text="Enter text to hide:").pack()
text_box = Text(root, height=5, width=40)
text_box.pack()

Button(root, text="Encode Text into Image", command=encode_text).pack()
Button(root, text="Decode Text from Image", command=decode_text).pack()

status_label = Label(root, text="", fg="green")
status_label.pack()

root.mainloop()
