from django.test import TestCase
from .models import Video


class VideoTestCase(TestCase):
    def testVideo(self):
        video = Video(video = "MyVideo.mp4", name = "My name", description = "my Description")
        self.assertEqual(video.video, "MyVideo.mp4")
        self.assertEqual(video.name, "My name")
        self.assertEqual(video.description, "my Description")



