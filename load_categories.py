import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Category
categories = [
    {'name': 'Web Development', 'slug': 'web-development', 'description': 'Frontend, Backend, Full Stack'},
    {'name': 'Graphic Design', 'slug': 'graphic-design', 'description': 'Logos, Branding, UI/UX'},
    {'name': 'Copywriting', 'slug': 'copywriting', 'description': 'Articles, SEO, Sales Copy'},
    {'name': 'Video Editing', 'slug': 'video-editing', 'description': 'YouTube, TikTok, Corporate'},
    {'name': 'Digital Marketing', 'slug': 'digital-marketing', 'description': 'Social Media, Ads, Strategy'},
    {'name': 'Voice Over', 'slug': 'voice-over', 'description': 'Audiobooks, Ads, Animation'},
    {'name': 'Data Entry', 'slug': 'data-entry', 'description': 'Excel, Admin Support'},
    {'name': 'Virtual Assistant', 'slug': 'virtual-assistant', 'description': 'Scheduling, Email, Operations'},
]

for cat_data in categories:
    Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
print('Categories populated successfully!')
