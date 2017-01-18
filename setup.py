#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup


def main():
    setup(
        name='scorer-sdk',
        version='0.5.0',
        description='A Software Development Kit for Scorer',
        url='https://github.com/future-standard/',
        zip_safe=False,
        packages=['scorer'],
    )


if __name__ == '__main__':
    main()
