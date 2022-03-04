import { roomName, create_socket, update_console_v2 } from './utils.js';

const modelSubmitSocket = create_socket("model/submit/");

const mrtExecutor = document.querySelector('#mrt-executor');
const modelSubmitter = document.querySelector('#model-submitter');

modelSubmitSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  if ('activate' in data) {
    mrtExecutor.disabled = false;
    modelSubmitter.disabled = false;
  }
  if ('message' in data) {
    if ('inc' in data) {
      update_console(data.message);
    } else {
      update_console_v2(data.message);
    }
  }
};

modelSubmitSocket.onclose = function(e) {
  console.error('model submit socket closed unexpectedly');
};

modelSubmitter.onclick = function(e) {
  mrtExecutor.disabled = true;
  modelSubmitter.disabled = true;
  let text_data = new Object();
  model_prefix = path.join(
    document.querySelector('#local-model-dir-locator').value,
    document.querySelector('#model-name-locator').value)
  text_data['symbol'] = model_prefix + '.json'
  text_data['params'] = model_prefix + '.params'
  text_data['dst'] = document.querySelector('#remote-model-dir-locator').value;
  text_data['host_addr'] = document.querySelector('#host-addr-locator').value;
  text_data['host_port'] = document.querySelector('#host-port-locator').value;
  modelSubmitSocket.send(JSON.stringify(text_data));
};
