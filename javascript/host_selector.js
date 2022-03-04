import { create_socket } from './utils.js'

const hostTypeSelector = document.querySelector("#host-selection");
const hostAddrText = document.querySelector('#host-addr-locator');
const hostPortText = document.querySelector('#host-port-locator')

hostTypeSelector.onchange= function(e) {
  if (hostTypeSelector.value == 'local') {
    hostAddrText.value = "";
    hostAddrText.disabled = true;
    hostPortText.value = "";
    hostPortText.disabled = true;
  } else {
    hostAddrText.disabled = false;
    hostPortText.disabled = false;
  }
}
