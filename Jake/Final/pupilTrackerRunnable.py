import PupilTracker

def main():

    # create object
    pt = PupilTracker.PupilTracker()

    # live run
    #pt.runLive('Jake/Final/output.csv')

    # record video
    #pt.record('Jake/Final/test.mp4')

    # process recording
    pt.runVideo(video = 'Jake/Final/test.mp4', threshold = 115, output = 'Jake/Final/output.csv')

if __name__ == "__main__":
    main()
    