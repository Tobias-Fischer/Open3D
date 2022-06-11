# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2018-2021 www.open3d.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
# ----------------------------------------------------------------------------

import os, sys
import open3d as o3d
import numpy as np
import glob

from config import ConfigParser
from common import load_rgbd_file_names, load_depth_file_names, save_poses, load_intrinsic, load_extrinsics, get_default_dataset


def split_fragments(config):
    depth_file_names, color_file_names = load_rgbd_file_names(config)

    os.makedirs(os.path.join(config.path_dataset, 'fragments'), exist_ok=True)

    frag_id = 0
    for i in range(0, len(depth_file_names), config.fragment_size):
        start = i
        end = min(i + config.fragment_size, len(depth_file_names))

        np.savetxt(os.path.join(config.path_dataset, 'fragments',
                                'fragment_{:03d}_colors.txt'.format(frag_id)),
                   color_file_names[start:end],
                   fmt='%s',
                   delimiter='')
        np.savetxt(os.path.join(config.path_dataset, 'fragments',
                                'fragment_{:03d}_depths.txt'.format(frag_id)),
                   depth_file_names[start:end],
                   fmt='%s',
                   delimiter='')

        frag_id += 1


def load_fragments(config):
    color_list_fnames = sorted(
        glob.glob(os.path.join(config.path_dataset, 'fragments',
                               '*_colors.txt')))
    depth_list_fnames = sorted(
        glob.glob(os.path.join(config.path_dataset, 'fragments',
                               '*_depths.txt')))

    color_lists = [
        np.loadtxt(color_list_fname, dtype=str)
        for color_list_fname in color_list_fnames
    ]
    depth_lists = [
        np.loadtxt(depth_list_fname, dtype=str)
        for depth_list_fname in depth_list_fnames
    ]

    return depth_lists, color_lists


if __name__ == '__main__':
    parser = ConfigParser()
    parser.add(
        '--config',
        is_config_file=True,
        help='YAML config file path. Please refer to default_config.yml as a '
        'reference. It overrides the default config file, but will be '
        'overridden by other command line inputs.')
    parser.add('--default_dataset',
               help='Default dataset is used when config file is not provided. '
               'Default dataset may be selected from the following options: '
               '[lounge, jack_jack]',
               default='lounge')
    config = parser.get_config()

    split_fragments(config)
    depth_lists, color_lists = load_fragments(config)
