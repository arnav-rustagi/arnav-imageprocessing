import cv2
import numpy as np
import types


def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image, secret_data):
    # read the image
    # image = cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image

def decode(image):
    print("[+] Decoding...")
    # read the image
    # image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

def encode_text():
    image_name = input("Enter image name (with extension): ")
    image = cv2.imread(image_name)

    print("The shape of image is: ",image.shape)
    print("The original image is as shown below: ")
    resized_image = cv2.resize(image,(500,500))
    cv2.imshow("",resized_image)
    cv2.waitKey(0)

    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data cannot be empty')

    filename = input("Enter the name of new encoded image (with extension): ")
    encoded_image = encode(image,data)
    cv2.imwrite(filename, encoded_image)
    print('Data Encoded')

def decode_text():
    image_name = input("Enter steganographed image name (with extension): ")
    image = cv2.imread(image_name)

    resized_image = cv2.resize(image,(500,500))
    cv2.imshow("",resized_image)
    cv2.waitKey(0)

    text = decode(image)
    return text

def Steganography():
    a = input("Image steganograpphy \n Press 1 for encoding the data in image \n Press 2 for decoding the data from image \n Your Input: ")
    userinput = int(a)
    if (userinput == 1):
        print("\n Encoding...")
        encode_text()

    elif (userinput == 2):
        print("\n Decoding...")
        print("Decoded data: ",decode_text())

Steganography()
