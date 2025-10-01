from PIL import Image
import numpy as np

def get_coords(letter):
    mat = [["a", "b", "c", "d", "e"], ["f", "g", "h", "i", "j"], ["k", "l", "m", "n", "o"], ["p", "q", "r", "s", "t"], ["u", "v", "w", "x", "y"]]
    row = -1
    col = -1

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if letter == mat[i][j]:
                row = i
                col = j
    if row == -1 or col == -1:
        print("Your flag include a character that is not supported")
        exit

    return(row, col)

def return_letter(row, col):
    mat = [["a", "b", "c", "d", "e"], ["f", "g", "h", "i", "j"], ["k", "l", "m", "n", "o"], ["p", "q", "r", "s", "t"], ["u", "v", "w", "x", "y"]]
    if 0 <= row < 5 and 0 <= col < 5:
        return mat[row][col]
    raise ValueError(f"Invalid coordinates: ({row}, {col})")


def hide_flag(image_path, flag, output_path):
    img = Image.open(image_path).convert('RGB')
    pixels = np.array(img)
    height, width, _ = pixels.shape

    #Check flag size
    flag_length = len(flag)
    if flag_length*5 >= height or flag_length*5 >= width:
        raise (ValueError("The image is too small"))
    
    #Encode flag
    char_count = 0
    row_loc = 0
    col_loc = 0
    char_flag = list(flag.replace(" ", ""))
    for i in range(len(char_flag)):
        pix_row, pix_col = get_coords(char_flag[i])
        if char_count != 0:
            pix_row = pix_row + 1
            pix_col = pix_col + 1
        char_count = char_count +1

        row_loc = row_loc + pix_row
        col_loc = col_loc + pix_col

        r, g, b = pixels[row_loc, col_loc]
        pixels[row_loc, col_loc] = (255-r, 255-g, 255-b)
    
    output_image = Image.fromarray(pixels)
    output_image.save(output_path)

def decode():
    print("What file should I decode?")
    decode_image = input()
    img = Image.open(decode_image).convert('RGB')
    pixels = np.array(img)
    height, width, _ = pixels.shape

    char_count = 0
    row_loc = 0
    col_loc = 0
    flag = ""

    #Decode Image
    for i in range(height):
        for j in range(width):
            if np.array_equal(pixels[i, j], [255, 255, 255]):
                if char_count == 0:
                    pix_row = i
                    pix_col = j
                else:
                    pix_row = i - row_loc - 1
                    pix_col = j - col_loc - 1
                
                letter = return_letter(pix_row, pix_col)
                flag += letter

                row_loc = i
                col_loc = j
                char_count += 1

    print("The flag is: " + flag)

def encode():
    image_path = "MSB3.png"
    print("What is the flag?")
    flag = input()
    output_path = "hidden.png"

    try:
        hide_flag(image_path, flag, output_path)
    except Exception as e:
        print(f"Error: {e}")
        return

    print("The flag has been hidden in: " + output_path)

def main():
    print("Encode or Decode?")

    choice = input()
    if choice == "Encode":
        encode()
    if choice == "Decode":
        decode()


if __name__ == "__main__":
    main()
