import pytest
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mock_spotify_rest_api_client.models import (
    SpotifyObjectFeaturedPlaylists,
    SpotifyObjectPlaylist
)
from api.query import Query
from api.types.playlist import Playlist


@pytest.fixture
def mock_spotify_client():
    """Fixture providing a mocked Spotify client"""
    client = MagicMock()
    client.get_async_httpx_client.return_value = AsyncMock()
    return client


def create_mock_playlist():
    """Helper to create a mock playlist with all required fields"""
    from mock_spotify_rest_api_client.models import (
        SpotifyObjectExternalUrl,
        SpotifyObjectFollowers,
        SpotifyObjectUserSimplified,
        SpotifyObjectPaginatedSpotifyObjectPlaylistTrack
    )
    
    return SpotifyObjectPlaylist(
        id="123",
        name="Test Playlist",
        description="Test Description",
        collaborative=False,
        external_urls=SpotifyObjectExternalUrl(spotify=""),
        followers=SpotifyObjectFollowers(total=0),
        href="https://api.spotify.com/v1/playlists/123",
        images=[],
        owner=SpotifyObjectUserSimplified(
            display_name="Test Owner",
            external_urls=SpotifyObjectExternalUrl(spotify=""),
            href="",
            id="owner123", 
            type="user",
            uri=""
        ),
        public=False,
        snapshot_id="snapshot123",
        tracks=SpotifyObjectPaginatedSpotifyObjectPlaylistTrack(
            href="",
            items=[],
            limit=20,
            next_=None,
            offset=0,
            previous=None,
            total=0
        ),
        type="playlist",
        uri="spotify:playlist:123"
    )


@pytest.mark.asyncio
async def test_featured_playlists_success(mock_spotify_client):
    """Test successful response with playlists"""
    # Mock raw API response structure
    mock_response = {
        "message": "Test message",
        "playlists": {
            "href": "https://api.spotify.com/v1/playlists",
            "items": [{
                "id": "123",
                "name": "Test Playlist", 
                "description": "Test Description",
                "collaborative": False,
                "external_urls": {"spotify": ""},
                "followers": {"total": 0},
                "href": "https://api.spotify.com/v1/playlists/123",
                "images": [],
                "owner": {
                    "display_name": "Test Owner",
                    "external_urls": {"spotify": ""},
                    "followers": {"total": 0},  # Added missing required field
                    "href": "",
                    "id": "owner123",
                    "type": "user",
                    "uri": ""
                },
                "public": False,
                "snapshot_id": "snapshot123",
                "tracks": {
                    "href": "",
                    "items": [],
                    "limit": 20,
                    "next": None,
                    "offset": 0,
                    "previous": None,
                    "total": 0
                },
                "type": "playlist",
                "uri": "spotify:playlist:123"
            }],
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total": 1
        }
    }
    
    # Mock client response
    mock_client = mock_spotify_client.get_async_httpx_client.return_value
    mock_client.request.return_value = MagicMock()
    mock_client.request.return_value.json.return_value = mock_response
    mock_client.request.return_value.status_code = 200
    
    # Create context with mock client
    info = MagicMock()
    info.context = {"spotify_client": mock_spotify_client}
    
    # Call resolver
    query = Query()
    result = await query.featured_playlists(info)
    
    # Assertions
    assert len(result) == 1
    assert isinstance(result[0], Playlist)
    assert result[0].id == "123"
    assert result[0].name == "Test Playlist"
    assert result[0].description == "Test Description"


@pytest.mark.asyncio
async def test_featured_playlists_empty(mock_spotify_client):
    """Test empty response case"""
    mock_response = SpotifyObjectFeaturedPlaylists(
        message="Test message",
        playlists={"items": [], "total": 0}
    )
    
    mock_client = mock_spotify_client.get_async_httpx_client.return_value
    mock_client.request.return_value = MagicMock()
    mock_client.request.return_value.json.return_value = {
        "message": mock_response.message,
        "playlists": {
            "href": "https://api.spotify.com/v1/playlists",
            "items": [],
            "limit": 20,
            "next": None,
            "offset": 0,
            "previous": None,
            "total": 0
        }
    }
    mock_client.request.return_value.status_code = 200
    
    info = MagicMock()
    info.context = {"spotify_client": mock_spotify_client}
    
    query = Query()
    result = await query.featured_playlists(info)
    
    assert len(result) == 0


@pytest.mark.asyncio
async def test_featured_playlists_error(mock_spotify_client):
    """Test error case"""
    mock_client = mock_spotify_client.get_async_httpx_client.return_value
    mock_client.request.side_effect = Exception("API Error")
    
    info = MagicMock()
    info.context = {"spotify_client": mock_spotify_client}
    
    query = Query()
    
    with pytest.raises(Exception, match="API Error"):
        await query.featured_playlists(info)
