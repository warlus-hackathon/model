import os
import time

#from recognizer.services import download, poll, recognize, upload
#from recognizer.utils import update_image_field


def main():
    while True:
        image = poll.get_next_task()
        if image:
            filename = image.dict()['name']
            output_filename = filename.split('.')[0] + '_yolov3.jpg'
            was_recognized = -1
            recognized_image = update_image_field(image=image,
                                                  field='was_recognized',
                                                  new_value=was_recognized
                                                  )
            try:
                download.download_image(filename)
                recognized_image = recognize.recognize_image(image)
                was_recognized = 1
                upload.upload_image(output_filename)
                os.remove(f'recognizer/file_storage/{filename}')
                os.remove(f'recognizer/file_storage/{output_filename}')
            finally:
                recognized_image = update_image_field(image=recognized_image,
                                                      field='was_recognized',
                                                      new_value=was_recognized
                                                      )
                poll.post_answer(recognized_image)
        time.sleep(1)


if __name__ == "__main__":
    #main()
    from recognizer.handler import watcher
