# coding=utf-8
"""
@desc: 文件格式检测工具：主要通过文件头对常见的文件进行识别。而不是通过文件名后缀识别
@version: 1.0
@author: huangqingwei(huangqingwei@baidu.com)
@license: Copyright (c) 2016 Baidu.com,Inc. All Rights Reserved
@software: PyCharm Community Edition
@file: check_file_type.py
@time: 2017/6/3 0:27
"""
import struct
import os


def type_list():
    return {
        # "FFD8FF": "JPEG",
        # "89504E47": "PNG",
        # "47494638":"GIF",
        # "49492A00":"TIFF",
        # "424D":"BMP",
        # "41433130":"DWG",
        # "38425053":"PSD",
        # "7B5C727466":"RTF",
        # "3C3F786D6C":"XML",
        # "68746D6C3E":"HTML",
        # "44656C69766572792D646174653A":"EML",
        # "CFAD12FEC5FD746F":"DBX",
        # "2142444E":"PST",
        # "D0CF11E0":"MS",
        # "504B0304":"ZIP",
        # "526172211A": "RAR",
        # "5374616E64617264204A":"MDB",
        # "25504446":"PDF",
        # "52494646":"AVI",
        # "464C560105":"f4v",
        "464C560104": "FLV",
        # "57415645":"WAV",
        # "3026B275":"WMA",
        # "FFFB9060000F":"MP3",
        # "FFFB906C0000":"MP3",
        "FFFB90640000": "MP3",
        # "FFFBB0640000":"MP3",
        # "FFFB90040000":"MP3",
        # "FFFB90440000":"MP3",
        "FFFB92840000": "MP3",
        # "FFFBB0440000":"MP3",
        # "494433030040":"MP3",
        # "494433030080":"MP3",
        # "494433030000":"MP3",
        # "494433040000":"MP3",
        "0000001C6674": "MP4",
        "000000186674": "MP4",
        # "2321414D520A":"AMR",
        # '46575307A4': "SWF",
    }


# 字节码转16进制字符串
def bytes2hex(b_arr):
    num = len(b_arr)
    hex_str = u""
    for i in range(num):
        t = u"%x" % b_arr[i]
        if len(t) % 2:
            hex_str += u"0"
        hex_str += t
    return hex_str.upper()


def file_type(filename):
    b_infile = open(filename, 'rb')  # 必需二制字读取
    tl = type_list()
    f_type = 'unknown'

    for h_code in tl.keys():
        numOfBytes = len(h_code) / 2  # 需要读多少字节
        b_infile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
        h_bytes = struct.unpack_from("B" * numOfBytes, b_infile.read(numOfBytes))  # 一个 "B"表示一个字节
        if bytes2hex(h_bytes) == h_code:
            f_type = tl[h_code]
            break
    b_infile.close()
    return f_type


def test():
    file_name = 'E:/FOUND.000/FILE8244.CHK'
    f_type = file_type(file_name)
    print file_name, f_type


def main():
    src_dir = 'E:\FOUND.000'
    os.chdir(src_dir)
    for file_name in os.listdir(src_dir):
        if file_name.find(".CHK") == -1:
            continue
        f_type = file_type(file_name)
        if f_type == "unknown":
            continue
        print file_name, f_type
        os.rename(file_name, file_name.split(".")[0] + '.' + f_type)
        # file_name = "E:\FOUND.000\FILE0124.CHK"
        # print file_name, file_type(file_name)


if __name__ == '__main__':
    main()