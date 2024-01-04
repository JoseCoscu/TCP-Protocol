from trapy import listen, accept

conn = listen('127.0.0.1:8888')
accept(conn)