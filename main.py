import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from config import States, TOKEN
from handlers import (
    start, date_handler, time_handler, address_handler,
    location, floor_number_handler, building_floors_handler, activity, people_reaction,
    custom_people_handler, skip_custom_people,
    
    process_item_reaction,
    building_class, damage_cracks, damage_plaster,
    damage_structural, damage_overall,
    building_tech_state, building_year,
    building_shape, building_diff,
    custom_building_handler, skip_custom_building,
    cancel, error_handler
)

from database import init_db

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler('bot.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def post_init(app):
    logger.info("Бот успешно запущен")
    await app.bot.set_my_commands([
        ('start', 'Начать опрос'),
        ('cancel', 'Отменить опрос')
    ])

async def post_shutdown(app):
    logger.info("Бот завершает работу")

def setup_handlers(app):
    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            States.DATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, date_handler)
            ],
            States.TIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, time_handler)
            ],
            States.ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, address_handler)
            ],
            States.LOCATION: [
                CallbackQueryHandler(location, pattern='^loc_')
            ],
            States.FLOOR_NUMBER: [  # ← здесь
                MessageHandler(filters.TEXT & ~filters.COMMAND, floor_number_handler)
            ],
            States.BUILDING_FLOORS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, building_floors_handler)
            ],
            States.ACTIVITY: [
                CallbackQueryHandler(activity, pattern='^act_')
            ],
            States.PEOPLE_REACTION: [
                CallbackQueryHandler(people_reaction, pattern='^radio_')
            ],
            States.CUSTOM_PEOPLE_REACTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, custom_people_handler),
                CallbackQueryHandler(skip_custom_people, pattern='^skip_people$')
            ],
            States.SELECT_ITEM_REACTION: [
                CallbackQueryHandler(process_item_reaction, pattern='^item_')
            ],
            States.BUILDING_CLASS: [
                CallbackQueryHandler(building_class, pattern='^cls_')
            ],
            States.DAMAGE_CRACKS: [
                CallbackQueryHandler(damage_cracks, pattern='^cr_')
            ],
            States.DAMAGE_PLASTER: [
                CallbackQueryHandler(damage_plaster, pattern='^pl_')
            ],
            States.DAMAGE_STRUCTURAL: [
                CallbackQueryHandler(damage_structural, pattern='^st_')
            ],
            States.DAMAGE_OVERALL: [
                CallbackQueryHandler(damage_overall, pattern='^ov_')
            ],
            States.BUILDING_TECH_STATE: [
                CallbackQueryHandler(building_tech_state, pattern='^cond_')
            ],
            States.BUILDING_YEAR: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, building_year)
            ],
            States.BUILDING_SHAPE: [
                CallbackQueryHandler(building_shape, pattern='^shape_')
            ],
            States.BUILDING_DIFF: [
                CallbackQueryHandler(building_diff, pattern='^diff_')
            ],
            States.CUSTOM_BUILDING_DAMAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, custom_building_handler),
                CallbackQueryHandler(skip_custom_building, pattern='^skip_building$')
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_message=False,
        per_chat=True,
        per_user=True
    )
    app.add_handler(conv)
    app.add_error_handler(error_handler)

async def post_shutdown(app):
    logger.info("Бот завершает работу")

def main():
    # Инициализация базы
    init_db()

    # Создаем и конфигурируем приложение
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    setup_handlers(app)

    # Запуск polling
    app.run_polling(
        drop_pending_updates=True,
        poll_interval=1.0,
        timeout=20
    )

if __name__ == '__main__':
    main()
