# -*- coding: utf-8 -*-
 
RUS_TEXTS = {
    "spells" : {
        0 : { # 0 level
            1 : {"title" : "Медитация",
                "self_message": "{player_name} медитирует",
                "self_lose_message": "{player_name} не может сосредоточиться на медитации"
                },
            2 : {"title" : "Бег",
                "self_message": "{player_name} стремительно убегает",
                "self_lose_message": "{player_name} не может убежать"
                },
            3 : {"title" : "Левитация",
                "self_message": "{player_name} взмывает в воздух",
                "self_lose_message": "{player_name} не может взлететь"
                },
            4: {"title" : "Фортуна",
                "self_message": "{player_name} сбрасывает все свои заклинания, заменяя новыми",
                "self_lose_message": "{player_name} не может сменить свои заклинания"
            },
            5: {"title" : "Суицид",
                "self_message": "{player_name} сводит счеты со своей жизнью...",
                "self_lose_message": "{player_name} не удалось покончить с собой..."
            },
            6: {"title" : "Обмен",
                "self_message": "{player_name} обменивает {dropped_spells} на заклинание второго уровня",
                "self_lose_message": "{player_name} не может обменять свои заклинания",
                "self_lose_message2": "У {player_name} недостаточно заклинаний для обмена и он теряет все!"
                },
            7: {"title" : "Жертва",
                "self_message": "{player_name}  жертвует {dropped_spells} ради заклинания третьего уровня",
                "self_lose_message": "{player_name} не может пожертвовать своими заклинаниями"
                },
            8: {"title" : "Защита",
                "self_message": "{player_name} уходит в защиту",
                "self_lose_message": "{player_name} не может уйти в защиту"
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
    },
    "aliases": {
        'м':  (0, 1),
        'б':  (0, 2),
        'л':  (0, 3),
        'ф':  (0, 4),
        'гг': (0, 5),
        'о':  (0, 6),
        'ж':  (0, 7),
        'з':  (0, 8),
    },
    "effects": {
        1: {"title": "Горение", "message": "Горение наносит {player_name} {damage} урона"},
        2: {"title": "Отравление", "message": "Отравление наносит {player_name} {damage} урона"},
        3: {"title": "Лечение", "message": "Лечение восстанавливает у {player_name} {healing} здоровья"},
        4: {"title": "Кощмарный сон", "message": "Кощмарный сон сжигает у {player_name} {mpburn} и заклинание {dropped_spells}"},
        5: {"title": "Развеивание", "message": "Развеивание снимает с {player_name} эффекты {dropped_effects}"},
        6: {"title": "Защита", "message": "Защита {player_name} сбрасывает эффект {dropped_effects}"},
        7: {"title": "Медитация", "message": "Медитация восстанавливает у {player_name} {mpup} маны"},
 
    },
    "events": {
        "new_round": "Раунд №{}",
        "draw": "Ничья между командами:\n{}",
        "winner": "Победила команда {}",
        "ask_move": "Введите ходы пользователей в формате:\nКастер Ход Цель",
        "move_saved": "Записанный ход: {}, {}, {}",
        "move_updated": "Ход обновлен: {}, {}, {}"
    },
    "warnings": {
        "player_not_exists": "Игрок {} не существует!",
        "wrong_caster": "Игрок {} не может совершить ход!",
        "empty_move": "Вы ввели пустой ход!",
        "spell_not_exists": "Заклинания {} не существует в игре!",
        "bad_target": "Игрок {} не может быть целью заклинания {}!",
        "target_must_exist": "Для заклинания {} требуется указать цель!"
    }
}
