from mnubo.services import MNUOwnerServices, MNUSmartObjectServices, MNUEventServices
from mnubo.models import MNUOwner, MNUSmartObject, MNUEvent
from mock import Mock
import uuid

####################################
# MNUOwnerServices
####################################


def test_create_owner():
    event_id = str(uuid.uuid1())
    api_manager_mock = Mock()
    api_manager_mock.post.return_value = 'SUCCESS'

    owner_services = MNUOwnerServices(api_manager_mock)
    owner = MNUOwner('USERNAME', 'PASSWORD', '2015-01-01T12:00:00', event_id)

    create = owner_services.create(owner)
    api_manager_mock.post.assert_called_with('owners', {'username': 'USERNAME', 'x_registration_date': '2015-01-01T12:00:00', 'x_password': 'PASSWORD', 'event_id': event_id})
    assert create == 'SUCCESS'


def test_claim_owner():
    api_manager_mock = Mock()
    api_manager_mock.post.return_value = 'SUCCESS'

    owner_services = MNUOwnerServices(api_manager_mock)
    claim = owner_services.claim('owner', 'device_id')

    api_manager_mock.post.assert_called_with('owners/owner/objects/device_id/claim')
    assert claim == 'SUCCESS'


def test_update_owner():
    api_manager_mock = Mock()
    api_manager_mock.put.return_value = 'SUCCESS'

    owner_services = MNUOwnerServices(api_manager_mock)
    owner = MNUOwner('USERNAME', 'PASSWORD', '2015-01-01T12:00:00')
    update = owner_services.update(owner)

    api_manager_mock.put.assert_called_with('owners/USERNAME', {'username': 'USERNAME', 'x_registration_date': '2015-01-01T12:00:00', 'x_password': 'PASSWORD', 'event_id': None})
    assert update == 'SUCCESS'


def test_delete_owner():
    api_manager_mock = Mock()
    api_manager_mock.delete.return_value = 'SUCCESS'

    owner_services = MNUOwnerServices(api_manager_mock)
    delete = owner_services.delete('owner')

    api_manager_mock.delete.assert_called_with('owners/owner')
    assert delete == 'SUCCESS'

####################################
# MNUSmartObjectServices
####################################


def test_create_object():
    api_manager_mock = Mock()
    api_manager_mock.post.return_value = 'SUCCESS'

    object_services = MNUSmartObjectServices(api_manager_mock)
    smart_object = MNUSmartObject('DEVICE_ID', 'OBJECT_TYPE', '2015-01-01T12:00:00')
    create = object_services.create(smart_object)

    api_manager_mock.post.assert_called_with('objects', {'x_device_id': 'DEVICE_ID', 'x_object_type': 'OBJECT_TYPE', 'event_id': None, 'x_owner': None, 'x_registration_date': '2015-01-01T12:00:00'})
    assert create == 'SUCCESS'


def test_update_object():
    api_manager_mock = Mock()
    api_manager_mock.put.return_value = 'SUCCESS'

    object_services = MNUSmartObjectServices(api_manager_mock)
    smart_object = MNUSmartObject('DEVICE_ID', 'OBJECT_TYPE', '2015-01-01T12:00:00')
    update = object_services.update(smart_object)

    api_manager_mock.put.assert_called_with('objects/DEVICE_ID', {'x_device_id': 'DEVICE_ID', 'x_object_type': 'OBJECT_TYPE', 'event_id': None, 'x_owner': None, 'x_registration_date': '2015-01-01T12:00:00'})
    assert update == 'SUCCESS'


def test_delete_object():
    api_manager_mock = Mock()
    api_manager_mock.delete.return_value = 'SUCCESS'

    object_services = MNUSmartObjectServices(api_manager_mock)
    delete = object_services.delete('object')

    api_manager_mock.delete.assert_called_with('objects/object')
    assert delete == 'SUCCESS'

####################################
# MNUEventServices
####################################


def test_send_event():
    api_manager_mock = Mock()
    api_manager_mock.post.return_value = 'SUCCESS'

    event_services = MNUEventServices(api_manager_mock)
    event = MNUEvent('EVENT_ID', 'OBJECT', 'EVENT_TYPE', '2015-11-03T21:40:39.534447')
    send = event_services.send(event)

    api_manager_mock.post.assert_called_with('events', {'event_id': 'EVENT_ID', 'x_timestamp': '2015-11-03T21:40:39.534447', 'x_event_type': 'EVENT_TYPE', 'timeseries': None, 'x_object': 'OBJECT'})
    assert send == 'SUCCESS'


def test_send_event_to_object():
    pass


