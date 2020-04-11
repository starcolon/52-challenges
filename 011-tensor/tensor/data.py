import pandas as pd
import numpy as np
import cv2
import argparse
import sys
import os

from typing import Tuple
from termcolor import colored

def gen_images(n: int, dim: Tuple[int,int], noise_level: float, f): 
  """
  Generate an image dataset
  Args:
    n (int):              Size of the dataset
    dim (int,int):        Dimension of the image, height x weight
    noise_level (double): Ratio of noise (0-1)
    f (function):         Function to apply with generated image
  """
  h,w = dim
  num_noise_pixels = int(noise_level * w * h)

  def add_noise(im):
    for i in num_noise_pixels:
      x = int(np.random.choice(range(w)))
      y = int(np.random.choice(range(h)))
      im[y,x] = 255
    return im

  dset = []
  for i in range(n):
    # Generate background
    im = np.ones(dim, cv2.uint8) * int(np.random.choice([
      25, 50, 100, 128, 150, 200, 250
      ]))
    # Generate crosshair
    x = np.random.choice(range(w))
    y = np.random.choice(range(h))
    cv2.line(im, (0,y), (w,y), (0,0,0), 1)
    cv2.line(im, (x,h), (x,0), (0,0,0), 1)
    im = add_noise(im)
    hashstr = joblib.hash(im)
    dset.append((hashstr,im))
    if f is not None:
      f(hashstr, im)
  return dset

def gen_dataset(n: int, dim: Tuple[int,int], f):
  """
  Generate the whole dataset consisting 10 portions
  1. Without noise
  2. With 5% noise
  3. With 15% noise
  4. With 50% noise
  5. With random noise between 15~50%
  """
  indices = range(n)

  # Following is taken from https://stackoverflow.com/a/2130035/4154262
  def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

  portions = chunkIt(indices, 5)
  noises = [0, 0.05, 0.15, 0.5, np.random.choice(np.arange(0.15,0.5,0.1))]

  rows = []
  i = 0
  for n,p in zip(noises,portions):
    i += 1
    print("Generating images in portion #{}, noise level = {:.2f}".format(
      i, n))
    images = gen_images(len(portions), dim, n, f)
    for hashstr,im in images:
      filename = "{}.jpg".format(hashstr)
      rows.append((filename, n))
  print("Generating dataframe")
  df = pd.DataFrame(rows, columns=["filename","noise"])
  return df

def save_image(path):
  def to(hashstr, im):
    p = "{}.jpg".format(path, hashstr)
    print("... Saving image to {}".format(p))
    cv2.imwrite(p, im)
  return to

def create_dir(path):
  if not os.path.exists(path) and not os.path.isfile(path):
    print("Creating directory : {}".format(path))
    os.mkdir(path)

def commandline(n: int, dim: Tuple[int,int], noise_level: float, f):
  """
  Create an instance of argument parser
  """
  parser = argparse.ArgumentParser(description='Dataset generator')
  parser.add_argument('--saveto', dest='saveto', default='data',
    help='Path to store the output')
  parser.add_argument('--size', dest='size', default=100, type=float,
    help='Size of the dataset to generate')
  parser.add_argument('--dim', dest='dim', default=256,
    help='Dimension of the image to generate (square)')

  args = parser.parse_args()
  return args

if __name__ == '__main__':
  """
  Generate a dataset onto the specified path
  """
  cmdline = commandline()
  create_dir(cmdline.saveto)

  print(colored("Starting dataset generator", "cyan"))

  # Generate images to the specified directory
  # with csv file named "dataset.csv" inside
  dset = gen_dataset(
    cmdline.size,
    (cmdline.size, cmdline.size),
    save_image(cmdline.saveto))
  
  path_csv = os.path.join(cmdline.saveto, "dataset.csv")
  print("Saving dataframe to {}".format(path_csv))
  dset.to_csv(path_csv, sep=',', header=True)
