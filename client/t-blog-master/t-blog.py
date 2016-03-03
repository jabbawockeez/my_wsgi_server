# coding=utf8
import sys
import getopt
import urllib
import hashlib

POST_URL = "http://localhost:8888/admin/remote"
SERVER_PASS = "pengfei1018"


def main(argv):
    try:
        opts, args = getopt.getopt(
            argv,
            "f:c:t:",
            ["file=", "category=", "tag="])
    except getopt.GetoptError:
        print "参数错误"
        sys.exit(2)
    options = dict(opts)
    data_dict = {
        "password": hashlib.md5(SERVER_PASS).hexdigest()
    }
    file_content = None
    try:
        md_file = open(options["-f"])
        file_content = md_file.read()
    except:
        print "文件打开错误"
        sys.exit(2)
    finally:
        md_file.close()
    data_dict["content"] = file_content
    if "-t" in options:
        data_dict["tags"] = options["-t"]
    if "-c" in options:
        data_dict["category"] = options["-c"]
    response = urllib.urlopen(POST_URL, urllib.urlencode(data_dict))
    print urllib.urlencode(data_dict)
    if response.getcode() != 200:
        print "Failed, server returns " + str(response.getcode())
    else:
        print "Publish Success!"

if __name__ == "__main__":
    main(sys.argv[1:])
