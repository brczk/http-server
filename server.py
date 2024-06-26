import socket

class WebServer:
    router = {
        'GET' : {}
    }

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port

    def route(self, resource, methods = ['GET']):
        def decorator(f):
            for method in methods:
                self.router[method][resource] = f
        return decorator
    
    def respond(self, method, resource):
        status = 'HTTP/1.1 200 OK'
        body = self.router[method][resource]()
        return f'{status}\n\n{body}'.encode()
        
    
    def serve(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                c = s.accept()[0]
                request = c.recv(1024).decode().split('\r\n')
                if request:
                    method = request[0].split(' ')[0]
                    if method in self.router.keys():
                        resource = request[0].split(' ')[1]
                        try:
                            c.sendall(self.respond(method = method,  resource = resource))
                        except KeyError:
                            c.sendall(b'HTTP/1.1 404 Not Found')
                        finally:
                            c.close()
                    else:
                        c.sendall(b'HTTP/1.1 405 Method Not Allowed')
                    c.close()
