from urllib.parse import quote

from app import create_app, db
from app.models import Category, Spice, Article, Image, Video


spices_data = [
    {
        "name": "Чёрный перец",
        "slug": "chernyy-perets",
        "category": "Перцы",
        "description": "Чёрный перец — одна из самых распространённых пряностей, получаемая из высушенных плодов растения Piper nigrum.",
        "origin": "Индия",
        "usage": "Используется для приготовления мяса, рыбы, супов, соусов и маринадов."
    },
    {
        "name": "Белый перец",
        "slug": "belyy-perets",
        "category": "Перцы",
        "description": "Белый перец получают из зрелых плодов Piper nigrum после удаления внешней оболочки.",
        "origin": "Индия",
        "usage": "Добавляется в светлые соусы, супы, блюда из рыбы и птицы."
    },
    {
        "name": "Красный перец",
        "slug": "krasnyy-perets",
        "category": "Перцы",
        "description": "Красный перец — пряность с выраженным острым вкусом, получаемая из плодов различных видов перца.",
        "origin": "Центральная и Южная Америка",
        "usage": "Используется в острых соусах, мясных блюдах, супах и маринадах."
    },
    {
        "name": "Паприка",
        "slug": "paprika",
        "category": "Перцы",
        "description": "Паприка представляет собой порошок из высушенного сладкого или слабоострого красного перца.",
        "origin": "Центральная Америка",
        "usage": "Добавляется в гуляш, супы, мясные блюда и овощные гарниры."
    },
    {
        "name": "Куркума",
        "slug": "kurkuma",
        "category": "Корни и корневища",
        "description": "Куркума — пряность золотистого цвета, получаемая из корневищ растения Curcuma longa.",
        "origin": "Южная Азия",
        "usage": "Используется в карри, рисе, супах, соусах и овощных блюдах."
    },
    {
        "name": "Имбирь",
        "slug": "imbir",
        "category": "Корни и корневища",
        "description": "Имбирь — ароматное корневище с характерным пряным и слегка жгучим вкусом.",
        "origin": "Юго-Восточная Азия",
        "usage": "Применяется в чае, выпечке, маринадах, соусах и мясных блюдах."
    },
    {
        "name": "Корица",
        "slug": "koritsa",
        "category": "Кора",
        "description": "Корица — ароматная пряность, получаемая из внутренней коры деревьев рода Cinnamomum.",
        "origin": "Шри-Ланка",
        "usage": "Добавляется в выпечку, десерты, напитки и некоторые мясные блюда."
    },
    {
        "name": "Гвоздика",
        "slug": "gvozdika",
        "category": "Бутоны и цветы",
        "description": "Гвоздика — высушенные нераскрывшиеся цветочные бутоны гвоздичного дерева.",
        "origin": "Молуккские острова, Индонезия",
        "usage": "Используется в маринадах, выпечке, напитках и мясных блюдах."
    },
    {
        "name": "Кардамон",
        "slug": "kardamon",
        "category": "Семена и плоды",
        "description": "Кардамон — ароматная пряность с насыщенным сладковато-пряным запахом.",
        "origin": "Индия",
        "usage": "Добавляется в кофе, чай, выпечку, десерты и восточные блюда."
    },
    {
        "name": "Мускатный орех",
        "slug": "muskatnyy-orekh",
        "category": "Семена и плоды",
        "description": "Мускатный орех — семя мускатного дерева с тёплым и насыщенным ароматом.",
        "origin": "Индонезия",
        "usage": "Используется в соусах, выпечке, картофельных и мясных блюдах."
    },
    {
        "name": "Шафран",
        "slug": "shafran",
        "category": "Бутоны и цветы",
        "description": "Шафран получают из высушенных рылец цветков крокуса посевного.",
        "origin": "Юго-Западная Азия",
        "usage": "Применяется в блюдах из риса, супах, соусах и десертах."
    },
    {
        "name": "Кориандр",
        "slug": "koriandr",
        "category": "Семена и плоды",
        "description": "Кориандр — пряность, получаемая из высушенных плодов растения Coriandrum sativum.",
        "origin": "Средиземноморье",
        "usage": "Добавляется в хлеб, маринады, колбасы, супы и овощные блюда."
    },
    {
        "name": "Зира",
        "slug": "zira",
        "category": "Семена и плоды",
        "description": "Зира, или кумин, — пряность с сильным тёплым ароматом и ореховыми нотами.",
        "origin": "Ближний Восток",
        "usage": "Используется в плове, блюдах из мяса, бобовых и овощей."
    },
    {
        "name": "Фенхель",
        "slug": "fenkhel",
        "category": "Семена и плоды",
        "description": "Фенхель — ароматное растение, семена которого обладают сладковатым анисовым вкусом.",
        "origin": "Средиземноморье",
        "usage": "Применяется в выпечке, рыбных блюдах, супах и овощных гарнирах."
    },
    {
        "name": "Анис",
        "slug": "anis",
        "category": "Семена и плоды",
        "description": "Анис — пряность с характерным сладким ароматом, напоминающим лакрицу.",
        "origin": "Восточное Средиземноморье",
        "usage": "Добавляется в выпечку, кондитерские изделия и напитки."
    },
    {
        "name": "Горчица",
        "slug": "gorchitsa",
        "category": "Семена и плоды",
        "description": "Горчица — пряность, получаемая из семян растений рода Brassica и Sinapis.",
        "origin": "Средиземноморье и Азия",
        "usage": "Используется для приготовления соусов, маринадов и приправ."
    },
    {
        "name": "Орегано",
        "slug": "oregano",
        "category": "Листья и травы",
        "description": "Орегано, или душица, — ароматная трава с насыщенным пряным вкусом.",
        "origin": "Средиземноморье",
        "usage": "Добавляется в пиццу, пасту, томатные соусы и мясные блюда."
    },
    {
        "name": "Базилик",
        "slug": "bazilik",
        "category": "Листья и травы",
        "description": "Базилик — ароматное растение с листьями, обладающими свежим пряным запахом.",
        "origin": "Южная Азия",
        "usage": "Используется в салатах, соусах, блюдах из томатов и пасте."
    },
    {
        "name": "Розмарин",
        "slug": "rozmarin",
        "category": "Листья и травы",
        "description": "Розмарин — вечнозелёное растение с хвойным ароматом и выраженным пряным вкусом.",
        "origin": "Средиземноморье",
        "usage": "Добавляется к мясу, картофелю, овощам и запечённым блюдам."
    },
    {
        "name": "Тимьян",
        "slug": "timyan",
        "category": "Листья и травы",
        "description": "Тимьян, или чабрец, — ароматная трава с тёплым и слегка терпким вкусом.",
        "origin": "Средиземноморье",
        "usage": "Применяется в супах, мясных блюдах, маринадах и соусах."
    }
]


