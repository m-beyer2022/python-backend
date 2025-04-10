import strawberry


@strawberry.input
class AddItemsToPlaylistInput:
    """Input type for adding items to a playlist.
    
    Attributes:
        playlist_id: The Spotify ID of the playlist to add items to.
        uris: List of Spotify track URIs to add to the playlist.
    """
    playlist_id: strawberry.ID = strawberry.field(description="The ID of the playlist.")
    uris: list[str] = strawberry.field(description="A list of Spotify URIs to add.")
