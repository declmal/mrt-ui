UNAME_OUT="$(uname -s)"
case "${UNAME_OUT}" in
  Linux*) BASH_FILE=~/.bashrc;;
  Darwin*) BASH_FILE=~/.bash_profile;;
  *) BASH_FILE="UNKNOWN:${UNAME_OUT}"
esac

echo "Environment Variable"
echo "    MRT_RPC_HOME : ${MRT_RPC_HOME}"
echo "    UNAME_OUT    : ${UNAME_OUT}"
echo "    BASH_FILE    : ${BASH_FILE}"
echo "    PYTHONPATH   : ${PYTHONPATH}"
echo ""

if [[ "x${MRT_RPC_HOME}" == "x" ]]; then
  MRT_RPC_HOME=`pwd`/python
  echo "Adding MRT_RPC_HOME: ${MRT_RPC_HOME}"
  echo "export MRT_RPC_HOME=${MRT_RPC_HOME}" >> ${BASH_FILE}
  echo "Inserting PYTHONPATH: ${PYTHONPATH}"
  echo "export PYTHONPATH=${MRT_RPC_HOME}:${PYTHONPATH}" >> ${BASH_FILE}
  echo "MRT-UI Environment Variables installed succussfully."
  echo "Attention please:"
  echo "    source bashfile {${BASH_FILE}} to activate environment."
fi
