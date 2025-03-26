#!/usr/bin/env python3
"""
Entrypoint for the Receipt Processor application.
"""

import uvicorn

from receiptprocessor import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)