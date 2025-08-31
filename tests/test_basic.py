"""Basic smoke tests."""


def test_import() -> None:
    """Test that we can import the main module."""
    import sonder

    assert sonder.__version__ == "0.1.0"


def test_entity_creation() -> None:
    """Test basic entity creation."""
    from sonder.entity.frog import Frog

    frog = Frog(x=5, y=10)
    assert frog.x == 5
    assert frog.y == 10
    assert frog.display_char == "F"
    assert frog.has_tag("frog")


def test_world_creation() -> None:
    """Test world creation."""
    from sonder.core.world import World

    world = World(width=50, height=30)
    assert world.width == 50
    assert world.height == 30
    assert world.is_valid_position(25, 15)
    assert not world.is_valid_position(-1, 15)
    assert not world.is_valid_position(25, 35)
