# # import random
# from django.core.management.base import BaseCommand
# from faker import providers
# from faker import Faker
# from vitube.models import Video
#
# CATEGORY = [
#     'Bollywood'
#     'Cartoons'
#     'Song'
#     'Lyrical'
#     'Music'
#     'Interview'
#     'Educational'
#     'Inspirational'
# ]
#
# class Provider(providers.BaseProvider):
#
#     def vid_category(self):
#         return self.random_element(CATEGORY)
#
#
# class Command(BaseCommand):
#     help ="Command Information"
#
#     def handle(self, *args, **kwargs):
#         fake = Faker()
#         fake.add_provider(Provider)
#
#
#         #print(fake.vid_category())
#
#         for i in range(20):
#             fake_video = fake.file_path(depth=3, category='video')
#             ct = fake.vid_category()
#             u = fake.user_name()
#             Video.objects.create(#user=u,
#                                  video=fake_video,
#                                  name=fake.name(),
#                                  description=fake.text(max_nb_chars=70),
#                                  category=ct,
#                                  upload_date=fake.date_time_this_month())
#
#
#         check_count = Video.objects.all().count()
