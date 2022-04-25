test=[0]*4
test[0]="HTTP/1.0 200 OK\r\ncache-control: public\r\ncontent-length: 0\r\ncontent-type: image/svg+xml\r\ndate: Tue, 22 Jun 2021 22:24:42 GMT\r\n"
test[1]="HTTP/1.1 302 Found\r\ncache-control: public\r\nTransfer-encoding: chunked\r\ninvalid_header\r\ndate: Tue, 22 Jun 2021 22:24:42 GMT\r\n"
test[2]="Header1: value1\r\ndate: Tue, 22 Jun 2021 22:24:42 GMT\r\ncontent-length: 1337\r\n"
test[3]="HTTP/1.0 200 OK\r\ncache-control: public\r\ncontent-length: 0\r\ncontent-type: image/svg+xml\r\ncontent-length: 1\r\ndate: Tue, 22 Jun 2021 22:24:42 GMT\r\n"

exp=[0]*4
exp[0]="HTTP version: 1.0\nStatus: 200\nNumber of valid headers: 4\nNumber of invalid headers: 0\n"
exp[1]="HTTP version: 1.1\nStatus: 302\nNumber of valid headers: 3\nNumber of invalid headers: 1\n"
exp[2]="Invalid status line";
exp[3]="Duplicate header key";

expDict=[0]*4
expDict[0]={'cache-control': {'valid': True, 'value': 'public'}, 'content-length': {'valid': True, 'value': '0'}, 'content-type': {'valid': True, 'value': 'image/svg+xml'}, 'date': {'valid': True, 'value': 'Tue, 22 Jun 2021 222442 GMT'}}
expDict[1]={'cache-control': {'valid': True, 'value': 'public'}, 'Transfer-encoding': {'valid': True, 'value': 'chunked'}, 'invalid_header': {'valid': False}, 'date': {'valid': True, 'value': 'Tue, 22 Jun 2021 222442 GMT'}}
expDict[2]=False
expDict[3]=False
