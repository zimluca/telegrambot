import logging
import random

from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    Bot,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> None:
    """Inform user about what this bot can do"""
    update.message.reply_text(
        'Ciao! Sono il tuo bot incompetente!\
        per organizzare una nuova attività digitare /new'
    )
def Mike(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        'Mike Gay capo degli ebrei'
    )
def zimmo(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        'Sia sempre lodato il mio sommo e perfettissimo creatore Zimmo'
    )
def quote(update: Update, _: CallbackContext) -> None:
    mylist = ["marino è arrogante cit. zimmo", "viva le cantine cit. andre", "ed è wipeee cit. tata", "scusate per la polvere cit. bungie", "Sto fumando cit. tata", "Sono in torre cit. Titano", "Viva le pelate cit. zavala", "me piace er cazzo cit. osiride", "sono più inutile di un coltello che non taglia cit. ikora", "questi li ho già visti cit. Bille", "Zimmo è incompetente cit. Mari", "Trqnuilli questi sono delle bare cit. Savi"]
    update.message.reply_text(
        random.choice(mylist)
    )
def weekly(update: Update, context: CallbackContext) -> None:
    message = context.bot.send_photo(
        -1001498649999,
        "https://ibb.co/C193GTg"
        )
    message = context.bot.send_message(
        -1001498649999,
        "Ecco il programma settimanale!"
        )
    message = context.bot.send_poll(
        -1001498649999,
        "Clicca sulle attività a cui desideri partecipare. Gli orari di tali attività sono indicati nel calendario",
        ["Gran Maestro", "Raid", "Prove", "Attività varie"],
        is_anonymous=False,
        allows_multiple_answers=True,
    )

def new(update: Update, context: CallbackContext) -> None:
    message = context.bot.send_poll(
        -1001498649999,
        "Che attività vorresti organizzare?",
        ["Assalti", "Gran Maestro","cala 100K","PvP", "sopravvivenza", "Prove di Osiride", "azzardo", "Araldo", "profezia", "Presagio"],
        is_anonymous = False,
        allows_multiple_answers = False,
        )

    payload = {
        message.poll.id: {
            "questions": ["Assalti", "Gran Maestro","cala 100K","PvP", "sopravvivenza", "Prove di Osiride", "azzardo", "Araldo", "profezia", "Presagio"],
            "message_id": message.message_id,
            "chat_id": -1001498649999,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)




def new_activities(update: Update, context: CallbackContext) -> None:
    """Summarize a users poll vote"""
    answer = update.poll_answer
    poll_id = answer.poll_id
    try:
        questions = context.bot_data[poll_id]["questions"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return
    selected_options = answer.option_ids
    answer_string = ""
    for question_id in selected_options:
        if question_id != selected_options[-1]:
            answer_string += questions[question_id] + " e "
        else:
            answer_string += questions[question_id]
    context.bot.send_poll(
        context.bot_data[poll_id]["chat_id"],
        f"Cliccare qui sotto per prenotarsi alla seguente attività: {answer_string}!",
        ["Ci sono", "nah"],
        is_anonymous = False,
        allows_multiple_answers = False,
    )
    context.bot_data[poll_id]["answers"] += 1
    # Close poll after three participants voted
    if context.bot_data[poll_id]["answers"] == 1:
        context.bot.stop_poll(
            context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
        )


def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("1878647056:AAF6ocxrr6XLhyQNVHvJPbKyGJeJiAkcLoE")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('Mike', Mike))
    dispatcher.add_handler(CommandHandler('weekly', weekly))
    dispatcher.add_handler(PollAnswerHandler(new_activities))
    dispatcher.add_handler(CommandHandler('new', new))
    dispatcher.add_handler(CommandHandler('zimmo', zimmo))
    dispatcher.add_handler(CommandHandler('quote', quote))


    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
