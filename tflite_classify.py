
#!/usr/bin/env python3

import warnings
import tflite_runtime.interpreter as tflite
from tflite_runtime.interpreter import Interpreter

import os
import cv2
import numpy
import string
import random
import argparse
import csv

def decode(characters, y):
    y = numpy.argmax(numpy.array(y), axis=2)[:,0]
    return ''.join([characters[x] for x in y])

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-name', help='Model name to use for classification', type=str)
    parser.add_argument('--captcha-dir', help='Where to read the captchas to break', type=str)
    parser.add_argument('--output', help='File where the classifications should be saved', type=str)
    parser.add_argument('--symbols', help='File with the symbols to use in captchas', type=str)
    args = parser.parse_args()

    if args.model_name is None:
        print("Please specify the CNN model to use")
        exit(1)

    if args.captcha_dir is None:
        print("Please specify the directory with captchas to break")
        exit(1)

    if args.output is None:
        print("Please specify the path to the output file")
        exit(1)

    if args.symbols is None:
        print("Please specify the captcha symbols file")
        exit(1)

    symbols_file = open(args.symbols, 'r')
    captcha_symbols = symbols_file.readline().strip()
    symbols_file.close()

    symbols_list = list(captcha_symbols)
    arr = []

    print("Classifying captchas with symbol set {" + captcha_symbols + "}")

    with open(args.output, 'w', newline='') as op_csv:
        output_csv_writer = csv.writer(op_csv, delimiter=' ')
        output_csv_writer.writerow(['vnagaraj'])

        interpreter = Interpreter(model_path=args.model_name)
        interpreter.allocate_tensors()

        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()                                 

        for x in os.listdir(args.captcha_dir):
            # load image and preprocess it
            raw_data = cv2.imread(os.path.join(args.captcha_dir, x))
            rgb_data = cv2.cvtColor(raw_data, cv2.COLOR_BGR2RGB)
            image = numpy.array(rgb_data) / 255.0
            (c, h, w) = image.shape
            image = image.reshape([-1, c, h, w])
                

            input_shape = input_details[0]['shape']
            input_data = numpy.array(image, dtype=numpy.float32)
            interpreter.set_tensor(input_details[0]['index'], input_data)

            interpreter.invoke()

            captcha_op = ''
            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            for i in range(5):   
                output_data = interpreter.get_tensor(output_details[i]['index'])
                od = numpy.squeeze(output_data)
                # labels = load_labels('symbols.txt')
                od_char=numpy.argmax(od)
                captcha_op = captcha_op + symbols_list[od_char]

            print(x+ "," + captcha_op)
            arr.append(x+','+captcha_op)

        arr = sorted(arr, key=str)
        for a in arr:
            output_csv_writer.writerow([a])


if __name__ == '__main__':
    main()
