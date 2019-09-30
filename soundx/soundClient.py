import sys
import os
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocal import TBinaryProtocal
from soundx import Soundx

transport = TSocket.TSocket('localhost', 8890)

transport=TTransport.TBufferedTransport(transport)

protocol = TBinaryProtocal.TBinaryProtocol(transport)

client = Soundx.Client(protocol)

transport.open()

refAudio = "/var/data/main.mp3"
videoDir = "/var/data/"
resultFilePath = "/var/data/result.txt"

result = client.fun(refAudio, videoDir, resultFilePath)
print(result)

transport.close()
