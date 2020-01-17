import ssl
def getCliSSL(cliSock):
    return ssl.wrap_socket(cliSock,ca_certs='cert.pem',cert_reqs=ssl.CERT_REQUIRED)
    
def getSrvSSL(srvSock):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    return context.wrap_socket(srvSock, server_side=True)
