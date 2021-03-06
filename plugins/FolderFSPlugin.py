import argparse
import os
from FSPlugin import FSPlugin

class FolderFSPlugin(FSPlugin):
    arg_name = 'folder'

    @classmethod
    def addArguments(cls, parser):
        parser.add_argument('--%s' % cls.arg_name, dest='%s_dirs' % cls.arg_name, nargs='+', help='Use the given folder')
    
    @classmethod
    def createFromArgs(cls, args):
        dirs = getattr(args, '%s_dirs' % cls.arg_name)
        folder_plugins = []

        if dirs != None:
            for d in dirs:
                folder_plugins.append(cls(d))
        
        return folder_plugins

    def __init__(self, folder_dir):
        super(FolderFSPlugin, self).__init__()
        self.source_dir = folder_dir
        self.open_files = dict()
    
    def getAllFiles(self):
        for f in os.listdir(self.source_dir):
            yield '/' + f
    
    def containsFile(self, path):
        return os.path.exists(self.source_dir + path)
    
    def readdir(self, path):
        for filename in os.listdir(self.source_dir + path):
            yield filename

    # TODO: actually check
    def canStoreFile(self, f):
        return True
    
    def createNewFile(self, name, mode, dev):
        f = open(self.source_dir + '/' + name, 'wb')
        f.close()
    
    def getAttributes(self, path):
        st = os.stat(self.source_dir + path)
        return st
    
    def changeMode(self, path, mode):
        os.chmod(self.source_dir + path, mode)
    
    def changeOwn(self, path, uid, gid):
        os.chown(self.source_dir + path, uid, gid)
    
    def fsync(self, path):
        os.fsync(self.source_dir + path)
    
    def truncateFile(self, path, size):
        os.truncate(self.source_dir + path, size)
    
    def deleteFile(self, path):
        os.remove(self.source_dir + path)
    
    def setTimes(self, path, times):
        os.utime(self.source_dir + path, times)

    def open(self, path, flags):
        self.open_files[path] = os.open(self.source_dir + path, flags)

    def read(self, path, length, offset):
        os.lseek(self.open_files[path], offset, os.SEEK_SET)
        return os.read(self.open_files[path], length)

    def write(self, path, buf, offset):
        os.lseek(self.open_files[path], offset, os.SEEK_SET)
        os.write(self.open_files[path], buf)
    
    def release(self, path, flags):
        f = self.open_files[path]
        os.close(f)
        del self.open_files[path]

    def closedFile(self, path):
        os.close(path)
