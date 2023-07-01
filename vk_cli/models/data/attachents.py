from dataclasses import dataclass


@dataclass
class DataAttachmentPhoto:
    type: str
    photo: 'PhotoData'


@dataclass
class DataAttachmentPost:
    type: str
    photo: 'PostData'
