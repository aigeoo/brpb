from core.RatingActions import RatingActions

if __name__ == "__main__":
    try:
        bot = RatingActions()
        bot.start()
    except Exception as e:
        print(e)