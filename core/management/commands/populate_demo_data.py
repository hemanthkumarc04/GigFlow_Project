import io
import urllib.request
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from core.models import CustomUser, Product, OfflineService, Category

class Command(BaseCommand):
    help = 'Populates the database with demo e-commerce and offline service data.'

    def _fetch_random_image(self, width, height, seed=None):
        url = f"https://picsum.photos/{width}/{height}"
        if seed:
            url += f"?random={seed}"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            return ContentFile(response.read())
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Could not fetch image for seed {seed}: {e}"))
            return None

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating demo users...")
        
        # Customers
        customer, _ = CustomUser.objects.get_or_create(username='demo_customer', defaults={
            'email': 'customer@demo.com',
            'user_type': 'CUSTOMER',
            'wallet_balance': 1000.00
        })
        customer.set_password('password123')
        customer.save()
        
        # Seller
        seller, _ = CustomUser.objects.get_or_create(username='demo_seller', defaults={
            'email': 'seller@demo.com',
            'user_type': 'SELLER',
            'wallet_balance': 0.00
        })
        seller.set_password('password123')
        seller.save()
        
        # Offline Provider
        provider, _ = CustomUser.objects.get_or_create(username='demo_provider', defaults={
            'email': 'provider@demo.com',
            'user_type': 'OFFLINE_PROVIDER',
            'wallet_balance': 0.00
        })
        provider.set_password('password123')
        provider.save()
        
        self.stdout.write("Generating demo products...")
        Product.objects.all().delete()
        
        products_data = [
            {'name': 'Vintage Leather Jacket', 'price': 120.00, 'stock': 5, 'desc': 'Genuine vintage leather jacket, softly worn for that classic look.'},
            {'name': 'Mechanical Gaming Keyboard', 'price': 89.99, 'stock': 15, 'desc': 'RGB mechanical keyboard with blue switches.'},
            {'name': 'Handcrafted Ceramic Mug', 'price': 24.50, 'stock': 3, 'desc': 'Beautifully glazed handmade ceramic mug.'},
            {'name': 'Noise Cancelling Headphones', 'price': 199.99, 'stock': 8, 'desc': 'Premium wireless over-ear headphones with active noise cancellation.'},
            {'name': 'Organic Coffee Beans (1lb)', 'price': 18.00, 'stock': 20, 'desc': 'Freshly roasted organic arabica beans.'},
        ]
        
        for i, pd in enumerate(products_data):
            product = Product.objects.create(
                seller=seller,
                name=pd['name'],
                description=pd['desc'],
                price=pd['price'],
                stock=pd['stock']
            )
            img = self._fetch_random_image(600, 600, seed=i+100)
            if img:
                product.image.save(f'product_{i}.jpg', img, save=True)
                
        self.stdout.write("Generating demo offline services...")
        OfflineService.objects.all().delete()
        
        services_data = [
            {'title': 'Expert Plumbing Repair', 'price': 80.00, 'location': 'New York, NY', 'desc': 'Fixing leaks, unclogging drains, and installing new fixtures.', 'open': '08:00', 'close': '18:00'},
            {'title': 'Professional Lawn Care', 'price': 45.00, 'location': 'Los Angeles, CA', 'desc': 'Mowing, edging, and fertilizing your lawn.', 'open': '07:00', 'close': '15:00'},
            {'title': 'House Deep Cleaning', 'price': 150.00, 'location': 'Chicago, IL', 'desc': 'Thorough top-to-bottom cleaning of your entire home.', 'open': '09:00', 'close': '17:00'},
            {'title': 'Mobile Auto Detailing', 'price': 120.00, 'location': 'New York, NY', 'desc': 'Interior and exterior car cleaning at your location.', 'open': '10:00', 'close': '19:00'},
        ]
        
        for i, sd in enumerate(services_data):
            service = OfflineService.objects.create(
                provider=provider,
                title=sd['title'],
                description=sd['desc'],
                base_price=sd['price'],
                location=sd['location'],
                opening_time=sd['open'],
                closing_time=sd['close']
            )
            img = self._fetch_random_image(800, 500, seed=i+200)
            if img:
                service.image.save(f'service_{i}.jpg', img, save=True)
                
        self.stdout.write(self.style.SUCCESS('Successfully populated database with demo data!'))
        self.stdout.write("Accounts created (Password is 'password123' for all):")
        self.stdout.write(f"- Customer: {customer.username}")
        self.stdout.write(f"- Seller: {seller.username}")
        self.stdout.write(f"- Provider: {provider.username}")
