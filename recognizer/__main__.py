import time

from recognizer.services import poll, recognize


def main():
    while True:
        image = poll.get_next_task()
        if image:
            recognized_image = recognize.recognize_image(image)
            poll.post_answer(recognized_image)
        time.sleep(5)


if __name__ == "__main__":
    main()
