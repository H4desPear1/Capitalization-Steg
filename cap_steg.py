import re
import string

def hide_flag(binary_string, contents, output_path):
    contents_char = list(contents)
    binary_string_char = list(binary_string)

    #Encode the flag in the text, ignore punctuation and spaces
    j = 0
    for i in range(len(contents_char)):
        if j >= len(binary_string_char):
            break
        if contents_char[i] != " " and contents_char[i] not in string.punctuation:
            if binary_string_char[j] == "1":
                contents_char[i] = contents_char[i].upper()
            j += 1
    
    #Put the ciphertext in a file
    output_text = "".join(contents_char)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_text)

def find_flag(ciphertext):
    ciphertext_char = list(ciphertext)
    bin_char = []

    #Iterate through the ciphertext and find the flag
    #End the loop on the null terminator
    end_count = 0
    count = 0
    for ch in ciphertext_char:
        if count%8 == 0:
            end_count = 0
        if end_count == 8:
            bin_char = bin_char[:-8]
            break
        if ch != " " and ch not in string.punctuation:
            if ch.isupper():
                bin_char.append('1')
                count += 1
            else:
                bin_char.append('0')
                end_count += 1
                count +=1
    
    #Take the binary list and make it text
    bin_string = "".join(bin_char)
    split = [bin_string[i:i+8] for i in range(0, len(bin_string), 8)]
    flag = "".join([chr(int(b, 2)) for b in split])

    print("The flag is:", flag)


def encode():
    flag = input("What is the flag?\n")
    spot = input("What is the filepath for the hiding spot?\n")
    output_path = "cap_ciphertext.txt"

    #Turn the flag into binary and count the characters
    encoded = flag.encode("utf-8")
    binary_string = "".join([format(byte, "08b") for byte in encoded])
    count = len(binary_string)

    with open(spot, "r", encoding="utf-8") as f:
        contents = f.read().lower()
    
    #Check that the text can hold the flag
    if len(re.sub(r"\s", "", contents)) < count:
        raise (ValueError ("The text is too short to hide the flag"))
    
    #Encode the flag
    try :
        hide_flag(binary_string, contents, output_path)
    except Exception as e:
        print(f"Error: {e}")
        return
    
    print("The flag has been hidden in", output_path)
    
def decode():
    ciphertext_path = input("What is the filepath for the ciphertext?\n")

    #Open the ciphertext file and put it in a string
    with open(ciphertext_path, "r", encoding="utf-8") as f:
        ciphertext = f.read()
    
    #Decode the flag
    try :
        find_flag(ciphertext)
    except Exception as e:
        print(f"Error: {e}")
        return
    
def main():
    choice = input("Encode or Decode\n")

    #Check if the user wants to Encode or Decode
    if choice == "Encode":
        encode()
    elif choice == "Decode":
        decode()
    else:
        print("Choose one of the choices")
        main()

if __name__ == "__main__" :
    main()