#!/usr/bin/env python3
# coding=utf-8

import os,sys
from xml.etree import ElementTree
from PIL import Image

def tree_to_dict(tree):
    d = {}
    for index, item in enumerate(tree):
        if item.tag == 'key':
            if tree[index+1].tag == 'string':
                d[item.text] = tree[index + 1].text
            elif tree[index + 1].tag == 'true':
                d[item.text] = True
            elif tree[index + 1].tag == 'false':
                d[item.text] = False
            elif tree[index+1].tag == 'dict':
                d[item.text] = tree_to_dict(tree[index+1])
    return d

def gen_png_from_plist(plist_filename, png_filename):
    file_path = plist_filename.replace('.plist', '')
    big_image = Image.open(png_filename)
    root = ElementTree.fromstring(open(plist_filename, 'r').read())
    plist_dict = tree_to_dict(root[0])
    to_list = lambda x: x.replace('{','').replace('}','').split(',')
    for k,v in plist_dict['frames'].items():
        rectlist = to_list(v['frame'])
        width = int( rectlist[3] if v['rotated'] else rectlist[2] )
        height = int( rectlist[2] if v['rotated'] else rectlist[3] )
        box=( 
            int(rectlist[0]),
            int(rectlist[1]),
            int(rectlist[0]) + width,
            int(rectlist[1]) + height
            )
        sizelist = [ int(x) for x in to_list(v['sourceSize'])]
        rect_on_big = big_image.crop(box)

        if v['rotated']:
            if k == "hill5_3.png":
                rect_on_big.show()
            fuck_image = Image.new('RGBA', [max(width, height), max(width, height)], (0,0,0,0))
            fuck_image.paste(rect_on_big, (0, 0), mask = 0)
            if k == "hill5_3.png":
                fuck_image.show()
            fuck_image = fuck_image.rotate(90)
            rect_on_big = fuck_image.crop((0, max(width, height) - width, height, max(width, height)))
            if k == "hill5_3.png":
                rect_on_big.show()
                fuck_image.show()


        result_image = Image.new('RGBA', sizelist, (0,0,0,0))
        offset = to_list(v['sourceColorRect'])
        result_box = (
            int(offset[0]),
            int(offset[1])
            )
        # if v['rotated']:
        #     result_box=(
        #         int(( sizelist[0] - height )/2),
        #         int(( sizelist[1] - width )/2),
        #         # int(( sizelist[0] + height )/2),
        #         # int(( sizelist[1] + width )/2)
        #         )
        # else:
        #     result_box=(
        #         int(( sizelist[0] - width )/2),
        #         int(( sizelist[1] - height )/2),
        #         # int(( sizelist[0] + width )/2),
        #         # int(( sizelist[1] + height )/2)
        #         )
        if k == "hill5_3.png":
            print("===", sizelist, rect_on_big, result_box, box)
        result_image.paste(rect_on_big, result_box, mask=0)

        # if v['rotated']:
        #     result_image = result_image.rotate(90)

        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        outfile = (file_path+'/' + k).replace('gift_', '')
        print(outfile, "generated")
        result_image.save(outfile)

if __name__ == '__main__':
    filename = sys.argv[1]
    plist_filename = filename + '.plist'
    png_filename = filename + '.png'
    if (os.path.exists(plist_filename) and os.path.exists(png_filename)):
        gen_png_from_plist( plist_filename, png_filename )
    else:
        print("make sure you have boith plist and png files in the same directory")