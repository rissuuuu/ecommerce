import pytest
from user_components.user.domain import model


@pytest.mark.user
@pytest.mark.asyncio
async def test_user(model_factory: model.user_factory):
    assert isinstance(model_factory, model.User)
    assert model_factory is not None
