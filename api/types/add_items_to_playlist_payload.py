import strawberry
from .playlist import Playlist


@strawberry.type
class AddItemsToPlaylistPayload:
    """Response payload for the addItemsToPlaylist mutation.
    
    Attributes:
        code: Numeric status code similar to HTTP status codes.
        success: Boolean indicating if the operation succeeded.
        message: Human-readable result message.
        playlist: Updated playlist object with new items, or None if operation failed.
    """
    code: int = strawberry.field(
        description="Similar to HTTP status code, represents the status of the mutation."
    )
    success: bool = strawberry.field(
        description="Indicates whether the mutation was successful."
    )
    message: str = strawberry.field(description="Human-readable message for the UI.")
    playlist: Playlist | None = strawberry.field(
        description="The playlist that contains the newly added items."
    )
