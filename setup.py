# python.exe setup.py py2exe

try:
    from distutils.core import setup
    import py2exe
    import pygame
    from modulefinder import Module
    import glob
    import fnmatch
    import sys
    import os
    import shutil
    import operator
except ImportError, message:
    raise SystemExit, 'Unable to load module. %s' % message

# hack which fixes the pygame mixer and pygame font
origIsSystemDLL = py2exe.build_exe.isSystemDLL  # save the orginal before we edit it


def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ('libfreetype-6.dll',
            'libogg-0.dll', 'sdl_ttf.dll'):
        return 0
    return origIsSystemDLL(pathname)  # return the orginal function

py2exe.build_exe.isSystemDLL = isSystemDLL  # override the default function with this one

class BuildExe:

    def __init__(self):
        # Name of starting .py
        self.script = 'Gin the Bear.py'

        # Name of program
        self.project_name = 'Gin the Bear'

        # Version of program
        self.project_version = '0.1'

        # Auhor of program
        self.author_name = 'Yojka'
        self.copyright = 'Yojka (C) 2017'

        # Description
        self.project_description = 'Gin the Bear'

        # Icon file (None will use pygame default icon)
        self.icon_file = 'Gin the Bear.ico'

        # Extra files/dirs copied to game
        self.extra_datas = ['data']

        # Extra/excludes python modules
        self.extra_modules = []
        self.exclude_modules = [
            '_ssl',
            'pyreadline',
            'difflib',
            'doctest',
            'locale',
            'optparse',
            'pickle',
            'calendar',
            'email',
            'pdb',
            'unittest',
            'difflib',
            'inspect',
            'multiprocessing',
            'logging',
            'distutils',
            'ctypes',
            'xml',
            'importlib',
            'pkg_resources',
            'os2emxpath',
            'weakref',
            '_hashlib',
            'select',
            'AppKit',
            'Foundation',
            'bdb',
            'tcl',
            'pydoc',
            'compiler',
            'socket',
            'rfc822',
            'curses',
            'setuptools',
            'urllib',
            'urllib2',
            'urlparse',
            'BaseHTTPServer',
            '_LWPCookieJar',
            '_MozillaCookieJar',
            'ftplib',
            'gopherlib',
            'htmllib',
            'httplib',
            'mimetools',
            'mimetypes',
            'tty',
            'webbrowser',
            ]
        self.ignores_modules = [
            'Numeric',
            'OpenGL.GL',
            'copyreg',
            'numpy',
            'opencv',
            'pygame.examples.camera',
            'queue',
            'vidcap',
            'winreg',
            'pygame.sdlmain_osx',
            ]

        # DLL Excludes
        self.exclude_dll = ['portmidi.dll']

        # python scripts (strings) to be included, seperated by a comma
        self.extra_scripts = []

        # Zip file name (None will bundle files in exe instead of zip file)
        self.zipfile_name = None

        # Dist directory
        self.dist_dir = 'dist'

    def opj(self, *args):
        path = os.path.join(*args)
        return os.path.normpath(path)

    def find_data_files(
        self,
        srcdir,
        *wildcards,
        **kw
        ):

        # get a list of all files under the srcdir matching wildcards,
        # returned in a format to be used for install_data
        def walk_helper(arg, dirname, files):
            if '.svn' in dirname:
                return
            names = []
            (lst, wildcards) = arg
            for wc in wildcards:
                wc_name = self.opj(dirname, wc)
                for f in files:
                    filename = self.opj(dirname, f)

                    if fnmatch.fnmatch(filename, wc_name) \
                        and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append((dirname, names))

        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            os.path.walk(srcdir, walk_helper, (file_list, wildcards))
        else:
            walk_helper((file_list, wildcards), srcdir,
                        [os.path.basename(f) for f in
                        glob.glob(self.opj(srcdir, '*'))])
        return file_list

    def run(self):
        if os.path.isdir(self.dist_dir):  # Erase previous destination dir
            shutil.rmtree(self.dist_dir)

        # Use the default pygame icon, if none given

        if self.icon_file == None:
            path = os.path.split(pygame.__file__)[0]
            self.icon_file = os.path.join(path, 'pygame.ico')

        # List all data files to add
        extra_datas = []
        for data in self.extra_datas:
            if os.path.isdir(data):
                extra_datas.extend(self.find_data_files(data, '*'))
            else:
                extra_datas.append(('.', [data]))

        setup_dict = dict(
            version=self.project_version,
            description=self.project_description,
            name=self.project_name,
            author=self.author_name,
            windows=[{'script': self.script, 'icon_resources': [(0,
                     self.icon_file)], 'copyright': self.copyright}],
            options={'py2exe': {
                'ascii': True,
                'optimize': 2,
                'bundle_files': 1,
                'compressed': True,
                'excludes': self.exclude_modules,
                'packages': self.extra_modules,
                'dll_excludes': self.exclude_dll,
                'ignores': self.ignores_modules,
                'includes': self.extra_scripts,
                }},
            zipfile=self.zipfile_name,
            data_files=extra_datas,
            )

        setup(**setup_dict)
        setup(**setup_dict)  # icon bugfix

        if os.path.isdir('build'):  # Clean up build dir
            shutil.rmtree('build')


if __name__ == '__main__':
    if operator.lt(len(sys.argv), 2):
        sys.argv.append('py2exe')
    BuildExe().run()  # Run generation
    raw_input('Press any key to continue')
