from pydantic import BaseModel
from typing import Optional


class NotificationObject(BaseModel):
    """
    Base class for notification objects.
    """
    message: str
    link: Optional[list[str]] = None
    
    model_config = {
        "from_attributes": True,
        "extra": "ignore"
    }


class NotificationMessages:
    """
    Class to hold all notification messages as NotificationObject instances.
    """

    # Auction related notifications
    AUCTION_CREATED = NotificationObject(
        message="Your auction has been created successfully.",
        link=["/auctions/"]
    )

    AUCTION_UPDATED = NotificationObject(
        message="Your auction has been updated successfully.",
        link=["/auctions/"]
    )

    AUCTION_DELETED = NotificationObject(
        message="Your auction has been deleted successfully.",
        link=["/auctions/"]
    )

    AUCTION_WON = NotificationObject(
        message="Congratulations! You have won the auction.",
        link=["/auctions/won/"]
    )

    AUCTION_LOST = NotificationObject(
        message="Unfortunately, you have lost the auction.",
        link=["/auctions/"]
    )

    AUCTION_RESTARTED = NotificationObject(
        message="Your Auction has been restarted successfully.",
        link=["/products/"]
    )

    # Bidding related notifications
    BID_PLACED = NotificationObject(
        message="Your bid has been placed successfully.",
        link=["/auctions/my-bids/"]
    )

    BID_UPDATED = NotificationObject(
        message="Your bid has been updated successfully.",
        link=["/auctions/my-bids/"]
    )

    BID_DELETED = NotificationObject(
        message="Your bid has been deleted successfully.",
        link=["/auctions/"]
    )

    # Payment related notifications
    PAYMENT_SUCCESSFUL = NotificationObject(
        message="Payment completed successfully.",
        link=["/payments/history/"]
    )

    PAYMENT_FAILED = NotificationObject(
        message="Payment failed. Please try again.",
        link=["/payments/retry/"]
    )

    # Account related notifications
    ACCOUNT_VERIFIED = NotificationObject(
        message="Your account has been verified successfully.",
        link=["/profile/"]
    )

    ACCOUNT_SUSPENDED = NotificationObject(
        message="Your account has been suspended. Please contact support.",
        link=["/support/"]
    )

    # Password related notifications
    PASSWORD_RESET_REQUESTED = NotificationObject(
        message="Password reset requested. Please check your email for instructions.",
        link=["/auth/check-email/"]
    )

    PASSWORD_RESET_SUCCESSFUL = NotificationObject(
        message="Your password has been reset successfully.",
        link=["/auth/login/"]
    )

    # Email verification
    EMAIL_VERIFICATION_REQUIRED = NotificationObject(
        message="Please verify your email address to continue.",
        link=["/auth/verify-email/"]
    )

    # Refund related notifications
    REFUND_REQUEST_SELLER = NotificationObject(
        message="A refund has been requested for your auction, "
                "please confirm that you have received the item back then "
                "click the link below to complete the refund",
        link=["/auctions/payments/complete_refund/"]
    )

    REFUND_REQUEST_BUYER = NotificationObject(
        message="Your refund is being processed, "
                "Return the item to the seller within 3 days to complete the refund",
        link=["/refunds/track/"]
    )

    REFUND_COMPLETED = NotificationObject(
        message="Your refund has been completed successfully.",
        link=["/products/", "/product-details/"]
    )

    BID_POINTS_EARNED = NotificationObject(
        message="You have earned bid points for your recent activity.",
        link=["/dashboard/"],
    )


# Create a singleton instance for easy access
notification_messages = NotificationMessages()
