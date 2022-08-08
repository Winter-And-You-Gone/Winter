from app import app
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(1)
# from app import manger


if __name__ == '__main__':
    app.run(port=9999, debug=True)  # manger.run()
