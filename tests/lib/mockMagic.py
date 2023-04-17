from tests.data.device_tools_unit import (validate_router_bgp, return_validate_config_for_device,
                                          validate_intf, validate_true, device_data, image_bundle)
from unittest.mock import MagicMock
from cvprac.cvp_client_errors import CvpApiError


def fail_json(msg, code=1):
    """
    mock method for AnsibleModule fail_json()
    """
    raise SystemExit(code)


class MockCvpApi(MagicMock):
    def validate_config_for_device(self, device_mac, config):
        if config == validate_router_bgp['config']:
            return return_validate_config_for_device['return_validate_ruter_bgp']
        if config == validate_intf['config']:
            return return_validate_config_for_device['return_validate_intf']
        if config == validate_true['config']:
            return return_validate_config_for_device['return_validate_true']

    def get_image_bundle_by_name(self, name):
        """
        mock to get image_bundle
        """
        if name != 'Invalid_bundle_name':
            return image_bundle
        else:
            return None

    def apply_image_to_element(self, image, element, name, id_type,
                               create_task=True):
        """
        mock for apply_image_to_element
        """
        if 'imageBundleKeys' in image_bundle:
            if image_bundle['imageBundleKeys']:
                node_id = image_bundle['imageBundleKeys'][0]

        if 'id' in image_bundle:
            node_id = image_bundle['id']

        if create_task:
            if node_id and node_id != "error_id":
                return {'data': {'taskIds': ['57'], 'status': 'success'}}
            elif node_id == "error_id":
                raise CvpApiError(msg='Image bundle ID is not valid')
            else:
                return {'data': {'taskIds': [], 'status': 'fail'}}
        else:
            return None