def seed_database():
    categories = {}

    category_names = sorted({
        item["category"] for item in spices_data
    })

    for name in category_names:
        category = Category.query.filter_by(name=name).first()

        if category is None:
            category = Category(
                name=name,
                description=f"Категория специй: {name.lower()}."
            )
            db.session.add(category)

        categories[name] = category

    db.session.flush()

    for item in spices_data:
        spice = Spice.query.filter_by(slug=item["slug"]).first()

        if spice is None:
            spice = Spice(
                name=item["name"],
                slug=item["slug"],
                description=item["description"],
                origin=item["origin"],
                usage=item["usage"],
                category=categories[item["category"]]
            )
            db.session.add(spice)
            db.session.flush()

        if not spice.articles:
            db.session.add(Article(
                title=f"Описание специи: {spice.name}",
                description=spice.description,
                content=(
                    f"{spice.name}. {spice.description} "
                    f"Страна происхождения: {spice.origin}. "
                    f"Применение в кулинарии: {spice.usage}"
                ),
                source_name="База знаний SpiceSearch",
                source_url="https://ru.wikipedia.org/",
                spice=spice
            ))

        if not spice.images:
            search = quote(spice.name)

            db.session.add(Image(
                title=f"Изображения специи: {spice.name}",
                description=f"Поиск изображений специи {spice.name}.",
                image_url=(
                    "https://commons.wikimedia.org/wiki/"
                    f"Special:MediaSearch?type=image&search={search}"
                ),
                source_url="https://commons.wikimedia.org/",
                spice=spice
            ))

        if not spice.videos:
            search = quote(spice.name)

            db.session.add(Video(
                title=f"Видео о специи: {spice.name}",
                description=f"Видеоматериалы о специи {spice.name}.",
                video_url=(
                    "https://www.youtube.com/results?search_query="
                    f"{search}"
                ),
                source_name="YouTube",
                spice=spice
            ))

    db.session.commit()

    print("База знаний успешно наполнена.")
    print(f"Количество специй: {Spice.query.count()}")
    print(f"Количество категорий: {Category.query.count()}")
    print(f"Количество статей: {Article.query.count()}")
    print(f"Количество записей изображений: {Image.query.count()}")
    print(f"Количество видеозаписей: {Video.query.count()}")


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        try:
            seed_database()
        except Exception:
            db.session.rollback()
            raise
