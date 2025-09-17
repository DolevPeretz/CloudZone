import os


TABLE_NAME = os.getenv("TABLE_NAME", "customer_ids")

AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# שם הטבלה שלנו (תתאימי אם השתנה)
# לא חובה, אבל טוב שיהיה אם תרצי להשתמש בו בהמשך
# לוג לבל (נשתמש בו אחר כך ב־handlers)

