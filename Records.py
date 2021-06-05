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
        self._edith_record = Record(assets.edith)
        self._edith_record.text = "Edith Keeler. social worker."
        self._spock_record = Record(assets.spock)
        self._spock_record.text = "Spock. Science officer, Vulcan"

        self._cur = self._edith_record

    def get_current_record(self):
        return self._cur

    def next_record(self):
        if self._cur == self._edith_record:
            self._cur = self._spock_record
        else:
            self._cur = self._edith_record
