function force_source {
  # echo "force source -- $#: $@|"
  sourced=0
  if [ -n "$ZSH_EVAL_CONTEXT" ]; then
    # echo "zsh"
    case $ZSH_EVAL_CONTEXT in *:file) sourced=1;; esac
  elif [ -n "$BASH_VERSION" ]; then
    # echo "bash"
    if ! [ "${BASH_SOURCE[0]}" -ef "$0" ]; then
      # echo "Hey, you should source this script, not execute it!"
      # exit 1
      sourced=1
    fi
    # (return 0 2>/dev/null) && sourced=1
  else # All other shells: examine $0 for known shell binary filenames
    # Detects `sh` and `dash`; add additional shell filenames as needed.
    # echo "other shell"
    case ${0##*/} in dash|-dash|bash|-bash|ksh|-ksh|sh|-sh) sourced=1;; esac
  fi
  # echo "checked: $sourced"
  if [ "$sourced" != "1" ]; then
    echo -e "You must use source for "\`$(basename $1)\`"\n\t. $(basename $1)"
    exit # not return because "you can only return from a funtion or sourced script"
  fi
}
force_source $0

function handler {
  echo -e "Interrupted, exiting..."
  return
}
trap handler INT

echo "Exiting/interrupting this script (ctrl-c) may behave unexpectedly since it's sourced. Sorry!"

project_name="AutoFIT"
env_name="autofit"

# ensure script run from root of repository
if [ ! -f "setup.py" ]; then
  # echo ${BASH_SOURCE[0]}
  echo "You must run this script from the root of the $project_name repository: $(dirname ${BASH_SOURCE[0]})"
  use_cd=0
  while true; do
      read -p "Do you want to cd to the root of the $project_name repository ([y]/n)? " yn
      case $yn in
          "" | [Yy]* ) use_cd=1; break;;
          [Nn]* ) break;;
          * ) echo "Please answer yes or no.";;
      esac
  done
  if [ $use_cd -eq 0 ]; then
    return
  fi
  echo "Changing directory to $(dirname ${BASH_SOURCE[0]})"
  cd $(dirname ${BASH_SOURCE[0]})
fi

env_name="autofit"

conda activate $env_name