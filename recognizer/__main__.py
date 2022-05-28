import time

from recognizer.services import poll, recognize, download
from recognizer.utils import update_image_field


def main():
    while True:
        image = poll.get_next_task()
        if image:
            was_recognized = -1
            recognized_image = update_image_field(image=image,
                                                  field='was_recognized',
                                                  new_value=was_recognized
                                                  )
            try:
                download.download_image(image.dict()['name'])
                recognized_image = recognize.recognize_image(image)
                was_recognized = 1
            finally:
                recognized_image = update_image_field(image=recognized_image,
                                                      field='was_recognized',
                                                      new_value=was_recognized
                                                      )
                poll.post_answer(recognized_image)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
