setup:
		@echo "To setup, source the configure_env.sh script. run the following command:"
		@echo "\t. configure_env.sh"

test:
		py.test tests

.PHONY: setup test