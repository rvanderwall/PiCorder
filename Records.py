from Assets import Assets


class Record:
    def __init__(self, image):
        self.image = image
        self.text = ""


class Records:
    """
    Archival records, video, images, and text
    """
    def __init__(self, assets: Assets):
        self.edith_record = Record(assets.edith)
        self.edith_record.text = "Edith Keeler. social worker."
        self.spock_record = Record(assets.spock)
        self.spock_record.text = "Spock. Scienct officer, Vulcan"

    def get_current_record(self):
        return self.spock_record
