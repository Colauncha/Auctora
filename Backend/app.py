#!/usr/bin/env python3
import sys
import uvicorn

from server import create_app, create_admin


app = create_app()


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'createadmin':
            admin = create_admin()
            print(admin)
        config = uvicorn.Config(app, port=8000, log_level='info', reload=True)
        server = uvicorn.Server(config)
        server.run()
    except KeyboardInterrupt:
        exit()
    
