# coding=utf-8

# 导入python包
import cv2
import argparse
import numpy as np


def color_transfer(source, target):
    # 从RGB空间转换到LAB空间中
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # 计算source和target图像的统计信息，即均值和方差等
    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)

    # 将目标图像的L、a、b通道划分开来并减去对应的均值
    (l, a, b) = cv2.split(target)
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar

    # 分别对L、a、b通道进行标准化操作
    l = (lStdTar / lStdSrc) * l
    a = (aStdTar / aStdSrc) * a
    b = (bStdTar / bStdSrc) * b

    # 加上均值
    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc

    # 将处理的结果限制在[0,255]的空间内
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    # 将L、a、b通道合并起来并将其转化回RGB颜色空间
    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    # 返回最终的变换结果
    return transfer


def image_stats(image):
    # 计算每一个通道的均值和方差值
    (l, a, b) = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())

    # 返回对应的统计信息
    return (lMean, lStd, aMean, aStd, bMean, bStd)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", required=True, help="Path to the source image")
    ap.add_argument("-t", "--target", required=True, help="Path to the target image")
    args = vars(ap.parse_args())
    source = cv2.imread(args["source"])
    target = cv2.imread(args["target"])
    taransform = color_transfer(source, target)
    source1 = cv2.resize(source, target.shape[0:2])
    target1 = cv2.resize(target, target.shape[0:2])
    taransform1 = cv2.resize(taransform, target.shape[0:2])
    result = np.hstack([source1, target1, taransform1])
    cv2.imwrite("transform4.png", result)
    cv2.imshow("transform", result)
    cv2.waitKey(0)

