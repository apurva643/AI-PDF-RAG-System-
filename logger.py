from datetime import datetime


def log_question(

    question,

    answer

):

    with open(

        "chat_logs.txt",

        "a",

        encoding="utf-8"

    ) as file:

        file.write(

            f"{datetime.now()}\n"

        )

        file.write(

            f"Question:\n{question}\n\n"

        )

        file.write(

            f"Answer:\n{answer}\n"

        )

        file.write(

            "-" * 60 + "\n\n"

        )