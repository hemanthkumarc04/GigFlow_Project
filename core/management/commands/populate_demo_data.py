import urllib.request
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from core.models import CustomUser, Product, OfflineService, Category, Job


class Command(BaseCommand):
    help = 'Populates the database with demo jobs, products and offline service data.'

    def _fetch_random_image(self, width, height, seed=None):
        url = f"https://picsum.photos/{width}/{height}"
        if seed:
            url += f"?random={seed}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=10)
            return ContentFile(response.read())
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  Could not fetch image (seed={seed}): {e}"))
            return None

    def handle(self, *args, **kwargs):

        # ─── Categories ──────────────────────────────────────────────────────
        self.stdout.write("Creating categories...")
        categories_data = [
            ('Web Development',      'web-development'),
            ('Design & Creative',    'design-creative'),
            ('Marketing',            'marketing'),
            ('Writing & Translation','writing-translation'),
        ]
        cats = {}
        for name, slug in categories_data:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})
            cats[slug] = cat

        # ─── Users ───────────────────────────────────────────────────────────
        self.stdout.write("Creating demo users...")

        provider, _ = CustomUser.objects.get_or_create(username='demo_client', defaults={
            'email': 'client@demo.com',
            'user_type': 'PROVIDER',
            'wallet_balance': 5000.00,
            'is_verified': True,
            'first_name': 'Alex',
            'last_name': 'Morgan',
        })
        provider.set_password('password123')
        provider.save()

        seller, _ = CustomUser.objects.get_or_create(username='demo_seller', defaults={
            'email': 'seller@demo.com',
            'user_type': 'SELLER',
            'wallet_balance': 0.00,
            'first_name': 'Jamie',
            'last_name': 'Lee',
        })
        seller.set_password('password123')
        seller.save()

        op, _ = CustomUser.objects.get_or_create(username='demo_provider', defaults={
            'email': 'provider@demo.com',
            'user_type': 'OFFLINE_PROVIDER',
            'wallet_balance': 0.00,
            'first_name': 'Sarah',
            'last_name': 'Kim',
        })
        op.set_password('password123')
        op.save()

        customer, _ = CustomUser.objects.get_or_create(username='demo_customer', defaults={
            'email': 'customer@demo.com',
            'user_type': 'CUSTOMER',
            'wallet_balance': 1000.00,
        })
        customer.set_password('password123')
        customer.save()

        # ─── Open Jobs ───────────────────────────────────────────────────────
        self.stdout.write("Creating open jobs...")
        jobs_data = [
            {
                'title': 'Build a React & Tailwind Dashboard UI',
                'category': 'web-development',
                'description': 'Need a skilled developer to build a clean, responsive SaaS dashboard.',
                'budget': 350.00,
            },
            {
                'title': 'Logo & Brand Identity Design',
                'category': 'design-creative',
                'description': 'Creative designer needed for a full brand identity package.',
                'budget': 200.00,
            },
            {
                'title': 'SEO Content Writing – 10 Blog Posts',
                'category': 'writing-translation',
                'description': '10 SEO-optimised blog posts on tech and productivity, 800-1200 words each.',
                'budget': 120.00,
            },
            {
                'title': 'Google & Meta Ads Campaign Setup',
                'category': 'marketing',
                'description': 'Set up and launch Google Ads and Meta Ads campaigns for an e-commerce store.',
                'budget': 280.00,
            },
        ]
        for jd in jobs_data:
            Job.objects.get_or_create(
                title=jd['title'],
                provider=provider,
                defaults={
                    'category': cats.get(jd['category']),
                    'description': jd['description'],
                    'budget': jd['budget'],
                    'status': 'OPEN',
                    'is_deposited': True,
                }
            )

        # ─── Products ────────────────────────────────────────────────────────
        self.stdout.write("Creating products...")
        products_data = [
            {'name': 'Vintage Leather Jacket',       'price': 120.00, 'stock': 5,  'desc': 'Genuine vintage leather jacket for that classic look.'},
            {'name': 'Mechanical Gaming Keyboard',   'price':  89.99, 'stock': 15, 'desc': 'RGB mechanical keyboard with blue switches.'},
            {'name': 'Handcrafted Ceramic Mug',      'price':  24.50, 'stock': 3,  'desc': 'Beautifully glazed handmade ceramic mug.'},
            {'name': 'Noise Cancelling Headphones',  'price': 199.99, 'stock': 8,  'desc': 'Premium wireless over-ear headphones.'},
            {'name': 'Organic Coffee Beans (1lb)',   'price':  18.00, 'stock': 20, 'desc': 'Freshly roasted organic arabica beans.'},
            {'name': 'Minimal Desk Lamp',            'price':  55.00, 'stock': 10, 'desc': 'Sleek LED desk lamp with adjustable colour temperature.'},
        ]
        for i, pd in enumerate(products_data):
            product, created = Product.objects.get_or_create(
                name=pd['name'],
                seller=seller,
                defaults={'description': pd['desc'], 'price': pd['price'], 'stock': pd['stock']}
            )
            if created:
                img = self._fetch_random_image(600, 600, seed=i + 100)
                if img:
                    product.image.save(f'product_{i}.jpg', img, save=True)

        # ─── Offline Services ────────────────────────────────────────────────
        self.stdout.write("Creating local services...")
        services_data = [
            {'title': 'Expert Plumbing Repair',    'price':  80.00, 'location': 'New York, NY',       'desc': 'Fixing leaks, unclogging drains, installing new fixtures.', 'open': '08:00', 'close': '18:00'},
            {'title': 'Professional Lawn Care',    'price':  45.00, 'location': 'Los Angeles, CA',    'desc': 'Mowing, edging, and fertilizing your lawn.',                'open': '07:00', 'close': '15:00'},
            {'title': 'House Deep Cleaning',       'price': 150.00, 'location': 'Chicago, IL',        'desc': 'Thorough top-to-bottom cleaning of your home.',             'open': '09:00', 'close': '17:00'},
            {'title': 'Mobile Auto Detailing',     'price': 120.00, 'location': 'New York, NY',       'desc': 'Interior and exterior car cleaning at your location.',      'open': '10:00', 'close': '19:00'},
            {'title': 'Home Electrician Services', 'price':  95.00, 'location': 'Houston, TX',        'desc': 'Safe wiring, panel upgrades, and outlet installation.',     'open': '08:00', 'close': '17:00'},
            {'title': 'Private Math Tutor',        'price':  40.00, 'location': 'San Francisco, CA',  'desc': 'One-on-one tutoring for high school and college maths.',    'open': '14:00', 'close': '20:00'},
        ]
        for i, sd in enumerate(services_data):
            service, created = OfflineService.objects.get_or_create(
                title=sd['title'],
                provider=op,
                defaults={
                    'description': sd['desc'],
                    'base_price': sd['price'],
                    'location': sd['location'],
                    'opening_time': sd['open'],
                    'closing_time': sd['close'],
                }
            )
            if created:
                img = self._fetch_random_image(800, 500, seed=i + 200)
                if img:
                    service.image.save(f'service_{i}.jpg', img, save=True)

        self.stdout.write(self.style.SUCCESS('\n✅ Demo data created successfully!'))
        self.stdout.write("\nDemo Accounts (password: password123):")
        self.stdout.write(f"  👤 Job Client  : {provider.username}")
        self.stdout.write(f"  🛍  Seller     : {seller.username}")
        self.stdout.write(f"  🏠 Local Svc   : {op.username}")
        self.stdout.write(f"  🧑 Customer    : {customer.username}")
