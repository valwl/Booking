import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apartments.models.apartments import Apartment
from apartments.models.locations import Locations
from booking.models.booking import Booking

User = get_user_model()


class ApartmentRulesTestCase(APITestCase):
    def setUp(self):
        # 1. Создаем тестовых пользователей с учетом требований CustomUserManager (передаем email)
        self.owner = User.objects.create_user(first_name="owner", email="owner@example.com", password="password123")
        self.client_user = User.objects.create_user(
            first_name="client", email="client@example.com", password="password123"
        )
        self.hacker = User.objects.create_user(first_name="hacker", email="hacker@example.com", password="password123")

        # 2. Создаем обязательную тестовую локацию
        self.test_location = Locations.objects.create(name="Test City")

        # 3. Создаем тестовые апартаменты
        self.apartment = Apartment.objects.create(
            title="Luxury Test Apartment",
            description="Beautiful views, production-ready quality.",
            user=self.owner,
            base_price=Decimal("100.00"),
            weekend_price=Decimal("150.00"),
            location=self.test_location,
        )

        # 4. Базовые даты бронирования
        self.start_date = datetime.date.today() + datetime.timedelta(days=2)
        self.end_date = datetime.date.today() + datetime.timedelta(days=5)

        # 5. Имена эндпоинтов из urls.py
        self.booking_list_url = reverse("booking-list")
        self.stripe_webhook_url = reverse("stripe_webhook")
        self.available_dates_url = reverse("available_dates", kwargs={"apartment_id": self.apartment.id})

        # По умолчанию авторизуем честного клиента для прохождения REST-тестов
        self.client.force_authenticate(user=self.client_user)

    def test_apartment_update_delete_only_by_owner(self):
        """Только владелец может изменять/удалять свои апартаменты"""
        apartment_update_url = reverse("apartment_update", kwargs={"pk": self.apartment.id})
        apartment_delete_url = reverse("apartment_delete", kwargs={"pk": self.apartment.id})

        # Авторизуем постороннего пользователя (хакера)
        self.client.force_authenticate(user=self.hacker)

        # Пытаемся обновить чужой объект
        response_update = self.client.put(apartment_update_url, {"title": "Hacked Title"}, format="json")
        self.assertEqual(response_update.status_code, status.HTTP_403_FORBIDDEN)

        # Пытаемся удалить чужой объект
        response_delete = self.client.delete(apartment_delete_url)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_review_only_for_completed_bookings(self):
        """Отзыв можно создать ТОЛЬКО если статус брони COMPLETED"""
        # Создаем PENDING бронь
        self.client.force_authenticate(user=self.client_user)

        booking = Booking.objects.create(
            user=self.client_user,
            apartment=self.apartment,
            checkin_day=self.start_date,
            checkout_day=self.end_date,
            status="PENDING",
            total_price=Decimal("300.00"),
        )

        review_url = reverse("create_review", kwargs={"booking_id": booking.id})
        review_data = {"rating": 5, "text": "Great!"}

        # Попытка 1: Статус PENDING -> Ошибка 400 или 403 (в зависимости от твоих настроек)
        response = self.client.post(review_url, review_data, format="json")
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN])

        # Попытка 2: Переводим статус в COMPLETED -> Успех 201
        booking.status = "complete"
        booking.save()

        response = self.client.post(review_url, review_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
