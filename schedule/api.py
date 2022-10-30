from datetime import time

from schedule.models import Server, Room


def get_server_choice(room_id, user):
    choices = [("", "---------", None)]
    qs = Server.objects.all()
    if room_id:
        assert user.organization.room.filter(id=room_id).exists()
        qs = qs.filter(
            room=room_id,
        )
    # Используем этот генератор вместо values,
    # что бы брать название из __str__
    choices.extend([(item.id, str(item), item.type) for item in qs])
    return choices


def get_conferences_on_server():

    return [
        {
            "name": "Обсуждение бюджета 2023 года",
            "time": "8:30 - 9:30",
            "count": 50,
            "max_count": 100,
        },
        {
            "name": "Импортозамещение в сфере IT",
            "time": "10:30 - 12:00",
            "count": 100,
            "max_count": 100,
        },
        {
            "name": "Искусственный интеллект в ГИС",
            "time": "14:00 - 14:30",
            "count": 70,
            "max_count": 100,
        },
        {
            "name": "Планерка",
            "time": "17:30 - 18:00",
            "count": 10,
            "max_count": 100,
        },
    ]


def get_bookings_on_room():

    return [
        {
            "name": "Обсуждение бюджета 2023 года",
            "time": "8:30 - 9:30",
        },
        {
            "name": "Импортозамещение в сфере IT",
            "time": "10:30 - 12:00",
        },
        {
            "name": "Искусственный интеллект в ГИС",
            "time": "14:00 - 14:30",
        },
        {
            "name": "Планерка",
            "time": "17:30 - 18:00",
        },
    ]
