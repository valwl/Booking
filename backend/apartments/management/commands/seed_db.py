import os
import random
from decimal import Decimal
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files import File

from apartments.models.locations import Locations, LocationImg
from apartments.models.apartments import Apartment, ApartmentImg, PopularApartment, SliderImage
from booking.models.booking import Booking
from booking.models.payment import Payment

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds the database with production-style demo data including multiple gallery images and popular objects"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Clearing old data..."))

        PopularApartment.objects.all().delete()
        ApartmentImg.objects.all().delete()
        LocationImg.objects.all().delete()
        Payment.objects.all().delete()
        Booking.objects.all().delete()
        Apartment.objects.all().delete()
        Locations.objects.all().delete()
        User.objects.all().delete()

        fixtures_media_dir = os.path.join(settings.BASE_DIR, "apartments", "fixtures", "media")
        fix_apt_dir = os.path.join(fixtures_media_dir, "apartments")
        fix_loc_dir = os.path.join(fixtures_media_dir, "locations")
        fix_slide_dir = os.path.join(fixtures_media_dir, "slider")

        has_fixtures = os.path.exists(fix_apt_dir) and os.path.exists(fix_loc_dir)
        if not has_fixtures:
            self.stdout.write(self.style.ERROR(
                f"🚨 Source media fixtures not found at {fixtures_media_dir}!\n"
                f"Please create folders and put seed images there. Proceeding without files..."
            ))


        self.stdout.write(self.style.SUCCESS("Creating demo users..."))
        owner = User.objects.create_user(
            email="owner@gmail.com", first_name="John", last_name="Doe", password="password123", is_staff=True
        )
        client = User.objects.create_user(
            email="client@gmail.com", first_name="Alice", last_name="Smith", password="password123"
        )


        self.stdout.write(self.style.SUCCESS("Creating locations with description and image references..."))
        city_data = [
            {"name": "Paris", "desc": "The city of light, romance, and world-class culinary art."},
            {"name": "London", "desc": "A dynamic hub of history, royal heritage, and modern culture."},
            {"name": "New York", "desc": "The city that never sleeps, filled with iconic skyscrapers."},
            {"name": "Tokyo", "desc": "An ultra-modern metropolis blended perfectly with timeless traditions."},
            {"name": "Barcelona", "desc": "A vibrant coastal city famous for Gaudí architecture and sun."}
        ]

        location_objects = []
        for city in city_data:
            loc = Locations.objects.create(name=city["name"], description=city["desc"])
            location_objects.append(loc)

            if has_fixtures:
                loc_images = os.listdir(fix_loc_dir)
                matched_images = [img for img in loc_images if city["name"].lower() in img.lower()]

                images_to_upload = matched_images if matched_images else random.sample(loc_images, min(2, len(loc_images)))

                for img_name in images_to_upload:
                    img_path = os.path.join(fix_loc_dir, img_name)
                    with open(img_path, "rb") as f:
                        loc_img_instance = LocationImg(location=loc)

                        loc_img_instance.img.save(img_name, File(f), save=True)


        self.stdout.write(self.style.SUCCESS("Creating apartments and populating image galleries..."))
        apartment_titles = [
            "Cozy Industrial Studio", "Luxury Penthouse Skyline", "Modern Loft Near Metro Station",
            "Charming Apartment with Terrace", "Premium High-Tech Flat in Center", "Elegant Suite Near Park"
        ]

        apartments = []
        for title in apartment_titles:
            apt = Apartment.objects.create(
                title=title,
                description="Stunning production-quality property featuring premium modern amenities, fully equipped kitchen, high-speed Wi-Fi, and a prime urban location.",
                user=owner,
                base_price=Decimal(random.randint(80, 150)),
                weekend_price=Decimal(random.randint(160, 250)),
                location=random.choice(location_objects)
            )
            apartments.append(apt)


            if has_fixtures:
                apt_images = os.listdir(fix_apt_dir)
                if len(apt_images) >= 2:
                    chosen_room_pics = random.sample(apt_images, 2)
                    for img_name in chosen_room_pics:
                        img_path = os.path.join(fix_apt_dir, img_name)
                        with open(img_path, "rb") as f:
                            apt_img_instance = ApartmentImg(apartment=apt)
                            apt_img_instance.img.save(img_name, File(f), save=True)


        self.stdout.write(self.style.SUCCESS("Selecting and promoting popular apartments to the homepage..."))

        popular_selection = random.sample(apartments, min(3, len(apartments)))
        for apt in popular_selection:
            PopularApartment.objects.create(apartment=apt)

        if os.path.exists(fix_slide_dir):
            self.stdout.write(self.style.SUCCESS("Populating slider images..."))
            slider_images = os.listdir(fix_slide_dir)
            for img_name in slider_images:
                if img_name.startswith("."):
                    continue
                img_path = os.path.join(fix_slide_dir, img_name)
                with open(img_path, "rb") as f:
                    slider_instance = SliderImage()
                    slider_instance.image.save(img_name, File(f), save=True)
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ Slider source folder not found at {fix_slide_dir}, skipping slider seed."))



        self.stdout.write(self.style.SUCCESS("Creating transactional history log slices..."))


        past_booking = Booking.objects.create(
            user=client, apartment=random.choice(apartments),
            checkin_day=date.today() - timedelta(days=10), checkout_day=date.today() - timedelta(days=5),
            status=Booking.STATUS_COMPLETE, total_price=Decimal("450.00")
        )
        Payment.objects.create(
            booking=past_booking, amount=past_booking.total_price, status=Payment.STATUS_PAID,
            provider=Payment.PROVIDER_STRIPE, provider_payment_id="ch_mock_past_123"
        )

        active_booking = Booking.objects.create(
            user=client, apartment=random.choice(apartments),
            checkin_day=date.today() + timedelta(days=2), checkout_day=date.today() + timedelta(days=7),
            status=Booking.STATUS_PAID, total_price=Decimal("950.00")
        )
        Payment.objects.create(
            booking=active_booking, amount=active_booking.total_price, status=Payment.STATUS_PAID,
            provider=Payment.PROVIDER_STRIPE, provider_payment_id="ch_mock_active_456"
        )

        self.stdout.write(self.style.SUCCESS("🎉 Database architecture successfully seeded with live objects and media blocks!"))
        self.stdout.write(self.style.WARNING("Credentials: owner@gmail.com / client@gmail.com (password: password123)"))
