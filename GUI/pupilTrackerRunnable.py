import asyncio
import threading
import os
import PupilTracker
import sftp


async def wait_for_csv():
    while not os.path.exists('C:/Users/jarki/Desktop/output.csv'):
        await asyncio.sleep(30)

async def main():

    output_path = 'C:/Users/jarki/Desktop/output.csv'

    # create object
    pt = PupilTracker.PupilTracker()

    # live run
    #pt.runLive('Jake/Final/output.csv')

    # record video
    #pt.record('Jake/Final/test.mp4')

    # process recording
    pt.runVideo(video = 'GUI/videoTests/longTest.mp4', threshold = 115, output=output_path)

    await wait_for_csv()
    threading.Thread(target=sftp.main).start()
    print("Sending output.csv")


if __name__ == "__main__":
    asyncio.run(main())
    