import ipfshttpclient

c = ipfshttpclient.connect()
result = c.add('hello.txt')
print(result)
