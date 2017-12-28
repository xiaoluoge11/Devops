# coding=utf-8
import socket
import time,threading

html = """HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nConnection: close\r\nContent-Length: """
html404 = """HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: 13\r\n\r\n<h1>404 </h1>"""


def run(client,address):
        read_data = client.recv(10000)
        print read_data
        try:
            pic_name = read_data.split(" ")[1][1:]
            print pic_name
            with file(pic_name) as f:
                pic_content = f.read()
                length = len(pic_content)
                html_resp = html
                html_resp += "%d\r\n\r\n" % (length)
                print html_resp
                html_resp += pic_content
        except:
            print "404 occur"
            html_resp = html404

        while len(html_resp) > 0:
            sent_cnt = conn.send(html_resp)
            print "sent:", sent_cnt
            html_resp = html_resp[sent_cnt:]
        conn.close()


if __name__ == "__main__":
    listen_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    listen_fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_fd.bind(("0.0.0.0", 9000))
    listen_fd.listen(10)
    while True:
        conn, addr = listen_fd.accept()
        thread = threading.Thread(target=run, args=(conn, addr))
        thread.start()
