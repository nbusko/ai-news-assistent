max_new_tokens = 8000

check_date_time_prompt = \
"""
Извлеки информацию о теме и дате начала периода из запроса пользователя. 
Если тема не указана, а дату начала периода невозможно высчитать, верни 'no' в соответствующих полях.
Дату начала высчитывай исходя из запроса, например, если в запросе будет указана неделя верни сегодняшнюю дату минус семь дней в формате гггг-мм-дд, если указана дата, просто верни ее в нужном формате
Темы новостей выбери только из списка: наука, спорт, технологии, экономика, нейросети
Верните данные в формате JSON:
{{
"theme": "..." //тема новости или 'no', если тема не указана
"date": "..." //дата начала периода в формате гггг-мм-дд или 'no'
}}
Текст запроса пользователя: {request}
Сегодняшняя дата: {date}
Начни отвечать с {{"theme":
"""

map_reduce_news = \
"""
На основе запроса пользователя выбери наиболее соответствующие новости.
Учитывай релевантность и актуальность информации. 
Если новость подпись к фото то не выбирай ее, внимательно проверяй новости, если там упоминаются изображения то не выбирай ее
Запрос пользователя: {request}
Доступные новости: {news}
Верни список только с релевантными новостями
Ответ верни в формате списка:
[
"", // первая новость
"", // вторая новость
...
]
Начни отвечать с [
"""

generate_final_answer_prompt = \
"""
Максимально вежливо и позитивно ответь пользователю, что будешь рад помочь, далее предоставь список новостей в таком формате:
"Вот все новости, которые мне удалось найти по вашему запросу:
1. новость_1
2. новость_2
...
" 
Убери из новостей всю рекламу и информацию не относящуюся к новости, оставь только основной текст новости без заголовков.
Запрос пользователя: {request}. 
Новости: {news}
"""

is_bad_answer_prompt = \
"""
Ваш запрос не соответствует целевой функции данного проекта, которая заключается в предоставлении актуальных новостей по темам и датам.
"""

is_no_news_prompt = \
"""
К сожалению, по вашему запросу не удалось найти подходящих новостей. Попробуйте изменить запрос или уточнить параметры поиска.
"""

check_bad_request_prompt = \
"""
Проверь, соответствует ли запрос пользователя общей тематике проекта: Предоставление новостей. 
Верни JSON в таком формате:
{{
"result": "..." // "no", если запрос не соответствует тематике, "yes" - если соответствует
}}
Запрос: {request}
Начни отвечать с {{"result":
"""
