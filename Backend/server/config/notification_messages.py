REFUND_REQUEST_SELLER = "\
A refund has been requested for your auction, \
please confirm that you have received the item back then\
click the link below to complete the refund\
"

REFUND_REQUEST_BUYER = "\
Your refund is being processed,\
Return the item to the seller within 3 days to complete the refund\
"


class NotificationMessages:
    """
    Class to hold notification messages.
    """

    AUCTION_CREATED = "Your auction has been created successfully."
    AUCTION_UPDATED = "Your auction has been updated successfully."
    AUCTION_DELETED = "Your auction has been deleted successfully."
    AUCTION_WON = "Congratulations! You have won the auction."
    AUCTION_LOST = "Unfortunately, you have lost the auction."
    
    BID_PLACED = "Your bid has been placed successfully."
    BID_UPDATED = "Your bid has been updated successfully."
    BID_DELETED = "Your bid has been deleted successfully."

    PAYMENT_SUCCESSFUL = "Payment completed successfully."
    PAYMENT_FAILED = "Payment failed. Please try again."

    REFUND_REQUESTED = "A refund request has been initiated."
    REFUND_COMPLETED = "Your refund has been processed successfully."

    ACCOUNT_VERIFIED = "Your account has been verified successfully."
    ACCOUNT_SUSPENDED = "Your account has been suspended. Please contact support."

    PASSWORD_RESET_REQUESTED = "Password reset requested. Please check your email for instructions."
    PASSWORD_RESET_SUCCESSFUL = "Your password has been reset successfully."

    EMAIL_VERIFICATION_REQUIRED = "Please verify your email address to continue."

    REFUND_REQUEST_SELLER = REFUND_REQUEST_SELLER
    REFUND_REQUEST_BUYER = REFUND_REQUEST_BUYER

notification_messages = NotificationMessages()
