import strawberry


@strawberry.type(description="A single audio file, usually a song.")
class Track:
    """Represents a track (song) in the Spotify system.
    
    Attributes:
        id: Unique Spotify ID for the track.
        name: Name of the track.
        duration_ms: Duration of the track in milliseconds.
        explicit: Flag indicating if the track contains explicit content.
        uri: Spotify URI that can be used to access the track.
    """
    id: strawberry.ID = strawberry.field(description="The ID for the track.")
    name: str = strawberry.field(description="The name of the track.")
    duration_ms: int = strawberry.field(description="The track length in milliseconds.")
    explicit: bool = strawberry.field(
        description="Whether or not the track has explicit lyrics (true = yes it does; false = no it does not OR unknown)"
    )
    uri: str = strawberry.field(
        description="The URI for the track, usually a Spotify link."
    )
