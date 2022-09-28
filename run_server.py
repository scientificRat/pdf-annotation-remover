import uvicorn

LISTEN_ADDRESS = '0.0.0.0'
SERVER_PORT = 9989
if __name__ == '__main__':
    uvicorn.run("main:app", host=LISTEN_ADDRESS, port=SERVER_PORT, log_level="info")
