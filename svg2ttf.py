import xml.etree.ElementTree as ET
import os
import logging


def svgicon2svgfont(icon_svg, out_svg):
    '''
    svg를 폰트 양식으로 변경
    '''
    logging.info(":: [system call] svgicons2svgfont %s > %s" % (icon_svg,
                                                                out_svg))
    os.system("svgicons2svgfont %s > %s" % (icon_svg, out_svg))
    logging.info(":: svgicons2svgfont done! made file [%s]" % out_svg)


def insert2target(source_svg, target_svg, new_svg):
    '''
    소스 svg의 glyph를 타겟 svg에 저장
    '''
    logging.info(":: insert2target start source: %s, target: %s, new : %s" %
                 (source_svg, target_svg, new_svg))
    ET.register_namespace('', "http://www.w3.org/2000/svg")

    # find unicode of source svg
    source = ET.parse(source_svg)
    source_root = source.getroot()
    for source_glyph in source_root.iter("{http://www.w3.org/2000/svg}glyph"):
        _ = 0
    source_unicode = source_glyph.attrib['unicode']

    # find target glyph matching source_unicode
    target = ET.parse(target_svg)
    target_root = target.getroot()
    for target_glyph in target_root.iter("{http://www.w3.org/2000/svg}glyph"):
        if 'unicode' not in target_glyph.attrib:
            continue
        if (target_glyph.attrib['unicode'] == source_unicode):
            break

    # insert source glyph to target glyph
    target_glyph.attrib = source_glyph.attrib

    # save new svg
    target.write(new_svg)
    logging.info(":: insert2target done! made file [%s]" % new_svg)


def svg2woff(svg_filname):
    '''
    최종 svg를 woff로 변환
    '''
    file_name = svg_filname.split('.')[0]
    logging.info(":: svg2woff start svg name :  [%s]" % svg2woff)
    logging.info(":: [system call] svg2ttf %s %s" % (svg_filname,
                                                     file_name + '.woff'))
    os.system("svg2ttf %s %s" % (svg_filname, file_name + '.woff'))
    logging.info(":: svg2woff done! made file  [%s]" % file_name + '.woff')


def svg2ttf(svg_filename):
    '''
    최종 svg를 ttf로 변환
    '''

    file_name = svg_filname.split('.')[0]
    logging.info(":: svg2ttf start svg name : [%s]" % svg_filename)
    logging.info(":: [system call] svg2ttf %s %s" % (svg_filname,
                                                     file_name + '.ttf'))
    os.system("svg2ttf %s %s" % (svg_filname, file_name + '.ttf'))
    logging.info(":: svg2ttf done! svg name : [%s]" % file_name + '.ttf')
