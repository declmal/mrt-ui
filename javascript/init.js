import { 
  roomName, update_yaml_configurations, update_console,
    create_socket } from './utils.js';

const yamlInitSocket = create_socket("yaml/init/");

yamlInitSocket.onopen = function(e) {
  yamlInitSocket.send(null);
};

yamlInitSocket.onmessage = function(e) {
  update_yaml_configurations(e);
  update_console("yaml parameters initialized.");
}

const submissionInitSocket = create_socket("submit/init/");

submissionInitSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  for (const [key, value] of Object.entries(data)) {
    const id = '#' + key;
    document.querySelector(id).value = value;
  }
  update_console("submission path initialized.");
}

submissionInitSocket.onopen = function(e) {
  submissionInitSocket.send(null);
};

const yamlResetter = document.querySelector('#yaml-resetter');

yamlResetter.onclick = function(e) {
  yamlInitSocket.send(null);
};
