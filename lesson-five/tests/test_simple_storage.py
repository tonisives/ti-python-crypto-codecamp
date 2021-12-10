from brownie import SimpleStorage, accounts

# test that after deploy function, retrieve returns 0
def test_deploy():
    # Arrange - setup all pieces
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0

    # Assert
    assert starting_value == expected

def test_update():
    # Arrange - setup all pieces
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    
    # Act
    simple_storage.store(4, {"from": account})
    updated_value = simple_storage.retrieve()

    # assert
    assert updated_value == 4
