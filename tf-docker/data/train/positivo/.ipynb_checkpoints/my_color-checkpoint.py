import numpy as np
import cv2
import os
import argparse
from glob import glob

def read_file(source_path, target_path):
    s = cv2.imread(source_path)
    s = cv2.cvtColor(s, cv2.COLOR_BGR2LAB)
    t = cv2.imread(target_path)
    t = cv2.cvtColor(t, cv2.COLOR_BGR2LAB)
    return s, t

def get_mean_and_std(x):
    x_mean, x_std = cv2.meanStdDev(x)
    x_mean = np.hstack(np.around(x_mean, 2))
    x_std = np.hstack(np.around(x_std, 2))
    return x_mean, x_std

def color_transfer(source, target):
    s_mean, s_std = get_mean_and_std(source)
    t_mean, t_std = get_mean_and_std(target)

    height, width, channel = source.shape
    for i in range(0, height):
        for j in range(0, width):
            for k in range(0, channel):
                x = source[i, j, k]
                x = ((x - s_mean[k]) * (t_std[k] / s_std[k])) + t_mean[k]
                x = round(x)
                x = 0 if x < 0 else x
                x = 255 if x > 255 else x
                source[i, j, k] = x

    source = cv2.cvtColor(source, cv2.COLOR_LAB2BGR)
    return source

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target", required=True, help="Caminho para a imagem target (alvo)")
    args = vars(ap.parse_args())

    target = cv2.imread(args["target"])

    if target is None:
        print("Erro ao carregar a imagem target.")
        sys.exit(0)

    if not os.path.exists("resultados"):
        os.makedirs("resultados")

    source_images = glob("source/*.jpg")

    for img_path in source_images:
        source = cv2.imread(img_path)

        if source is None:
            print(f"Erro ao carregar a imagem {img_path}")
            continue

        transferred = color_transfer(source, target)

        result_filename = os.path.join("resultados", os.path.basename(img_path))
        cv2.imwrite(result_filename, transferred)

if __name__ == "__main__":
    main()
