from piwho import recognition, config

from jarpis.recognition import audiofile_path


def get_current_speaker():
    recog = recognition.SpeakerRecognizer(audiofile_path + 'speakerIdentifierFiles/')
    names = recog.identify_speaker()
    name = names[0]

    try:
        with open(config.SPEAKER_DB, 'r') as reader:
            speakers = [row.split(',')[:2] for row in reader]

        for speaker in speakers:
            if speaker[1] == name:
                return speaker
            else:
                return ("anonymus", None)
    except IOError as err:
        print("IOError: {0}").format(err)

