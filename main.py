# import requests module
import requests
import re
import glob
  
class HTTPHeader:
    def __init__(self, headersRaw=""):
        self.headersRaw = headersRaw
        # the headers dictionary can be used to retreive header values using their names
        self.headersDict = {}
        self.status = {}
        self.error = ""

    def setHeaders(self, headersRaw):
        self.headersRaw = headersRaw


    #check the correctness of the status line using regex and parse if it is valid
    def checkStatusLine(self,line):
        pattern = re.compile(r"HTTP/([0-9]+\.[0-9]+) ([0-9][0-9][0-9]) ([a-zA-Z0-9 ]+)")
        match=pattern.match(line)
        match = pattern.match(line)
        if match:
            self.status = {
                "http_version": match.group(1),
                "status_code": match.group(2),
                "reason": match.group(3),
            }
        return match

    def is_ascii(self,s):
        return all(ord(c) < 128 for c in s)

    def checkHeaderName(self,headerName):
        pattern = re.compile(r"^[a-zA-Z0-9-]+$")
        return pattern.match(headerName)
    
    def parse(self):
        # headers should end in \r\n
        # assert (self.headersRaw[-2:]=="\r\n"), "Invalid header, header should end in \\r\\n"
        if not self.headersRaw[-2:] == "\r\n":
            self.error = "Invalid header, header should end in \\r\\n"
            return False

        headers = self.headersRaw.strip().split("\r\n")

        # headers should be at least one line
        # assert(len(headers)>0), "Invalid header, header should be at least one line"
        if not len(headers) > 0:
            self.error = "Invalid header, header should be at least one line"
            return False

        statusLine = headers[0]

        # checking status line format using regex
        # assert (self.checkStatusLine(statusLine)), "Invalid status line"
        if not self.checkStatusLine(statusLine):
            self.error = "Invalid status line"
            return False

        headers = headers[1:]
        for header in headers:
            valid = True
            header = header.split(":")

            name = header[0]
            value = "".join(header[1:]).strip()

            # invalid header line if does not have a key-value pair
            if len(header) < 2:
                valid = False

            # check if key is duplicate
            if name in self.headersDict:
                self.error = "Duplicate header key"
                return False

            # check the format of the name (key) using regex
            if not self.checkHeaderName(name):
                valid = False

            # value should be ascii
            if not self.is_ascii(value):
                valid = False

            self.headersDict[name] = {"valid": valid}
            if valid:
                self.headersDict[name]["value"] = value

        
    def countValidInvalid(self):
        if not len(self.headersDict):
            return 0,0
        valid = 0
        for key in self.headersDict:
            if self.headersDict[key]["valid"]:
                valid += 1
        return valid, len(self.headersDict) - valid
           
    def output(self):
        if self.error:
            return self.error
        valid,invalid=self.countValidInvalid()
        out = "HTTP version: " + self.status["http_version"] + "\n"
        out += "Status: " + self.status["status_code"] + "\n"
        out += "Number of valid headers: " + str(valid) + "\n"
        out += "Number of invalid headers: " + str(invalid) + "\n"
        return out
    
    # return the headers dictionary
    def getHeaders(self):
        if self.error:
            return False
        return self.headersDict
