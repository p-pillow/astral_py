RUS_TEXTS = {
    "spells" : {
        0 : { # 0 level
            1 : {"title" : "Медитация", "alias": 'м',
                "self_message": "{player_name} медитирует",
                "self_lose_message": "{player_name} не может сосредоточиться на медитации"
                },
            2 : {"title" : "Бег",       "alias": 'б',
                "self_message": "{player_name} стремительно убегает",
                "self_lose_message": "{player_name} не может убежать"
                },
            3 : {"title" : "Левитация", "alias": 'л',
                "self_message": "{player_name} взмывает в воздух",
                "self_lose_message": "{player_name} не может взлететь"
                },
        },
        1: { # 1 level
            1  : {"title" : "Огненная стрела",
                  "target_message": "{player_name} выпускает стрелу по {target_name}",
                  "target_lose_message": "{player_name} не может кинуть оненную стрелу в {target_name}"
                  },
            2  : {"title" : "Ядовитый плевок",
                  "target_message": "{player_name} плюёт в лицо {target_name}",
                  "target_lose_message": "{player_name} не может плюнуть ядом в {target_name}"
                  },
            12 : {"title" : "Лечение",
                  "target_message": "{player_name} восстанавливает здоровье {target_name}",
                  "self_message": "{player_name} восстанавливает своё здоровье",
                  "self_lose_message": "{player_name} не может вылечить себя",
                  "target_lose_message": "{player_name} не может вылечить {target_name}"
                  },
            15 : {"title" : "Кошмарный сон",
                  "target_message": "{player_name} насылает кошмарный сон на {target_name}",
                  "target_lose_message": "{player_name} не может усыпить {target_name}",
                  },
            19 : {"title" : "Развеивание",
                  "target_message": "{player_name} чистит эффекты с {target_name}",
                  "self_message": "{player_name} чистится от эффектов",
                  "target_lose_message": "{player_name} не может развеять эффекты с {target_name}",
                  "self_lose_message": "{player_name} не может развеять свои эффекты",
                  },
            24 : {"title" : "Магический щит",
                  "target_message": "{player_name} прикрывает магическим щитом {target_name}",
                  "self_message": "{player_name} прячется под магическим щитом",
                  "target_lose_message": "{player_name} не может прикрыть магическим щитом {target_name}",
                  "self_lose_message": "{player_name} не может прикрыться магическим щитом",
                  },
        }
    }
}
