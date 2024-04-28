import asyncio
import threading
import os
import PupilTracker


async def wait_for_csv():
    while not os.path.exists("Jake/Final/output.csv"):
        await asyncio.sleep(1)

async def main():

    # create object
    pt = PupilTracker.PupilTracker()

    # live run
    #pt.runLive('Jake/Final/output.csv')

    # record video
    #pt.record('Jake/Final/test.mp4')

    # process recording
    pt.runVideo(video = 'GUI/videoTests/longTest.mp4', threshold = 115, output = 'Jake/Final/output.csv')

    #await wait_for_csv("Jake/Final/output.csv")
    #threading.Thread(target=sftp.main).start()


if __name__ == "__main__":
    asyncio.run(main())
    